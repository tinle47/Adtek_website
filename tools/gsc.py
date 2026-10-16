"""Google Search Console cho blog Adtek: gửi lại sitemap, kiểm tra bài đã được Google lập chỉ mục chưa.

Đăng nhập bằng service account: biến môi trường GSC_SERVICE_ACCOUNT chứa file khóa JSON (nguyên văn hoặc base64).
Email của service account phải được thêm vào property adtek.agency trong Search Console với quyền Full.
Google không có API cho nút "Yêu cầu lập chỉ mục": bài chưa được index thì in link để anh Tin bấm tay.

Cách dùng:
  python3 tools/gsc.py sites              property mà service account truy cập được (kiểm tra kết nối)
  python3 tools/gsc.py submit             gửi lại sitemap_index.xml
  python3 tools/gsc.py inspect <số bài>   tình trạng index của bài, ghi index_status, index_checked vào calendar.json
  python3 tools/gsc.py pending [số ngày]  kiểm tra bài đăng từ <số ngày> ngày trước (mặc định 2, tối đa 30 ngày) mà chưa index, in link bấm tay
"""
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

from blog_post import VN, find, load, save

SITE_URL = "https://adtek.agency"
SITEMAP = f"{SITE_URL}/sitemap_index.xml"
SCOPE = "https://www.googleapis.com/auth/webmasters"
TOKEN_URL = "https://oauth2.googleapis.com/token"
WEBMASTERS = "https://www.googleapis.com/webmasters/v3"
INSPECT = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"


def b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def credentials():
    raw = os.environ.get("GSC_SERVICE_ACCOUNT", "").strip()
    if not raw:
        sys.exit("Chưa có GSC_SERVICE_ACCOUNT: thêm khóa JSON của service account vào biến môi trường của môi trường cloud.")
    if not raw.startswith("{"):
        raw = base64.b64decode(raw).decode()
    return json.loads(raw)


def token():
    """Đổi JWT ký bằng khóa service account lấy access token (hạn 1 giờ). Ký bằng openssl để không cần thư viện Google."""
    sa = credentials()
    now = int(time.time())
    head = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    claim = b64url(json.dumps({"iss": sa["client_email"], "scope": SCOPE, "aud": TOKEN_URL,
                               "iat": now, "exp": now + 3600}).encode())
    with tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False) as f:
        f.write(sa["private_key"])
        key = f.name
    try:
        os.chmod(key, 0o600)
        sig = subprocess.run(["openssl", "dgst", "-sha256", "-sign", key], input=f"{head}.{claim}".encode(),
                             capture_output=True, check=True).stdout
    finally:
        os.unlink(key)
    r = call("POST", TOKEN_URL, form={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                                      "assertion": f"{head}.{claim}.{b64url(sig)}"})
    if "access_token" not in r:
        sys.exit(f"Lỗi đăng nhập Google: {str(r)[:300]}")
    return r["access_token"]


def call(method, url, body=None, form=None, bearer=None):
    cmd = ["curl", "-sS", "--max-time", "60", "-X", method, url]
    if bearer:
        cmd += ["-H", f"Authorization: Bearer {bearer}"]
    data = None
    if form:
        for k, v in form.items():
            cmd += ["--data-urlencode", f"{k}={v}"]
    elif body is not None:
        cmd += ["-H", "Content-Type: application/json", "--data-binary", "@-"]
        data = json.dumps(body)
    r = subprocess.run(cmd, input=data, capture_output=True, text=True)
    if not r.stdout.strip():
        return {}
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"error": r.stdout[:300]}


def property_url(tok):
    """Property của adtek.agency: ưu tiên Domain property (sc-domain:), sau đó URL-prefix."""
    sites = [s["siteUrl"] for s in call("GET", f"{WEBMASTERS}/sites", bearer=tok).get("siteEntry", [])
             if s.get("permissionLevel") != "siteUnverifiedUser"]
    for cand in ("sc-domain:adtek.agency", f"{SITE_URL}/", "https://www.adtek.agency/"):
        if cand in sites:
            return cand
    sys.exit(f"Service account chưa được thêm vào property adtek.agency. Đang thấy: {sites}")


def manual_link(prop, url):
    return f"https://search.google.com/search-console/inspect?resource_id={quote(prop, safe='')}&id={quote(url, safe='')}"


def inspect(data, post, tok, prop):
    url = f"{SITE_URL}/{post['slug']}/"
    r = call("POST", INSPECT, {"inspectionUrl": url, "siteUrl": prop, "languageCode": "vi"}, bearer=tok)
    res = r.get("inspectionResult", {}).get("indexStatusResult")
    if not res:
        sys.exit(f"Lỗi kiểm tra {url}: {str(r)[:300]}")
    post["index_status"] = res.get("verdict")  # PASS = đã index
    post["index_checked"] = datetime.now(VN).strftime("%Y-%m-%d %H:%M")
    return {"no": post["no"], "url": url, "verdict": res.get("verdict"), "coverage": res.get("coverageState"),
            "last_crawl": res.get("lastCrawlTime"), "google_canonical": res.get("googleCanonical"),
            **({} if res.get("verdict") == "PASS" else {"request_indexing": manual_link(prop, url)})}


if __name__ == "__main__":
    cmd = sys.argv[1]
    tok = token()
    if cmd == "sites":
        print(json.dumps(call("GET", f"{WEBMASTERS}/sites", bearer=tok), ensure_ascii=False, indent=1))
        sys.exit()
    prop = property_url(tok)
    if cmd == "submit":
        call("PUT", f"{WEBMASTERS}/sites/{quote(prop, safe='')}/sitemaps/{quote(SITEMAP, safe='')}", bearer=tok)
        info = call("GET", f"{WEBMASTERS}/sites/{quote(prop, safe='')}/sitemaps/{quote(SITEMAP, safe='')}", bearer=tok)
        print(json.dumps({"property": prop, "sitemap": SITEMAP, "lastSubmitted": info.get("lastSubmitted"),
                          "errors": info.get("errors"), "warnings": info.get("warnings")}, ensure_ascii=False, indent=1))
        sys.exit()
    data = load()
    if cmd == "inspect":
        out = inspect(data, find(data, int(sys.argv[2])), tok, prop)
        save(data)
        print(json.dumps(out, ensure_ascii=False, indent=1))
    elif cmd == "pending":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        cutoff = (datetime.now(VN) - timedelta(days=days)).strftime("%Y-%m-%d")
        oldest = (datetime.now(VN) - timedelta(days=30)).strftime("%Y-%m-%d")  # quá 30 ngày thì để báo cáo tháng xử lý
        out = [inspect(data, p, tok, prop) for p in data["posts"] if p["status"] == "published"
               and oldest <= p.get("published", "9999") <= cutoff and p.get("index_status") != "PASS"]
        save(data)
        print(json.dumps({"checked": len(out), "not_indexed": [o for o in out if o["verdict"] != "PASS"],
                          "indexed": [o["no"] for o in out if o["verdict"] == "PASS"]}, ensure_ascii=False, indent=1))
