"""Đưa bài trong content/editorial/calendar.json lên WordPress.

Mỗi bài trong calendar.json cần: slug, seo_title, meta_desc, cover {kicker, title, subtitle, hero, hero_text, fb_kicker},
và file nội dung content/posts/<slug>.html.

Cách dùng:
  python3 tools/blog_post.py cover <số bài>     tạo ảnh bìa content/posts/<slug>-cover.jpg (1200x630, phong cách ảnh Facebook)
  python3 tools/blog_post.py draft <số bài>     tải ảnh bìa, tạo hoặc cập nhật bản nháp
  python3 tools/blog_post.py recover <số bài> [--delete-old]  tải content/posts/<slug>-cover.jpg lên, thay ảnh đại diện trên WordPress (giữ nguyên trạng thái bài)
  python3 tools/blog_post.py schedule <số bài>  đặt lịch đăng theo date/time (anh Tin đã duyệt)
  python3 tools/blog_post.py changes <số bài>   anh Tin yêu cầu sửa: không tự đăng cho tới khi gửi duyệt lại
  python3 tools/blog_post.py unschedule <số bài> hủy lịch đăng, đưa bài về nháp
  python3 tools/blog_post.py retime             gán giờ đăng ngẫu nhiên cho các bài chưa đăng (khung 12:00-12:59 hoặc 20:00-20:59)
  python3 tools/blog_post.py auto               tự đặt lịch các bài đã gửi email quá 24 giờ mà chưa có phản hồi

Trạng thái duyệt (trường approval): pending (đã gửi email, ghi approval_requested), approved, auto, changes_requested.
"""
import json
import random
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fix_alt import API, api

ROOT = Path(__file__).resolve().parent.parent
CAL = ROOT / "content/editorial/calendar.json"
AUTHOR = 4  # Tin Le
CATEGORIES = {"C3": [185, 184], "C4": [185], "C6": [185]}  # còn lại: Digital Marketing + Growth Marketing


def load():
    return json.loads(CAL.read_text(encoding="utf-8"))


def save(data):
    CAL.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def find(data, no):
    return next(p for p in data["posts"] if p["no"] == no)


def cover(post):
    """Ảnh bìa blog 1200x630 cùng phong cách ảnh Facebook (fb_post.cover)."""
    from fb_post import cover as styled_cover  # fb_post import blog_post, nên import ở đây để tránh vòng lặp
    return styled_cover(post, (1200, 630), ROOT / f"content/posts/{post['slug']}-cover.jpg")


def upload(path, alt):
    r = subprocess.run(["curl", "-sS", "--max-time", "120", "-X", "POST", f"{API}/media",
                        "-H", f'Content-Disposition: attachment; filename="{path.name}"',
                        "-H", "Content-Type: image/jpeg", "--data-binary", f"@{path}"],
                       capture_output=True, text=True)
    media = json.loads(r.stdout)
    api("POST", f"media/{media['id']}?_fields=id", {"alt_text": alt})
    return media["id"]


def nofollow(content):
    """Link ra ngoài website: target _blank, rel nofollow noopener. Link nội bộ giữ nguyên."""
    def fix(m):
        tag = m.group(0)
        if re.search(r'href="https?://(www\.)?adtek\.agency', tag):
            return tag
        tag = re.sub(r'\s(rel|target)="[^"]*"', "", tag)
        return tag[:-1] + ' target="_blank" rel="nofollow noopener">'
    return re.sub(r'<a\s[^>]*href="https?://[^"]*"[^>]*>', fix, content)


def draft(data, post):
    path = ROOT / f"content/posts/{post['slug']}-cover.jpg"
    src = ROOT / f"content/posts/{post['slug']}.html"
    content = nofollow(src.read_text(encoding="utf-8"))
    src.write_text(content, encoding="utf-8")
    if not post.get("media_id"):
        post["media_id"] = upload(path if path.exists() else cover(post), post["title"])
    body = {
        "title": post["title"], "slug": post["slug"], "author": AUTHOR,
        "content": content,
        "categories": CATEGORIES.get(post["cluster"], [185, 143]), "featured_media": post["media_id"],
        "meta": {"_yoast_wpseo_title": post["seo_title"], "_yoast_wpseo_metadesc": post["meta_desc"]},
    }
    if not post.get("wp_id"):
        body["status"] = "draft"
    r = api("POST", f"posts/{post['wp_id']}" if post.get("wp_id") else "posts", body)
    if "id" not in r:
        sys.exit(f"Lỗi: {str(r)[:300]}")
    post["wp_id"] = r["id"]
    if post["status"] == "planned":
        post["status"] = "draft"
    save(data)
    print(f"Bài {post['no']}: post {r['id']} ({r['status']}), xem trước: https://adtek.agency/?p={r['id']}&preview=true")


def recover(data, post, delete_old=False):
    """Thay ảnh đại diện bằng content/posts/<slug>-cover.jpg (ảnh do phiên Adtek - Designer dựng; chưa có thì tự dựng).
    --delete-old: xóa hẳn ảnh cũ khỏi Media Library."""
    old = post.get("media_id")
    path = ROOT / f"content/posts/{post['slug']}-cover.jpg"
    new = upload(path if path.exists() else cover(post), post["title"])
    r = api("POST", f"posts/{post['wp_id']}?_fields=id,status,featured_media", {"featured_media": new})
    if r.get("featured_media") != new:  # cập nhật bài đã đăng có thể chạy xong nhưng proxy cắt phản hồi: đọc lại
        r = api("GET", f"posts/{post['wp_id']}?context=edit&_fields=id,status,featured_media")
    if r.get("featured_media") != new:
        sys.exit(f"Lỗi: {str(r)[:300]}")
    post["media_id"] = new
    save(data)
    if delete_old and old and old != new:
        d = api("DELETE", f"media/{old}?force=true")
        if not d.get("deleted"):
            print(f"Bài {post['no']}: chưa xóa được ảnh cũ {old}: {str(d)[:200]}")
    print(f"Bài {post['no']}: ảnh đại diện {old} -> {new} ({r['status']})")


VN = timezone(timedelta(hours=7))
APPROVAL_WINDOW = timedelta(hours=24)  # D+1 kể từ khi gửi email mà chưa duyệt thì tự đặt lịch
SLOTS = (12, 20)  # giờ đăng: ngẫu nhiên trong khung 12:00-12:59 hoặc 20:00-20:59, không cố định một mốc


def random_time():
    return f"{random.choice(SLOTS)}:{random.randint(1, 58):02d}"


def retime(data):
    for post in data["posts"]:
        if post["status"] in ("planned", "draft"):
            post["time"] = random_time()
            print(f"Bài {post['no']}: {post['date']} {post['time']}")
    save(data)


def schedule(data, post, approval="approved"):
    when = f"{post['date']}T{post['time']}:00"  # giờ Việt Nam (site đặt UTC+7)
    r = api("POST", f"posts/{post['wp_id']}?_fields=id,status,date,link", {"status": "future", "date": when})
    if r.get("status") not in ("future", "publish"):
        sys.exit(f"Lỗi: {str(r)[:300]}")
    post["status"] = "scheduled"
    post["approval"] = approval
    save(data)
    print(f"Bài {post['no']}: {r['status']} lúc {r['date']}, {r['link']}")


def changes(data, post):
    post["approval"] = "changes_requested"
    save(data)
    print(f"Bài {post['no']}: chờ sửa, không tự đăng")


def unschedule(data, post):
    r = api("POST", f"posts/{post['wp_id']}?_fields=id,status", {"status": "draft"})
    if r.get("status") != "draft":
        sys.exit(f"Lỗi: {str(r)[:300]}")
    post["status"] = "draft"
    post["approval"] = "changes_requested"
    save(data)
    print(f"Bài {post['no']}: đã hủy lịch, về nháp")


def auto(data):
    now = datetime.now(VN)
    done = []
    for post in data["posts"]:
        if post.get("approval") != "pending" or post.get("status") != "draft" or not post.get("approval_requested"):
            continue
        # trừ hao 5 phút vì lịch hẹn send_later làm tròn xuống theo phút
        if now - datetime.fromisoformat(post["approval_requested"]) >= APPROVAL_WINDOW - timedelta(minutes=5):
            schedule(data, post, approval="auto")
            done.append(post["no"])
    print(json.dumps({"auto_scheduled": done}))


if __name__ == "__main__":
    cmd = sys.argv[1]
    data = load()
    if cmd in ("auto", "retime"):
        {"auto": auto, "retime": retime}[cmd](data)
        sys.exit()
    post = find(data, int(sys.argv[2]))
    {"cover": lambda: cover(post), "draft": lambda: draft(data, post), "schedule": lambda: schedule(data, post),
     "changes": lambda: changes(data, post), "recover": lambda: recover(data, post, "--delete-old" in sys.argv), "unschedule": lambda: unschedule(data, post)}[cmd]()
