"""Đăng bài Facebook cho bài blog trong content/editorial/calendar.json.

Mỗi bài đăng dạng ảnh dọc 4:5 (content/posts/<slug>-fb.jpg, dựng từ dữ liệu cover của bài) kèm caption không có link.
Caption = câu CTA chung (CTA) + fb_caption; fb_caption không tự viết câu mời xem bài ở cuối.
Ngay sau đó Page tự bình luận fb_comment (tiêu đề ngắn + link bài blog) dưới bài.

Page access token do proxy gắn vào header Authorization khi gọi graph.facebook.com (network secret của môi
trường), script không đọc token. Trước khi đăng, script kiểm tra token đúng là của Page PAGE_ID.

Cách dùng:
  python3 tools/fb_post.py check                 kiểm tra kết nối (chỉ đọc): token thuộc Page nào
  python3 tools/fb_post.py cover <số bài>        dựng ảnh 4:5 content/posts/<slug>-fb.jpg (làm cùng lúc đưa nháp blog)
  python3 tools/fb_post.py post <số bài>         đăng ảnh + caption, rồi bình luận link (chỉ khi bài blog đã lên sóng)
  python3 tools/fb_post.py post <số bài> --dry-run   in nội dung sẽ gửi, không đăng

Chạy lại "post" an toàn: bài đã có fb_post_id thì không đăng lại, chỉ bình luận bù nếu còn thiếu fb_comment_id.
"""
import html
import json
import subprocess
import sys
from datetime import datetime

from blog_post import ROOT, VN, find, load, save
from fix_alt import api

GRAPH = "https://graph.facebook.com/v23.0"
PAGE_ID = "101888089257566"  # Adtek Growth Agency
CTA = "Xem full bài viết ở bình luận bên dưới."
COVER = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1080px;height:1350px;background:#002D72;font-family:Inter,sans-serif;color:#fff;overflow:hidden;position:relative}
.circle{position:absolute;left:520px;top:880px;width:900px;height:900px;border-radius:50%;background:#1F3A6B}
.main{position:absolute;left:90px;top:60px;bottom:260px;width:900px;display:flex;flex-direction:column;justify-content:center}
.kicker{color:#FF9014;font-weight:700;font-size:34px;letter-spacing:4px;text-transform:uppercase}
h1{font-size:{size}px;line-height:1.06;margin:34px 0 40px;font-weight:800}
.sub{font-size:46px;line-height:1.4;color:#D6E2F5}
.chips{display:grid;grid-template-columns:repeat(2,420px);gap:28px;margin-top:72px}
.chips span{height:96px;border:2px solid #8FA3C4;border-radius:48px;display:flex;align-items:center;justify-content:center;font-size:34px}
.chips span:first-child{border-color:#FF9014;color:#FF9014}
.brand{position:absolute;left:90px;bottom:110px;display:flex;align-items:center;gap:24px;font-weight:700;letter-spacing:7px;font-size:30px}
.brand i{display:block;width:140px;height:10px;border-radius:5px;background:#FF9014}
</style></head><body><div class="circle"></div>
<div class="main"><div class="kicker">{kicker}</div><h1>{title}</h1><div class="sub">{subtitle}</div>
<div class="chips">{chips}</div></div><div class="brand"><i></i>ADTEK</div></body></html>"""


def graph(method, path, fields=None, form_strings=None, files=None):
    url = f"{GRAPH}/{path}" + (f"?fields={fields}" if fields else "")
    cmd = ["curl", "-sS", "--max-time", "120", "-X", method, url]
    for k, v in (form_strings or {}).items():
        cmd += ["--form-string", f"{k}={v}"]  # --form-string: không hiểu @ hay < trong caption là tên file
    for k, v in (files or {}).items():
        cmd += ["-F", f"{k}=@{v}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"error": {"message": (r.stdout or r.stderr)[:300]}}


def fail(what, r):
    sys.exit(f"Lỗi {what}: {json.dumps(r.get('error', r), ensure_ascii=False)[:400]}")


def check():
    r = graph("GET", "me", fields="id,name")
    if "id" not in r:
        fail("kết nối Graph API", r)
    if r["id"] != PAGE_ID:
        sys.exit(f"Token thuộc Page {r['name']} ({r['id']}), không phải Page {PAGE_ID}: không đăng")
    print(json.dumps({"page_id": r["id"], "page_name": r["name"]}, ensure_ascii=False))


def message(post):
    """Caption đăng thật: câu CTA chung ở đầu, rồi nội dung fb_caption."""
    return f"{CTA}\n\n{post['fb_caption'].strip()}"


def cover(post):
    """Ảnh dọc 4:5 cho Facebook, cùng nhận diện với ảnh bìa blog (tools/blog_post.py)."""
    c, esc = post["cover"], html.escape
    page = (COVER.replace("{kicker}", esc(c["kicker"])).replace("{title}", esc(c["title"]))
            .replace("{subtitle}", esc(c["subtitle"])).replace("{size}", "124" if len(c["title"]) <= 18 else "100")
            .replace("{chips}", "".join(f"<span>{esc(x)}</span>" for x in c["chips"][:4])))
    src = ROOT / f"previews/fb-{post['slug']}.html"
    out = ROOT / f"content/posts/{post['slug']}-fb.jpg"
    src.parent.mkdir(exist_ok=True)
    src.write_text(page, encoding="utf-8")
    subprocess.run(["node", str(ROOT / "tools/render_cover.js"), str(src), str(out), "1080", "1350"], check=True)
    src.unlink()
    print(out)
    return out


def is_live(post):
    """Bài blog đã đăng thật: WordPress báo publish và URL công khai trả về 200."""
    if not post.get("wp_id"):
        return False
    wp = api("GET", f"posts/{post['wp_id']}?_fields=status,link")
    if wp.get("status") != "publish":
        return False
    code = subprocess.run(["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "60", wp["link"]],
                          capture_output=True, text=True).stdout
    return code == "200"


def post_fb(data, post, dry_run=False):
    image = ROOT / f"content/posts/{post['slug']}-fb.jpg"
    if not post.get("fb_caption") or not post.get("fb_comment"):
        sys.exit(f"Bài {post['no']}: thiếu fb_caption hoặc fb_comment")
    caption, comment = message(post), post["fb_comment"]
    if "http" in caption or "adtek.agency" in caption:
        sys.exit(f"Bài {post['no']}: caption có link, cần bỏ link khỏi caption")
    if not image.exists():
        image = cover(post)
    if dry_run:
        print(json.dumps({"image": str(image.relative_to(ROOT)), "caption": caption, "comment": comment},
                         ensure_ascii=False, indent=1))
        return
    if not post.get("fb_post_id"):
        if not is_live(post):
            sys.exit(f"Bài {post['no']}: bài blog chưa lên sóng, chưa đăng Facebook")
        check()  # token phải đúng Page PAGE_ID
        r = graph("POST", "me/photos", form_strings={"message": caption, "published": "true"},
                  files={"source": image})
        if "post_id" not in r:
            fail("đăng ảnh", r)
        post["fb_post_id"] = r["post_id"]
        post["fb_posted"] = datetime.now(VN).isoformat(timespec="seconds")
        post["fb_status"] = "posted"
        save(data)  # lưu ngay để lần chạy lại không đăng trùng
    if not post.get("fb_comment_id"):
        r = graph("POST", f"{post['fb_post_id']}/comments", form_strings={"message": comment})
        if "id" not in r:
            post["fb_status"] = "comment_failed"
            save(data)
            fail("bình luận link (chạy lại lệnh post để bình luận bù)", r)
        post["fb_comment_id"] = r["id"]
        post["fb_status"] = "posted"
        save(data)
    print(json.dumps({"no": post["no"], "fb_post_id": post["fb_post_id"], "fb_comment_id": post["fb_comment_id"],
                      "url": f"https://www.facebook.com/{post['fb_post_id']}"}, ensure_ascii=False))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "check":
        check()
        sys.exit()
    data = load()
    post = find(data, int(sys.argv[2]))
    if cmd == "cover":
        cover(post)
    else:
        post_fb(data, post, dry_run="--dry-run" in sys.argv)
