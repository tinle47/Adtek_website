"""Video TikTok theo danh sách "tiktok" trong content/editorial/calendar.json (3 video/tuần, lịch do phiên Adtek - Marketing lập).

Phương án B (anh Tin chọn 17/10/2026): script đẩy video vào hộp nháp (inbox) của tài khoản TikTok Adtek qua
Content Posting API, scope video.upload. Anh Tin bấm thông báo trong app TikTok, dán caption, bật nhãn "Nội dung do AI
tạo", rồi bấm Đăng. API inbox không nhận caption, nên script in caption để gửi anh Tin qua tin nhắn và push.
TikTok không duyệt Direct Post (đăng thẳng) cho công cụ chỉ đăng lên tài khoản của chính mình (Content Sharing Guidelines).

Mỗi mục tiktok có id (tt-YYYYMMDD), date, time, post (số bài blog), part (video thứ mấy của bài), angle, status.
Kịch bản: video/scripts/<slug bài blog>/<part>.json (id, caption, hashtags); video dựng ra: video/out/<id kịch bản>.mp4
(node tools/render.mjs <slug> <part> trong thư mục video, cần giọng đọc ở video/public/voice/<id>/).

status: planned -> inbox (đã vào hộp nháp, publish_id) -> posted (anh Tin đã bấm Đăng); cancelled; failed (lỗi xử lý).

Khóa TikTok đọc từ biến môi trường (network secret của môi trường), script không in token:
  TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET   ứng dụng trên developers.tiktok.com
  TIKTOK_REFRESH_TOKEN                      lấy một lần bằng lệnh auth, hạn 365 ngày
Mã truy cập (24 giờ) xin mới mỗi lần chạy. TikTok đổi refresh token thì script lưu bản mới vào REFRESH_FILE (ngoài repo)
và báo refresh_token_rotated: true để anh Tin cập nhật TIKTOK_REFRESH_TOKEN.

Cách dùng:
  python3 tools/tiktok_post.py auth                lấy refresh token (chạy trên máy anh Tin, không chạy trong phiên cloud)
  python3 tools/tiktok_post.py check               kiểm tra kết nối (chỉ đọc): token thuộc tài khoản TikTok nào
  python3 tools/tiktok_post.py due                 video đã đến giờ mà chưa đẩy vào hộp nháp (JSON)
  python3 tools/tiktok_post.py week <YYYY-MM-DD>   video trong 7 ngày từ ngày đó (JSON tóm tắt)
  python3 tools/tiktok_post.py show <id>           caption để dán, file video, việc còn thiếu
  python3 tools/tiktok_post.py upload <id> [--dry-run]   đẩy video vào hộp nháp TikTok
  python3 tools/tiktok_post.py status <id>         hỏi TikTok trạng thái; anh Tin đã bấm Đăng thì status = posted
  python3 tools/tiktok_post.py posted <id>         anh Tin báo đã đăng (khi status API chưa cập nhật)
  python3 tools/tiktok_post.py cancel <id>         anh Tin nhắn "hủy": không đẩy video này
"""
import json
import os
import secrets
import subprocess
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

from blog_post import ROOT, VN, find, load, save

API = "https://open.tiktokapis.com/v2"
AUTHORIZE = "https://www.tiktok.com/v2/auth/authorize/"
SCOPES = "user.info.basic,video.upload"
REDIRECT = os.environ.get("TIKTOK_REDIRECT_URI", "https://adtek.agency/")  # phải khai báo trong Login Kit của ứng dụng
REFRESH_FILE = Path.home() / ".config/adtek/tiktok_refresh_token"
VIDEO = ROOT / "video"
CHUNK = 10_000_000  # TikTok: mỗi phần 5 đến 64 MB, phần cuối gánh số byte dư (tối đa 128 MB); file đến 64 MB gửi một lần
PENDING_CAP = 5  # TikTok: tối đa 5 video chờ trong hộp nháp mỗi 24 giờ
DAYS = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]


def curl(args, data=None):
    r = subprocess.run(["curl", "-sS", "--max-time", "300", *args], input=data, capture_output=True)
    try:
        return json.loads(r.stdout or b"{}")
    except json.JSONDecodeError:
        return {"error": {"code": "bad_response", "message": (r.stdout or r.stderr)[:300].decode(errors="replace")}}


def fail(what, r):
    sys.exit(f"Lỗi {what}: {json.dumps(r.get('error', r), ensure_ascii=False)[:400]}")


def env(name):
    v = os.environ.get(name)
    if not v:
        sys.exit(f"Thiếu biến môi trường {name} (network secret của môi trường, xem đầu file)")
    return v


def oauth(form):
    form = {"client_key": env("TIKTOK_CLIENT_KEY"), "client_secret": env("TIKTOK_CLIENT_SECRET"), **form}
    return curl(["-X", "POST", f"{API}/oauth/token/", "-H", "Content-Type: application/x-www-form-urlencoded",
                 "--data-binary", "@-"], urllib.parse.urlencode(form).encode())


ROTATED = False


def token():
    """Mã truy cập mới từ refresh token. Bản đã lưu ở REFRESH_FILE (TikTok đổi token) được ưu tiên hơn biến môi trường."""
    global ROTATED
    old = REFRESH_FILE.read_text().strip() if REFRESH_FILE.exists() else env("TIKTOK_REFRESH_TOKEN")
    r = oauth({"grant_type": "refresh_token", "refresh_token": old})
    if "access_token" not in r:
        fail("xin mã truy cập (refresh token hết hạn hoặc bị thu hồi thì chạy lại lệnh auth)", r)
    if r.get("refresh_token") and r["refresh_token"] != old:
        REFRESH_FILE.parent.mkdir(parents=True, exist_ok=True)
        REFRESH_FILE.write_text(r["refresh_token"])
        REFRESH_FILE.chmod(0o600)
        ROTATED = True
    return r["access_token"]


def call(method, path, body=None, access=None):
    args = ["-X", method, f"{API}/{path}", "-H", f"Authorization: Bearer {access or token()}"]
    if body is None:
        return curl(args)
    return curl(args + ["-H", "Content-Type: application/json; charset=UTF-8", "--data-binary", "@-"],
                json.dumps(body).encode())


def ok(r):
    return (r.get("error") or {}).get("code") == "ok"


def auth():
    """Chạy trên máy anh Tin: mở link, bấm Cho phép, dán lại địa chỉ trang adtek.agency vừa mở ra (có ?code=...).
    Refresh token chỉ in ra máy anh Tin để lưu vào cài đặt môi trường, không gửi vào phiên chat."""
    state = secrets.token_urlsafe(16)
    q = {"client_key": env("TIKTOK_CLIENT_KEY"), "response_type": "code", "scope": SCOPES, "redirect_uri": REDIRECT,
         "state": state}
    print("1. Mở link này, đăng nhập TikTok Adtek, bấm Cho phép:\n\n" + AUTHORIZE + "?" + urllib.parse.urlencode(q))
    back = urllib.parse.parse_qs(urllib.parse.urlparse(input("\n2. Dán địa chỉ trang vừa mở ra: ").strip()).query)
    if back.get("state", [""])[0] != state:
        sys.exit("state không khớp, làm lại từ bước 1")
    if "code" not in back:
        sys.exit(f"TikTok không trả mã: {back.get('error_description', back)}")
    r = oauth({"grant_type": "authorization_code", "code": back["code"][0], "redirect_uri": REDIRECT})
    if "refresh_token" not in r:
        fail("đổi mã lấy token", r)
    if "video.upload" not in r.get("scope", ""):
        sys.exit(f"Tài khoản chưa cấp quyền video.upload (scope: {r.get('scope')})")
    print(f"\n3. Lưu giá trị sau vào biến TIKTOK_REFRESH_TOKEN trong cài đặt môi trường (hạn "
          f"{int(r.get('refresh_expires_in', 0)) // 86400} ngày):\n\n{r['refresh_token']}")


def check():
    r = call("GET", "user/info/?fields=open_id,display_name")
    if not ok(r):
        fail("kết nối TikTok", r)
    u = r["data"]["user"]
    print(json.dumps({"display_name": u.get("display_name"), "open_id": u.get("open_id"),
                      "refresh_token_rotated": ROTATED}, ensure_ascii=False))


def item(data, tid):
    try:
        return next(x for x in data["tiktok"] if x["id"] == tid)
    except StopIteration:
        sys.exit(f"Không có video {tid} trong danh sách tiktok")


def when(x):
    return datetime.fromisoformat(f"{x['date']}T{x['time']}:00").replace(tzinfo=VN)


def label(x):
    d = when(x)
    return f"{DAYS[d.weekday()]} {d.day}/{d.month}, {x['time']}"


def script(data, x):
    """(slug, kịch bản) của video, hoặc (slug, None) khi chưa có kịch bản."""
    slug = find(data, x["post"]).get("slug")
    path = VIDEO / f"scripts/{slug}/{x['part']}.json"
    return slug, (json.loads(path.read_text(encoding="utf-8")) if slug and path.exists() else None)


def mp4(s):
    return VIDEO / f"out/{s['id']}.mp4"


def caption(s):
    """Caption để anh Tin dán khi đăng: lời dẫn + hashtag, không link (TikTok không cho bấm, link để ở bio)."""
    return f"{s['caption'].strip()}\n\n{' '.join(s['hashtags'])}"


def problems(data, x):
    slug, s = script(data, x)
    if not slug:
        return [f"bài blog {x['post']} chưa có slug"]
    if not s:
        return [f"thiếu kịch bản video/scripts/{slug}/{x['part']}.json"]
    out = []
    if any(t in s.get("caption", "") for t in ("http", "adtek.agency")):
        out.append("caption có link")
    if not (VIDEO / f"public/voice/{s['id']}/manifest.json").exists():
        out.append(f"chưa có giọng đọc: cd video && node tools/voice.mjs {slug}")
    if not mp4(s).exists():
        out.append(f"chưa dựng video: cd video && node tools/render.mjs {slug} {x['part']}")
    return out


def summary(data, x):
    _, s = script(data, x)
    return {"id": x["id"], "when": label(x), "angle": x["angle"], "status": x.get("status"),
            "video": str(mp4(s).relative_to(ROOT)) if s else None, "caption": caption(s) if s else None,
            "problems": problems(data, x)}


def due(data):
    now = datetime.now(VN)
    out = [summary(data, x) for x in data["tiktok"] if x.get("status") in (None, "planned") and when(x) <= now]
    print(json.dumps(out, ensure_ascii=False, indent=1))


def week(data, start):
    d0 = datetime.fromisoformat(start).date()
    out = [summary(data, x) for x in data["tiktok"] if 0 <= (datetime.fromisoformat(x["date"]).date() - d0).days < 7]
    print(json.dumps(out, ensure_ascii=False, indent=1))


def show(data, x):
    s = summary(data, x)
    print(s["caption"] or "(chưa có kịch bản)")
    print("\n---\nVideo:", s["video"], "\nCần xử lý:", "; ".join(s["problems"]) or "không")


def chunks(size):
    """(chunk_size, total_chunk_count) theo quy tắc chia phần của TikTok."""
    return (size, 1) if size <= 64_000_000 else (CHUNK, size // CHUNK)


def upload(data, x, dry_run=False):
    if x.get("status") in ("inbox", "posted"):
        sys.exit(f"{x['id']}: đã vào hộp nháp ({x.get('publish_id')}), không đẩy lại")
    if x.get("status") == "cancelled":
        sys.exit(f"{x['id']}: anh Tin đã hủy, không đẩy")
    issues = problems(data, x)
    if issues:
        sys.exit(f"{x['id']}: chưa đẩy: {'; '.join(issues)}")
    _, s = script(data, x)
    path = mp4(s)
    size = path.stat().st_size
    chunk, count = chunks(size)
    if dry_run:
        print(json.dumps({"id": x["id"], "video": str(path.relative_to(ROOT)), "bytes": size, "chunk_size": chunk,
                          "chunks": count, "caption": caption(s)}, ensure_ascii=False, indent=1))
        return
    access = token()
    r = call("POST", "post/publish/inbox/video/init/", {"source_info": {
        "source": "FILE_UPLOAD", "video_size": size, "chunk_size": chunk, "total_chunk_count": count}}, access)
    if not ok(r):
        fail("khởi tạo tải video", r)
    publish_id, url = r["data"]["publish_id"], r["data"]["upload_url"]
    with path.open("rb") as f:
        for i in range(count):
            start = i * chunk
            part = f.read(size - start if i == count - 1 else chunk)  # phần cuối lấy hết số byte còn lại
            u = subprocess.run(["curl", "-sS", "--max-time", "300", "-o", "/dev/null", "-w", "%{http_code}", "-X", "PUT",
                                url, "-H", "Content-Type: video/mp4", "-H",
                                f"Content-Range: bytes {start}-{start + len(part) - 1}/{size}", "--data-binary", "@-"],
                               input=part, capture_output=True)
            if not u.stdout.startswith(b"2"):
                sys.exit(f"Lỗi tải phần {i + 1}/{count}: HTTP {u.stdout.decode()} {u.stderr.decode()[:200]}")
    x.update({"status": "inbox", "publish_id": publish_id, "uploaded_at": datetime.now(VN).isoformat(timespec="seconds")})
    save(data)  # lưu ngay để lần chạy lại không đẩy trùng
    st = call("POST", "post/publish/status/fetch/", {"publish_id": publish_id}, access)
    print(json.dumps({"id": x["id"], "publish_id": publish_id, "tiktok_status": (st.get("data") or {}).get("status"),
                      "caption": caption(s), "refresh_token_rotated": ROTATED}, ensure_ascii=False))


def status(data, x):
    if not x.get("publish_id"):
        sys.exit(f"{x['id']}: chưa đẩy vào hộp nháp")
    r = call("POST", "post/publish/status/fetch/", {"publish_id": x["publish_id"]})
    if not ok(r):
        fail("hỏi trạng thái", r)
    st = r["data"].get("status")
    if st == "PUBLISH_COMPLETE" and x.get("status") != "posted":
        x.update({"status": "posted", "posted_at": datetime.now(VN).isoformat(timespec="seconds")})
        ids = r["data"].get("publicaly_available_post_id") or []  # TikTok viết sai chính tả tên trường
        if ids:
            x["tiktok_post_id"] = str(ids[0])
    elif st == "FAILED":
        x.update({"status": "failed", "fail_reason": r["data"].get("fail_reason")})
    save(data)
    print(json.dumps({"id": x["id"], "tiktok_status": st, "status": x["status"], "fail_reason": x.get("fail_reason"),
                      "refresh_token_rotated": ROTATED}, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd, args = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    if cmd == "auth":
        auth()
        sys.exit()
    if cmd == "check":
        check()
        sys.exit()
    data = load()
    if cmd == "due":
        due(data)
    elif cmd == "week":
        week(data, args[0])
    elif cmd == "show":
        show(data, item(data, args[0]))
    elif cmd == "upload":
        upload(data, item(data, args[0]), dry_run="--dry-run" in sys.argv)
    elif cmd == "status":
        status(data, item(data, args[0]))
    elif cmd == "posted":
        x = item(data, args[0])
        x.update({"status": "posted", "posted_at": datetime.now(VN).isoformat(timespec="seconds")})
        save(data)
        print(json.dumps({"posted": x["id"]}))
    elif cmd == "cancel":
        x = item(data, args[0])
        x["status"] = "cancelled"
        save(data)
        print(json.dumps({"cancelled": x["id"]}))
    else:
        sys.exit(__doc__)
