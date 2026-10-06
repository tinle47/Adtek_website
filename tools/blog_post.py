"""Đưa bài trong content/editorial/calendar.json lên WordPress.

Mỗi bài trong calendar.json cần: slug, seo_title, meta_desc, cover {kicker, title, subtitle, chips},
và file nội dung content/posts/<slug>.html.

Cách dùng:
  python3 tools/blog_post.py cover <số bài>     tạo ảnh bìa content/posts/<slug>-cover.jpg
  python3 tools/blog_post.py draft <số bài>     tải ảnh bìa, tạo hoặc cập nhật bản nháp
  python3 tools/blog_post.py schedule <số bài>  đặt lịch đăng theo date/time (chỉ sau khi đã được duyệt)
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

from fix_alt import API, api

ROOT = Path(__file__).resolve().parent.parent
CAL = ROOT / "content/editorial/calendar.json"
AUTHOR = 4  # Tin Le
CATEGORIES = {"C3": [185, 184], "C4": [185], "C6": [185]}  # còn lại: Digital Marketing + Growth Marketing
COVER = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:630px;background:#002D72;font-family:Inter,sans-serif;color:#fff;overflow:hidden;position:relative}
.circle{position:absolute;left:796px;top:269px;width:628px;height:628px;border-radius:50%;background:#1F3A6B}
.left{position:absolute;left:80px;top:96px;width:720px}
.kicker{color:#FF9014;font-weight:700;font-size:24px;letter-spacing:3px;text-transform:uppercase}
h1{font-size:{size}px;line-height:1.08;margin:22px 0 28px;font-weight:800}
.sub{font-size:34px;line-height:1.4;color:#D6E2F5}
.brand{position:absolute;left:80px;bottom:88px;display:flex;align-items:center;gap:20px;font-weight:700;letter-spacing:6px;font-size:24px}
.brand i{display:block;width:120px;height:8px;border-radius:4px;background:#FF9014}
.chips{position:absolute;right:70px;top:120px;display:flex;flex-direction:column;gap:24px}
.chips span{width:222px;height:64px;border:2px solid #8FA3C4;border-radius:34px;display:flex;align-items:center;justify-content:center;font-size:25px}
.chips span:first-child{border-color:#FF9014;color:#FF9014}
</style></head><body><div class="circle"></div>
<div class="left"><div class="kicker">{kicker}</div><h1>{title}</h1><div class="sub">{subtitle}</div></div>
<div class="chips">{chips}</div><div class="brand"><i></i>ADTEK</div></body></html>"""


def load():
    return json.loads(CAL.read_text(encoding="utf-8"))


def save(data):
    CAL.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def find(data, no):
    return next(p for p in data["posts"] if p["no"] == no)


def cover(post):
    c = post["cover"]
    esc = html.escape
    page = (COVER.replace("{kicker}", esc(c["kicker"])).replace("{title}", esc(c["title"]))
            .replace("{subtitle}", esc(c["subtitle"])).replace("{size}", "88" if len(c["title"]) <= 18 else "64")
            .replace("{chips}", "".join(f"<span>{esc(x)}</span>" for x in c["chips"][:4])))
    src = ROOT / f"previews/cover-{post['slug']}.html"
    out = ROOT / f"content/posts/{post['slug']}-cover.jpg"
    src.write_text(page, encoding="utf-8")
    subprocess.run(["node", str(ROOT / "tools/render_cover.js"), str(src), str(out)], check=True)
    src.unlink()
    print(out)
    return out


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


def schedule(data, post):
    when = f"{post['date']}T{post['time']}:00"  # giờ Việt Nam (site đặt UTC+7)
    r = api("POST", f"posts/{post['wp_id']}?_fields=id,status,date,link", {"status": "future", "date": when})
    if r.get("status") not in ("future", "publish"):
        sys.exit(f"Lỗi: {str(r)[:300]}")
    post["status"] = "scheduled"
    save(data)
    print(f"Bài {post['no']}: {r['status']} lúc {r['date']}, {r['link']}")


if __name__ == "__main__":
    cmd, no = sys.argv[1], int(sys.argv[2])
    data = load()
    post = find(data, no)
    {"cover": lambda: cover(post), "draft": lambda: draft(data, post), "schedule": lambda: schedule(data, post)}[cmd]()
