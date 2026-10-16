"""Đăng bài Facebook cho bài blog trong content/editorial/calendar.json.

Mỗi bài đăng dạng ảnh vuông 1:1 (content/posts/<slug>-fb.jpg, dựng bằng tools/covers.py từ cover.hero, cover.hero_text, cover.fb_kicker, cover.subtitle) kèm caption không có link.
Caption = câu CTA chung (CTA) + fb_caption; fb_caption không tự viết câu mời xem bài ở cuối.
Ngay sau đó Page tự bình luận fb_comment (tiêu đề ngắn + link bài blog) dưới bài.

Page access token do proxy gắn vào header Authorization khi gọi graph.facebook.com (network secret của môi
trường), script không đọc token. Trước khi đăng, script kiểm tra token đúng là của Page PAGE_ID.

Cách dùng:
  python3 tools/fb_post.py check                 kiểm tra kết nối (chỉ đọc): token thuộc Page nào
  python3 tools/fb_post.py cover <số bài>        dựng ảnh 4:5 content/posts/<slug>-fb.jpg (làm cùng lúc đưa nháp blog)
  python3 tools/fb_post.py post <số bài>         đăng ảnh + caption, rồi bình luận link (chỉ khi bài blog đã lên sóng)
  python3 tools/fb_post.py post <số bài> --dry-run   in nội dung sẽ gửi, không đăng
  python3 tools/fb_post.py post <số bài> --sample [--image <file>]   đăng bài mẫu để duyệt, không ghi vào calendar.json
  python3 tools/fb_post.py delete <số bài>       gỡ bài Facebook đã đăng (bình luận đi kèm bị gỡ theo), xóa fb_post_id
  python3 tools/fb_post.py delete --id <post_id> gỡ một bài theo ID, ví dụ bài mẫu

Chạy lại "post" an toàn: bài đã có fb_post_id thì không đăng lại, chỉ bình luận bù nếu còn thiếu fb_comment_id.
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from blog_post import ROOT, VN, find, load, save
from fix_alt import api

GRAPH = "https://graph.facebook.com/v23.0"
PAGE_ID = "101888089257566"  # Adtek Growth Agency
CTA = "Xem full bài viết ở bình luận bên dưới."
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


def cover(post, size=(1080, 1080), out=None):
    """Ảnh Facebook 1:1 (hoặc khổ ngang 1200x630 khi size rộng hơn cao) theo bộ mẫu tools/covers.py."""
    import covers
    return covers.make(post, "fb" if size[0] == size[1] else "blog", out)


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


def post_fb(data, post, dry_run=False, sample=False, image=None):
    image = Path(image) if image else ROOT / f"content/posts/{post['slug']}-fb.jpg"
    if not post.get("fb_caption") or not post.get("fb_comment"):
        sys.exit(f"Bài {post['no']}: thiếu fb_caption hoặc fb_comment")
    caption, comment = message(post), post["fb_comment"]
    if "http" in caption or "adtek.agency" in caption:
        sys.exit(f"Bài {post['no']}: caption có link, cần bỏ link khỏi caption")
    if not image.exists():
        image = cover(post)
    if dry_run:
        print(json.dumps({"image": str(image), "caption": caption, "comment": comment},
                         ensure_ascii=False, indent=1))
        return
    if sample:
        if not is_live(post):
            sys.exit(f"Bài {post['no']}: bài blog chưa lên sóng, chưa đăng Facebook")
        check()
        r = graph("POST", "me/photos", form_strings={"message": caption, "published": "true"}, files={"source": image})
        if "post_id" not in r:
            fail("đăng ảnh", r)
        c = graph("POST", f"{r['post_id']}/comments", form_strings={"message": comment})
        print(json.dumps({"sample": True, "no": post["no"], "fb_post_id": r["post_id"], "fb_comment_id": c.get("id"),
                          "comment_error": c.get("error"), "url": f"https://www.facebook.com/{r['post_id']}"},
                         ensure_ascii=False))
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


def delete(post_id, data=None, post=None):
    """Gỡ bài trên Page. Bình luận của bài bị gỡ theo."""
    r = graph("DELETE", post_id)
    if r.get("success") is not True:
        fail("gỡ bài", r)
    if post is not None:
        for k in ("fb_post_id", "fb_comment_id", "fb_posted"):
            post.pop(k, None)
        post["fb_status"] = "ready"
        save(data)
    print(json.dumps({"deleted": post_id}, ensure_ascii=False))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "check":
        check()
        sys.exit()
    data = load()
    if cmd == "delete" and sys.argv[2] == "--id":
        delete(sys.argv[3])
        sys.exit()
    post = find(data, int(sys.argv[2]))
    if cmd == "delete":
        if not post.get("fb_post_id"):
            sys.exit(f"Bài {post['no']}: chưa có bài Facebook để gỡ")
        delete(post["fb_post_id"], data, post)
    elif cmd == "cover":
        cover(post)
    else:
        img = sys.argv[sys.argv.index("--image") + 1] if "--image" in sys.argv else None
        post_fb(data, post, dry_run="--dry-run" in sys.argv, sample="--sample" in sys.argv, image=img)
