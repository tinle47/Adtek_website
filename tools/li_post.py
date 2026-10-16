"""Đăng bài hằng ngày lên LinkedIn Page Adtek, cùng lịch với Facebook (danh sách "facebook" trong content/editorial/calendar.json).

Bản LinkedIn dùng chung id, date, time, link_post và approval với bản Facebook (anh Tin duyệt một lần cho cả hai kênh),
nội dung tiếng Anh nằm ở các trường riêng:
  li_title     tiêu đề câu hỏi tiếng Anh
  li_caption   caption tiếng Anh, viết lại cho LinkedIn từ caption Facebook, không link
  li_hashtags  3 hashtag tiếng Anh, không dấu, viết liền
  li_design    chữ trên ảnh tiếng Anh, cùng cấu trúc với design (python3 tools/social.py render <id> --lang en dựng ảnh)
  li_images    ảnh tiếng Anh content/linkedin/<id>/1.jpg, 2.jpg...; bài video dùng content/linkedin/<id>/video.mp4
  li_comment   (không bắt buộc) câu bình luận link, mặc định "Full article (in Vietnamese): <url>"
Script ghi: li_status (posted, cancelled), li_post_id, li_comment_id, li_posted_at, li_comment_error.
Bài Facebook bị hủy (status cancelled) thì bản LinkedIn cũng không đăng.

Caption đăng thật (template anh Tin chọn 16/10/2026: tiêu đề viết thường, không footer Website/Email, 3 hashtag):
  Tiêu đề
  Full article in the first comment.   (chỉ khi bài blog link_post đã lên sóng, Page sẽ bình luận link)
  caption
  3 hashtag

Dạng đăng: 1 ảnh thành bài ảnh; nhiều ảnh (Carousel hướng dẫn) ghép thành PDF, đăng dạng tài liệu lướt trang;
video.mp4 thành bài video.

Quyền truy cập: app LinkedIn có Community Management API, token của tài khoản admin Page, quyền w_organization_social
(đăng, bình luận, gỡ) và r_organization_admin (lệnh check). Proxy gắn token vào header Authorization khi gọi
api.linkedin.com và www.linkedin.com (network secret của môi trường, giống Facebook); nếu môi trường có biến
LINKEDIN_ACCESS_TOKEN thì script tự gắn. Token hết hạn sau 60 ngày: lỗi 401 nghĩa là cần cấp token mới.

Cách dùng:
  python3 tools/li_post.py check                   kiểm tra token: các Page tài khoản đang làm admin, ORG_ID có quyền đăng không
  python3 tools/li_post.py due                     bài đến giờ trong 24 giờ qua mà chưa đăng LinkedIn (JSON)
  python3 tools/li_post.py show <id>               caption đăng thật, bình luận, ảnh
  python3 tools/li_post.py publish <id> [--dry-run] [--late]
        đăng (cần approval approved hoặc auto, đủ nội dung tiếng Anh và ảnh). Bài trễ quá 24 giờ chỉ đăng khi có --late,
        để lúc mới gắn token không đăng dồn các bài cũ.
  python3 tools/li_post.py cancel <id>             không đăng bản LinkedIn của bài này (Facebook không đổi)
  python3 tools/li_post.py delete <id>             gỡ bài LinkedIn đã đăng (bình luận đi kèm bị gỡ theo)

Chạy lại "publish" an toàn: bài đã có li_post_id thì không đăng lại, chỉ bình luận bù nếu còn thiếu li_comment_id.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

from blog_post import ROOT, VN, load, save
from fb_daily import blog_link, item, label, when

API = "https://api.linkedin.com/rest"
VERSION = "202609"  # LinkedIn-Version (YYYYMM); mỗi bản dùng được khoảng 1 năm, hết hạn thì API báo lỗi version
ORG_ID = ""  # ID Page Adtek trên LinkedIn (số trong urn:li:organization:<id>), lấy từ lệnh check
POST_ROLES = ("ADMINISTRATOR", "CONTENT_ADMINISTRATOR")
CTA = "Full article in the first comment."
LATE = timedelta(hours=24)
MAX_CHARS = 3000  # giới hạn commentary của LinkedIn


def call(method, url, body=None, upload=None, ctype="application/octet-stream"):
    """Gọi LinkedIn bằng curl. Trả (mã HTTP, header viết thường, body JSON)."""
    if not url.startswith("http"):
        url = f"{API}/{url}"
    with tempfile.NamedTemporaryFile() as h:
        cmd = ["curl", "-sS", "--max-time", "600", "-X", method, url, "-D", h.name, "-w", "\n%{http_code}",
               "-H", f"LinkedIn-Version: {VERSION}", "-H", "X-Restli-Protocol-Version: 2.0.0"]
        if os.environ.get("LINKEDIN_ACCESS_TOKEN"):
            cmd += ["-H", f"Authorization: Bearer {os.environ['LINKEDIN_ACCESS_TOKEN']}"]
        if body is not None:
            cmd += ["-H", "Content-Type: application/json", "--data-binary", "@-"]
        if upload:
            cmd += ["-H", f"Content-Type: {ctype}", "--data-binary", f"@{upload}"]
        r = subprocess.run(cmd, input=json.dumps(body) if body is not None else None, capture_output=True, text=True)
        raw = Path(h.name).read_text(errors="replace")
    text, _, code = r.stdout.rpartition("\n")
    blocks = [b for b in raw.replace("\r\n", "\n").split("\n\n") if b.strip()]  # block cuối là response thật (sau CONNECT)
    headers = {}
    for line in blocks[-1].splitlines()[1:] if blocks else []:
        k, _, v = line.partition(":")
        headers[k.strip().lower()] = v.strip()
    try:
        data = json.loads(text) if text.strip() else {}
    except json.JSONDecodeError:
        data = {"message": (text or r.stderr)[:300]}
    return (int(code) if code.isdigit() else 0), headers, data


def fail(what, code, data):
    sys.exit(f"Lỗi {what} (HTTP {code}): {json.dumps(data, ensure_ascii=False)[:400]}")


def org():
    if not ORG_ID:
        sys.exit("Chưa điền ORG_ID (ID Page Adtek trên LinkedIn) trong tools/li_post.py: chạy check để xem ID")
    return f"urn:li:organization:{ORG_ID}"


def check():
    code, _, d = call("GET", "organizationAcls?q=roleAssignee&state=APPROVED&count=100")
    if code != 200:
        fail("kết nối LinkedIn API (token hết hạn, chưa gắn, hoặc thiếu quyền r_organization_admin)", code, d)
    pages = []
    for e in d.get("elements", []):
        c, _, o = call("GET", f"organizations/{e['organization'].rsplit(':', 1)[1]}")
        pages.append({"organization": e["organization"], "name": o.get("localizedName") if c == 200 else None,
                      "role": e["role"]})
    if not ORG_ID:
        sys.exit("Chưa điền ORG_ID trong tools/li_post.py. Tài khoản đang làm admin các Page: "
                 + json.dumps(pages, ensure_ascii=False))
    if not any(p["organization"] == org() and p["role"] in POST_ROLES for p in pages):
        sys.exit(f"Token không có quyền đăng cho Page {org()}: {json.dumps(pages, ensure_ascii=False)}")
    print(json.dumps({"organization": org(), "pages": pages}, ensure_ascii=False))


# ---------------------------------------------------------------- nội dung

RESERVED = set("\\|{}@[]()<>#*_~")


def little(text):
    """Commentary của LinkedIn theo little text format: ký tự đặc biệt phải thoát bằng \\, nếu không phần sau có thể bị cắt."""
    return "".join("\\" + c if c in RESERVED else c for c in text)


def tags(x):
    return [h.lstrip("#") for h in (x.get("li_hashtags") or [])][:3]


def message(x, with_cta, for_api=False):
    esc = little if for_api else str
    head = esc(x["li_title"].strip()) + ("\n" + esc(CTA) if with_cta else "")
    hashtags = " ".join("{hashtag|\\#|%s}" % t if for_api else "#" + t for t in tags(x))
    return "\n\n".join([head, esc(x["li_caption"].strip()), hashtags])


def comment(data, x, live_check=True):
    """Câu bình luận link nếu bài blog link_post đã lên sóng, ngược lại None."""
    link = blog_link(data, x, live_check)
    if not link:
        return None
    url = link[1]
    text = x.get("li_comment") or f"Full article (in Vietnamese): {url}"
    return text if url in text else f"{text} {url}"


def media(x):
    """Ảnh hoặc video tiếng Anh của bài, theo thứ tự đăng."""
    if x.get("li_images"):
        return [ROOT / p for p in x["li_images"]]
    folder = ROOT / f"content/linkedin/{x['id']}"
    if not folder.is_dir():
        return []
    files = [p for p in folder.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".mp4", ".mov")]
    return sorted(files, key=lambda p: (len(p.stem), p.stem))


def problems(x, files):
    out = []
    if not x.get("li_title") or not x.get("li_caption"):
        out.append("thiếu li_title hoặc li_caption tiếng Anh")
    elif any(s in x["li_caption"] + x["li_title"] for s in ("http", "adtek.agency")):
        out.append("caption LinkedIn có link")
    elif len(message(x, True, for_api=True)) > MAX_CHARS:
        out.append(f"caption LinkedIn dài quá {MAX_CHARS} ký tự")
    if len(tags(x)) < 3:
        out.append("thiếu 3 hashtag tiếng Anh (li_hashtags)")
    if not files:
        out.append(f"thiếu ảnh tiếng Anh content/linkedin/{x['id']}/ (python3 tools/social.py render {x['id']} --lang en)")
    elif any(not p.exists() for p in files):
        out.append("file ảnh không tồn tại: " + ", ".join(str(p.relative_to(ROOT)) for p in files if not p.exists()))
    return out


def summary(data, x, live_check=False):
    files = media(x)
    return {"id": x["id"], "when": label(x), "format": x["format"], "title": x.get("li_title") or x["title"],
            "li_status": x.get("li_status"), "approval": x.get("approval"),
            "media": [str(p.relative_to(ROOT)) for p in files], "comment": comment(data, x, live_check),
            "problems": problems(x, files)}


def due(data):
    now = datetime.now(VN)
    out = [summary(data, x, live_check=True) for x in data["facebook"]
           if x.get("li_status") not in ("posted", "cancelled") and x.get("status") != "cancelled"
           and now - LATE < when(x) <= now]
    print(json.dumps(out, ensure_ascii=False, indent=1))


def show(data, x):
    c = comment(data, x, live_check=False)
    print(message(x, with_cta=bool(c)) if x.get("li_caption") else "(chưa có caption LinkedIn)")
    print("\n---\nBình luận:", c or "(không bình luận)")
    print("Ảnh:", [str(p.relative_to(ROOT)) for p in media(x)])


# ---------------------------------------------------------------- tải ảnh, tài liệu, video

def wait(kind, urn, tries=60):
    """LinkedIn xử lý file sau khi tải lên; đăng khi trạng thái là AVAILABLE."""
    for _ in range(tries):
        code, _, d = call("GET", f"{kind}/{quote(urn, safe='')}")
        if code != 200:
            fail(f"kiểm tra {urn}", code, d)
        if d.get("status") == "AVAILABLE":
            return
        if d.get("status") == "PROCESSING_FAILED":
            fail(f"LinkedIn xử lý {urn}", code, d)
        time.sleep(5)
    sys.exit(f"LinkedIn xử lý {urn} quá 5 phút, chưa đăng")


def upload(kind, path, ctype="application/octet-stream"):
    """Ảnh (images) hoặc PDF (documents): xin link tải lên, PUT file, chờ xử lý xong. Trả URN."""
    code, _, d = call("POST", f"{kind}?action=initializeUpload", {"initializeUploadRequest": {"owner": org()}})
    if code != 200:
        fail(f"xin link tải {path.name}", code, d)
    v = d["value"]
    urn = v["image" if kind == "images" else "document"]
    code, _, d = call("PUT", v["uploadUrl"], upload=path, ctype=ctype)
    if code not in (200, 201):
        fail(f"tải {path.name}", code, d)
    wait(kind, urn)
    return urn


def upload_video(path):
    """Video tải theo từng phần LinkedIn chỉ định, ghép lại bằng ETag của từng phần."""
    code, _, d = call("POST", "videos?action=initializeUpload", {"initializeUploadRequest": {
        "owner": org(), "fileSizeBytes": path.stat().st_size, "uploadCaptions": False, "uploadThumbnail": False}})
    if code != 200:
        fail(f"xin link tải {path.name}", code, d)
    v, raw, etags = d["value"], path.read_bytes(), []
    with tempfile.TemporaryDirectory() as tmp:
        for i, part in enumerate(v["uploadInstructions"]):
            chunk = Path(tmp) / str(i)
            chunk.write_bytes(raw[part["firstByte"]:part["lastByte"] + 1])
            code, h, d = call("PUT", part["uploadUrl"], upload=chunk)
            if code not in (200, 201) or "etag" not in h:
                fail(f"tải phần {i + 1} của {path.name}", code, d)
            etags.append(h["etag"])
    code, _, d = call("POST", "videos?action=finalizeUpload", {"finalizeUploadRequest": {
        "video": v["video"], "uploadToken": v.get("uploadToken", ""), "uploadedPartIds": etags}})
    if code != 200:
        fail(f"hoàn tất tải {path.name}", code, d)
    wait("videos", v["video"])
    return v["video"]


def pdf(files, out):
    """Carousel ghép thành PDF nhiều trang để đăng dạng tài liệu lướt trang."""
    from PIL import Image
    pages = [Image.open(p).convert("RGB") for p in files]
    pages[0].save(out, save_all=True, append_images=pages[1:], quality=95)
    return out


def content(x, files):
    videos = [p for p in files if p.suffix.lower() in (".mp4", ".mov")]
    if videos:
        return {"media": {"id": upload_video(videos[0]), "title": x["li_title"]}}
    if len(files) == 1:
        return {"media": {"id": upload("images", files[0]), "altText": x["li_title"]}}
    with tempfile.TemporaryDirectory() as tmp:
        title = (x.get("li_design") or {}).get("title") or x["li_title"]
        return {"media": {"id": upload("documents", pdf(files, Path(tmp) / f"{x['id']}.pdf"), "application/pdf"),
                          "title": title}}


# ---------------------------------------------------------------- đăng, bình luận, gỡ

def add_comment(data, x, text):
    urn = x["li_post_id"]
    code, h, d = call("POST", f"socialActions/{quote(urn, safe='')}/comments",
                      {"actor": org(), "object": urn, "message": {"text": text}})
    if code != 201:
        x["li_comment_error"] = json.dumps(d, ensure_ascii=False)[:300]
        save(data)
        fail("bình luận link (bài đã đăng, chạy lại publish để bình luận bù)", code, d)
    x["li_comment_id"] = h.get("x-restli-id") or d.get("commentUrn") or d.get("id") or "ok"
    x.pop("li_comment_error", None)
    save(data)


def publish(data, x, dry_run=False, late=False):
    if x.get("li_status") == "cancelled" or x.get("status") == "cancelled":
        sys.exit(f"{x['id']}: đã hủy, không đăng LinkedIn")
    c = comment(data, x)
    if x.get("li_status") == "posted":
        if c and not x.get("li_comment_id") and not dry_run:
            check()
            add_comment(data, x, c)
            print(json.dumps({"id": x["id"], "li_post_id": x["li_post_id"], "li_comment_id": x["li_comment_id"]}))
            return
        sys.exit(f"{x['id']}: đã đăng LinkedIn ({x.get('li_post_id')}), không đăng lại")
    files = media(x)
    issues = problems(x, files)
    if issues:
        sys.exit(f"{x['id']}: chưa đăng LinkedIn: {'; '.join(issues)}")
    if x.get("approval") not in ("approved", "auto"):
        sys.exit(f"{x['id']}: chưa duyệt (approval = {x.get('approval')}), chưa đăng LinkedIn")
    if dry_run:
        print(json.dumps({"id": x["id"], "media": [str(p.relative_to(ROOT)) for p in files],
                          "message": message(x, with_cta=bool(c)), "commentary": message(x, bool(c), for_api=True),
                          "comment": c}, ensure_ascii=False, indent=1))
        return
    if datetime.now(VN) - when(x) > LATE and not late:
        sys.exit(f"{x['id']}: đã trễ quá 24 giờ so với giờ đăng {label(x)}, không tự đăng (thêm --late để vẫn đăng)")
    check()  # token phải có quyền đăng cho Page ORG_ID
    body = {"author": org(), "commentary": message(x, with_cta=bool(c), for_api=True), "visibility": "PUBLIC",
            "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
            "content": content(x, files), "lifecycleState": "PUBLISHED", "isReshareDisabledByAuthor": False}
    code, h, d = call("POST", "posts", body)
    urn = h.get("x-restli-id") or d.get("id")
    if code != 201 or not urn:
        fail("đăng bài LinkedIn", code, d)
    x.update({"li_post_id": urn, "li_status": "posted", "li_posted_at": datetime.now(VN).isoformat(timespec="seconds")})
    save(data)  # lưu ngay để lần chạy lại không đăng trùng
    if c:
        add_comment(data, x, c)
    print(json.dumps({"id": x["id"], "li_post_id": urn, "li_comment_id": x.get("li_comment_id"),
                      "url": f"https://www.linkedin.com/feed/update/{urn}/"}, ensure_ascii=False))


def delete(data, x):
    if not x.get("li_post_id"):
        sys.exit(f"{x['id']}: chưa đăng LinkedIn")
    code, _, d = call("DELETE", f"posts/{quote(x['li_post_id'], safe='')}")
    if code not in (200, 204):
        fail("gỡ bài LinkedIn", code, d)
    deleted = x["li_post_id"]
    for k in ("li_post_id", "li_comment_id", "li_posted_at", "li_status", "li_comment_error"):
        x.pop(k, None)
    save(data)
    print(json.dumps({"deleted": deleted}))


if __name__ == "__main__":
    cmd, args = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    if cmd == "check":
        check()
        sys.exit()
    data = load()
    if cmd == "due":
        due(data)
    elif cmd == "show":
        show(data, item(data, args[0]))
    elif cmd == "publish":
        publish(data, item(data, args[0]), dry_run="--dry-run" in sys.argv, late="--late" in sys.argv)
    elif cmd == "cancel":
        x = item(data, args[0])
        x["li_status"] = "cancelled"
        save(data)
        print(json.dumps({"cancelled": x["id"]}))
    elif cmd == "delete":
        delete(data, item(data, args[0]))
    else:
        sys.exit(__doc__)
