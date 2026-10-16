"""Đưa báo cáo trong content/reports/ lên mục Reports (https://adtek.agency/resources-report/).

Mỗi báo cáo cần: content/reports/<slug>.json, <slug>.pdf và <slug>-cover.jpg (dựng bằng tools/report_pdf.py).
Trường filters trong JSON: {"category_reports": "Việt Nam", "field_reports": "...", "year_reports": "2026"}
(tên bộ lọc hiện trên trang; chưa có thì tạo mới). Gắn bộ lọc cần mu-plugin adtek-reports-rest.php.

Cách dùng:
  python3 tools/report_wp.py draft <slug>     tải PDF và ảnh bìa, tạo hoặc cập nhật bản nháp, gắn file PDF và bộ lọc
  python3 tools/report_wp.py preview <slug>   link xem trước không cần đăng nhập (7 ngày), gửi anh Tin duyệt
  python3 tools/report_wp.py refresh <slug>   đã sửa nội dung: thay PDF, ảnh bìa và chữ trên bài (kể cả bài đã đăng)
  python3 tools/report_wp.py publish <slug>   đăng bản nháp (anh Tin đã duyệt) và xóa cache trang Reports
ID trên WordPress ghi lại vào trường wp của file JSON để lần chạy sau cập nhật đúng bài.
"""
import html
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

from fix_alt import API, api

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "content/reports"
AUTHOR = 4  # Tin Le
ACF = "https://adtek.agency/wp-json/adtek/v1/acf"
LIST_PAGE = "resources-report"
esc = html.escape


def upload(path, mime, alt=None):
    r = subprocess.run(["curl", "-sS", "--max-time", "180", "-X", "POST", f"{API}/media",
                        "-H", f'Content-Disposition: attachment; filename="{path.name}"',
                        "-H", f"Content-Type: {mime}", "--data-binary", f"@{path}"],
                       capture_output=True, text=True)
    media = json.loads(r.stdout)
    if "id" not in media:
        sys.exit(f"Tải {path.name} lỗi: {r.stdout[:300]}")
    if alt:
        api("POST", f"media/{media['id']}?_fields=id", {"alt_text": alt, "title": alt})
    return media["id"]


def acf(post_id, payload):
    r = subprocess.run(["curl", "-sS", "--max-time", "60", "-X", "POST", f"{ACF}/{post_id}",
                        "-H", "Content-Type: application/json; charset=utf-8", "--data-binary", "@-"],
                       input=json.dumps(payload, ensure_ascii=False), capture_output=True, text=True)
    return json.loads(r.stdout)


def term(tax, name):
    found = api("GET", f"{tax}?search={quote(name)}&per_page=100&_fields=id,name,slug")
    if not isinstance(found, list):
        sys.exit(f"Chưa đọc được bộ lọc {tax} qua REST: cần cài wordpress/mu-plugins/adtek-reports-rest.php ({found})")
    for t in found:
        if html.unescape(t["name"]).lower() == name.lower():
            return t["id"]
    t = api("POST", tax, {"name": name})
    if "id" not in t:
        sys.exit(f"Tạo bộ lọc {tax}/{name} lỗi: {t}")
    return t["id"]


def content(r):
    pubs = list(dict.fromkeys(s["publisher"] for s in r["sources"]))
    shown = ", ".join(pubs[:6]) + (" và các nguồn khác" if len(pubs) > 6 else "")
    return (f"<p>{esc(r['web_intro'])}</p>\n<p><strong>Bên trong báo cáo:</strong></p>\n<ul>\n"
            + "".join(f"<li>{esc(b)}</li>\n" for b in r["web_bullets"])
            + f"</ul>\n<p>Số liệu tổng hợp từ {esc(shown)}. {esc(r['period'])}.</p>")


def draft(slug):
    path = DIR / f"{slug}.json"
    r = json.loads(path.read_text(encoding="utf-8"))
    wp = r.setdefault("wp", {})
    terms = {tax: [term(tax, name)] for tax, name in r["filters"].items()}  # kiểm tra plugin trước khi tải file
    if not wp.get("pdf_id"):
        wp["pdf_id"] = upload(DIR / f"{slug}.pdf", "application/pdf", r["title"])
    if not wp.get("cover_id"):
        wp["cover_id"] = upload(DIR / f"{slug}-cover.jpg", "image/jpeg", r["title"])
    path.write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    body = {"title": r["title"], "slug": slug, "author": AUTHOR, "content": content(r), "excerpt": r["excerpt"],
            "featured_media": wp["cover_id"], "meta": {"_yoast_wpseo_metadesc": r["meta_desc"]}, **terms}
    if not wp.get("id"):
        # api() gửi lại khi phản hồi chậm hoặc bị cắt, nên lệnh tạo có thể đã chạy dù không nhận được kết quả:
        # tìm bài cùng slug trước khi tạo để không sinh bài trùng (WordPress sẽ đặt slug "-2" cho bài sau)
        found = api("GET", f"mona_reports?slug={slug}&status=draft,publish,pending,private&context=edit&_fields=id")
        if isinstance(found, list) and found:
            wp["id"] = found[0]["id"]
    if wp.get("id"):
        res = api("POST", f"mona_reports/{wp['id']}?_fields=id,status,link", body)
    else:
        res = api("POST", "mona_reports?_fields=id,status,link", {**body, "status": "draft"})
    if "id" not in res:
        sys.exit(f"Tạo bài lỗi: {res}")
    wp["id"] = res["id"]
    path.write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    f = acf(wp["id"], {"fields": {"mona_report_file": wp["pdf_id"]}})
    check = api("GET", f"mona_reports/{wp['id']}?context=edit&_fields=id,status,link,category_reports,field_reports,year_reports")
    print(json.dumps({"post": check, "acf": f.get("fields", f).get("mona_report_file") if isinstance(f, dict) else f},
                     ensure_ascii=False))


def preview(slug):
    """Plugin adtek-public-preview trả link ?p=<id>, nhưng với mona_reports link đó 404: phải thêm post_type."""
    r = json.loads((DIR / f"{slug}.json").read_text(encoding="utf-8"))
    out = subprocess.run(["curl", "-sS", "-X", "POST", f"https://adtek.agency/wp-json/adtek/v1/preview/{r['wp']['id']}?days=7"],
                         capture_output=True, text=True).stdout
    res = json.loads(out)
    print(res["url"].replace("/?p=", "/?post_type=mona_reports&p="), "hết hạn", res["expires"])


def refresh(slug):
    """Báo cáo đã sửa nội dung: tải PDF và ảnh bìa mới, cập nhật bài (giữ nguyên trạng thái), xóa ảnh bìa cũ.
    PDF cũ giữ lại để link trong email đã gửi cho người tải trước vẫn mở được."""
    path = DIR / f"{slug}.json"
    r = json.loads(path.read_text(encoding="utf-8"))
    old = {k: r["wp"].pop(k) for k in ("pdf_id", "cover_id")}
    r["wp"].setdefault("old_pdf_ids", []).append(old["pdf_id"])
    path.write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    draft(slug)
    api("DELETE", f"media/{old['cover_id']}?force=true")
    purge_list()


def purge_list():
    page = api("GET", f"pages?slug={LIST_PAGE}&_fields=id")
    if isinstance(page, list) and page:
        acf(page[0]["id"], {"purge": True})


def publish(slug):
    r = json.loads((DIR / f"{slug}.json").read_text(encoding="utf-8"))
    res = api("POST", f"mona_reports/{r['wp']['id']}?_fields=id,status,link", {"status": "publish"})
    purge_list()
    print(res)


if __name__ == "__main__":
    {"draft": draft, "preview": preview, "refresh": refresh, "publish": publish}[sys.argv[1]](sys.argv[2])
