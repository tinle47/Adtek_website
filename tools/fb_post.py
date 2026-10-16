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
  python3 tools/fb_post.py post <số bài> --sample [--image <file>]   đăng bài mẫu để duyệt, không ghi vào calendar.json
  python3 tools/fb_post.py delete <số bài>       gỡ bài Facebook đã đăng (bình luận đi kèm bị gỡ theo), xóa fb_post_id
  python3 tools/fb_post.py delete --id <post_id> gỡ một bài theo ID, ví dụ bài mẫu

Chạy lại "post" an toàn: bài đã có fb_post_id thì không đăng lại, chỉ bình luận bù nếu còn thiếu fb_comment_id.
"""
import html
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
ASSETS = ROOT / "tools/assets"
COVER = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:BVP;font-weight:600;src:url(FONTS/be-vietnam-pro-vietnamese-600-normal.woff2),url(FONTS/be-vietnam-pro-latin-600-normal.woff2)}
@font-face{font-family:BVP;font-weight:700;src:url(FONTS/be-vietnam-pro-vietnamese-700-normal.woff2),url(FONTS/be-vietnam-pro-latin-700-normal.woff2)}
@font-face{font-family:BVP;font-weight:800;src:url(FONTS/be-vietnam-pro-vietnamese-800-normal.woff2),url(FONTS/be-vietnam-pro-latin-800-normal.woff2)}
@font-face{font-family:BVP;font-weight:900;src:url(FONTS/be-vietnam-pro-vietnamese-900-normal.woff2),url(FONTS/be-vietnam-pro-latin-900-normal.woff2)}
*{box-sizing:border-box}
body{margin:0;width:{w}px;height:{h}px;overflow:hidden;position:relative;font-family:BVP,Inter,sans-serif;color:#fff;
background:radial-gradient(ellipse 70% 38% at 50% 0%,rgba(255,255,255,.38),transparent 70%),
linear-gradient(180deg,#A9ABF6 0%,#8384DA 34%,#4A4CA3 66%,#1E2056 100%)}
.grid{position:absolute;left:0;right:0;bottom:0;height:38%;opacity:.4}
.horizon{position:absolute;left:8%;right:8%;bottom:38%;height:2px;background:linear-gradient(90deg,transparent,rgba(170,215,255,.9),transparent);filter:blur(1px)}
.wrap{position:absolute;inset:{pad}px 80px {padb}px;display:flex;flex-direction:column;align-items:center}
.logo{height:{logo}px}
.body{flex:1;width:100%;display:flex;flex-direction:column;justify-content:center;gap:{gapbox}px;padding-bottom:{bodyb}px}
.main{width:100%;display:flex;align-items:center;justify-content:center;gap:44px}
.stack .main{flex-direction:column;gap:16px}
.side .text{text-align:left;flex:1}.stack .text{text-align:center}
.kicker{color:#D3E7FF;font-weight:800;font-size:{kick}px;letter-spacing:3px;text-transform:uppercase}
.hero{position:relative;flex:none;font-weight:900;font-size:{hero}px;line-height:.9;letter-spacing:-4px;
background:linear-gradient(165deg,#FFFFFF 8%,#F6DCF2 38%,#CDB8F2 62%,#8F8CE4 88%);-webkit-background-clip:text;background-clip:text;color:transparent;
filter:drop-shadow(1px 1px 0 #6F6FC8) drop-shadow(2px 2px 0 #5E5EB6) drop-shadow(3px 3px 0 #5052A4) drop-shadow(4px 4px 0 #444694)
drop-shadow(5px 6px 0 #3A3C85) drop-shadow(0 18px 26px rgba(10,12,50,.55)) drop-shadow(0 0 30px rgba(140,205,255,.45))}
.title{margin-top:12px;font-weight:900;font-size:{tsize}px;line-height:1.14;text-transform:uppercase;text-shadow:0 4px 18px rgba(20,20,70,.45)}
.box{width:100%;border:2px solid rgba(255,255,255,.9);border-radius:30px;padding:30px 38px;background:rgba(255,255,255,.12);
font-weight:700;font-size:{sub}px;line-height:1.38;text-align:left;text-shadow:0 2px 10px rgba(20,20,70,.4)}
</style></head><body>
<svg class="grid" viewBox="0 0 1000 500" preserveAspectRatio="none" fill="none" stroke="#9FD4FF" stroke-width="1.4">
{gridlines}
<path d="M120 380 h160 a18 18 0 0 0 18 -18 v-40 h120 M880 420 h-150 a18 18 0 0 1 -18 -18 v-30 h-110 M60 470 h300 M640 470 h300" stroke-opacity=".7"/>
<rect x="330" y="400" width="340" height="70" rx="16" stroke-opacity=".5"/>
</svg><div class="horizon"></div>
<div class="wrap {layout}"><img class="logo" src="LOGO"><div class="body"><div class="main"><div class="hero">{herotext}</div>
<div class="text"><div class="kicker">{kicker}</div><div class="title">{title}</div></div></div>
<div class="box">{subtitle}</div></div></div></body></html>"""



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


def grid_lines():
    """Lưới phối cảnh kiểu sàn công nghệ ở nửa dưới ảnh."""
    lines = [f'<path d="M0 {y:.0f} H1000" stroke-opacity="{0.15 + y / 900:.2f}"/>' for y in (20, 55, 100, 160, 240, 340, 470)]
    lines += [f'<path d="M500 0 L{x} 500" stroke-opacity=".35"/>' for x in range(-900, 1901, 200)]
    return "".join(lines)


def cover(post, size=(1080, 1350)):
    """Ảnh Facebook theo nhận diện bài đăng của Adtek: nền tím xanh, lưới công nghệ, chữ 3D lớn, khung mô tả bo góc."""
    c, esc = post["cover"], html.escape
    w, h = size
    # Số lớn và dòng chữ cạnh nó phải đọc liền thành một câu ("30" + "ngày chuẩn bị 11.11"), như mẫu "5 xu hướng marketing".
    hero = c.get("hero") or c["title"].split()[-1]
    title = c.get("hero_text") or c["title"]
    square = w == h
    side = len(hero) <= 2  # số hoặc chữ ngắn: đặt bên trái, chữ bên phải như mẫu "5 xu hướng"
    k = 0.88 if square else 1
    vals = {"w": w, "h": h, "pad": 64 if square else 80, "padb": 64 if square else 90, "logo": 104 if square else 116,
            "kick": round(34 * k), "sub": round(38 * k),
            "tsize": round((86 if len(title) <= 16 else 76 if len(title) <= 28 else 68) * k),
            "gapbox": 56, "bodyb": 40 if square else 60, "hero": round(((380 if len(hero) == 1 else 310) if side else 250 if len(hero) <= 4 else 190) * k), "layout": "side" if side else "stack"}
    page = COVER.replace("FONTS", (ASSETS / "fonts").as_uri()).replace("LOGO", (ASSETS / "adtek-logo-white.png").as_uri())
    for k, v in vals.items():
        page = page.replace("{" + k + "}", f"{v:g}" if isinstance(v, float) else str(v))
    page = (page.replace("{gridlines}", grid_lines()).replace("{kicker}", esc(c["kicker"]))
            .replace("{herotext}", esc(hero)).replace("{title}", esc(title)).replace("{subtitle}", esc(c["subtitle"])))
    src = ROOT / f"previews/fb-{post['slug']}.html"
    out = ROOT / f"content/posts/{post['slug']}-fb.jpg"
    src.parent.mkdir(exist_ok=True)
    src.write_text(page, encoding="utf-8")
    subprocess.run(["node", str(ROOT / "tools/render_cover.js"), str(src), str(out), str(w), str(h)], check=True)
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
