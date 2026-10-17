"""Video TikTok theo danh sách "tiktok" trong content/editorial/calendar.json (3 video/tuần, lịch do phiên Adtek - Marketing lập).

Đăng qua Zernio (zernio.com, anh Tin chọn 17/10/2026): script tải video lên Zernio và hẹn giờ đăng công khai đúng date,
time của video (giờ Việt Nam); đến giờ Zernio đăng lên TikTok Adtek, có nhãn "Nội dung do AI tạo" (giọng đọc nhân bản).
Hủy trước giờ đăng thì script xóa lịch trên Zernio. TikTok không duyệt Direct Post cho công cụ chỉ đăng lên tài khoản
của chính mình (Content Sharing Guidelines), Zernio là đơn vị đã được TikTok duyệt.
Dự phòng (phương án B): lệnh upload đẩy video vào hộp nháp TikTok bằng ứng dụng TikTok riêng của Adtek, anh Tin tự bấm Đăng.

Mỗi mục tiktok có id (tt-YYYYMMDD), date, time, post (số bài blog), part (video thứ mấy của bài), angle, status.
Kịch bản: video/scripts/<slug bài blog>/<part>.json (id, caption, hashtags); video dựng ra: video/out/<id kịch bản>.mp4
(node tools/render.mjs <slug> <part> trong thư mục video, cần giọng đọc ở video/public/voice/<id>/).

status: planned -> scheduled (đã hẹn trên Zernio, zernio_post_id) -> posted (tiktok_url); cancelled; failed (fail_reason).
Phương án B: planned -> inbox (publish_id) -> posted.

Khóa đọc từ biến môi trường (network secret của môi trường), script không in khóa:
  ZERNIO_API_KEY                            API key trong trang quản trị Zernio
  ZERNIO_TIKTOK_ACCOUNT_ID                  không bắt buộc; bỏ trống thì dùng tài khoản TikTok duy nhất đã kết nối
  TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_REFRESH_TOKEN   chỉ cho phương án B (lệnh auth, upload, inbox-status)

Cách dùng:
  python3 tools/tiktok_post.py check               kiểm tra kết nối Zernio (chỉ đọc): tài khoản TikTok, quyền riêng tư, còn đăng được không
  python3 tools/tiktok_post.py week <YYYY-MM-DD>   video trong 7 ngày từ ngày đó (JSON tóm tắt)
  python3 tools/tiktok_post.py show <id>           caption đăng thật, file video, việc còn thiếu
  python3 tools/tiktok_post.py schedule <id> [--dry-run]   tải video lên Zernio, hẹn đăng đúng date, time
  python3 tools/tiktok_post.py status <id>         hỏi Zernio: đã đăng thì status = posted, ghi tiktok_url; lỗi thì failed
  python3 tools/tiktok_post.py cancel <id>         anh Tin nhắn "hủy": xóa lịch trên Zernio (nếu có), status = cancelled
  python3 tools/tiktok_post.py due                 video đã qua giờ đăng mà chưa hẹn hay đăng (JSON)
Phương án B:
  python3 tools/tiktok_post.py auth                lấy refresh token (chạy trên máy anh Tin, không chạy trong phiên cloud)
  python3 tools/tiktok_post.py upload <id> [--dry-run]   đẩy video vào hộp nháp TikTok
  python3 tools/tiktok_post.py inbox-status <id>   hỏi TikTok trạng thái video trong hộp nháp
  python3 tools/tiktok_post.py posted <id>         anh Tin báo đã đăng từ hộp nháp
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
ZERNIO = "https://zernio.com/api/v1"
# Cài đặt đăng mặc định (anh Tin đổi được): công khai, cho bình luận, Duet, Stitch; gắn nhãn AI vì giọng đọc nhân bản;
# không bật nhãn quảng cáo (commercialContentType "brand_organic" sẽ gắn nhãn "Promotional content").
TIKTOK_SETTINGS = {"privacyLevel": "PUBLIC_TO_EVERYONE", "allowComment": True, "allowDuet": True, "allowStitch": True,
                   "videoMadeWithAi": True, "commercialContentType": "none",
                   # anh Tin duyệt qua email báo trước và được hủy đến giờ đăng (routines/tiktok.md)
                   "contentPreviewConfirmed": True, "expressConsentGiven": True}
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


def inbox_status(data, x):
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


def zapi(method, path, body=None, headers=()):
    """(mã HTTP, JSON) từ Zernio API."""
    args = ["-X", method, f"{ZERNIO}/{path}", "-H", f"Authorization: Bearer {env('ZERNIO_API_KEY')}", "-w", "\n%{http_code}"]
    for h in headers:
        args += ["-H", h]
    data = None
    if body is not None:
        args += ["-H", "Content-Type: application/json", "--data-binary", "@-"]
        data = json.dumps(body, ensure_ascii=False).encode()
    r = subprocess.run(["curl", "-sS", "--max-time", "300", *args], input=data, capture_output=True)
    text, _, code = r.stdout.decode(errors="replace").rpartition("\n")
    try:
        return int(code), json.loads(text or "{}")
    except (ValueError, json.JSONDecodeError):
        return 0, {"error": (text or r.stderr.decode(errors="replace"))[:300]}


def zfail(what, code, r):
    sys.exit(f"Lỗi {what} (HTTP {code}): {json.dumps(r, ensure_ascii=False)[:400]}")


def account():
    """ID tài khoản TikTok trên Zernio: ZERNIO_TIKTOK_ACCOUNT_ID, hoặc tài khoản TikTok duy nhất đã kết nối."""
    if os.environ.get("ZERNIO_TIKTOK_ACCOUNT_ID"):
        return os.environ["ZERNIO_TIKTOK_ACCOUNT_ID"]
    code, r = zapi("GET", "accounts?platform=tiktok")
    if code != 200:
        zfail("đọc danh sách tài khoản Zernio", code, r)
    tiktok = [a for a in r.get("accounts", []) if a.get("platform") == "tiktok" and a.get("isActive", True)]
    if len(tiktok) != 1:
        sys.exit(f"Zernio có {len(tiktok)} tài khoản TikTok, cần đúng 1 (hoặc đặt ZERNIO_TIKTOK_ACCOUNT_ID): "
                 + ", ".join(f"{a['_id']} {a.get('username') or a.get('displayName')}" for a in tiktok))
    return tiktok[0]["_id"]


def creator(acc):
    code, r = zapi("GET", f"accounts/{acc}/tiktok/creator-info?mediaType=video")
    if code != 200:
        zfail("đọc thông tin tài khoản TikTok", code, r)
    return r


def check():
    acc = account()
    c = creator(acc)
    print(json.dumps({"account_id": acc, "nickname": c.get("creator", {}).get("nickname"),
                      "can_post_more": c.get("creator", {}).get("canPostMore"),
                      "privacy_levels": [p.get("value") for p in c.get("privacyLevels", [])],
                      "max_video_sec": c.get("postingLimits", {}).get("maxVideoDurationSec")}, ensure_ascii=False))


def settings(c):
    """TIKTOK_SETTINGS, tắt tương tác nào tài khoản đã tắt trong app; dừng nếu không đăng được công khai."""
    levels = [p.get("value") for p in c.get("privacyLevels", [])]
    if TIKTOK_SETTINGS["privacyLevel"] not in levels:
        sys.exit(f"Tài khoản TikTok không đăng được {TIKTOK_SETTINGS['privacyLevel']} (chỉ có {levels}): "
                 "chuyển tài khoản sang công khai")
    out = dict(TIKTOK_SETTINGS)
    for k, field in (("allow_comment", "allowComment"), ("allow_duet", "allowDuet"), ("allow_stitch", "allowStitch")):
        d = (c.get("postingLimits", {}).get("interactionSettings") or {}).get(k) or {}
        if d.get("enabled") is False:
            out[field] = False
    return out


def schedule(data, x, dry_run=False):
    if x.get("status") in ("scheduled", "inbox", "posted"):
        sys.exit(f"{x['id']}: đã hẹn hoặc đã đăng ({x.get('zernio_post_id') or x.get('publish_id')}), không hẹn lại")
    if x.get("status") == "cancelled":
        sys.exit(f"{x['id']}: anh Tin đã hủy, không đăng")
    issues = problems(data, x)
    if issues:
        sys.exit(f"{x['id']}: chưa hẹn: {'; '.join(issues)}")
    _, s = script(data, x)
    path = mp4(s)
    body = {"content": caption(s), "platforms": [{"platform": "tiktok", "accountId": None}],
            "scheduledFor": when(x).isoformat(), "timezone": "Asia/Ho_Chi_Minh", "tiktokSettings": dict(TIKTOK_SETTINGS),
            "mediaItems": [{"type": "video", "url": None}], "metadata": {"calendar_id": x["id"], "script": s["id"]}}
    if dry_run:
        print(json.dumps({"id": x["id"], "video": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "post": body},
                         ensure_ascii=False, indent=1))
        return
    acc = account()
    c = creator(acc)
    if c.get("creator", {}).get("canPostMore") is False:
        sys.exit(f"{x['id']}: TikTok báo tài khoản tạm thời không đăng thêm được, thử lại sau")
    body["platforms"][0]["accountId"] = acc
    body["tiktokSettings"] = settings(c)
    code, r = zapi("POST", "media/presign", {"filename": path.name, "contentType": "video/mp4", "size": path.stat().st_size})
    if code != 200 or "uploadUrl" not in r:
        zfail("xin link tải video", code, r)
    u = subprocess.run(["curl", "-sS", "--max-time", "600", "-o", "/dev/null", "-w", "%{http_code}", "-X", "PUT",
                        r["uploadUrl"], "-H", "Content-Type: video/mp4", "--data-binary", f"@{path}"], capture_output=True)
    if not u.stdout.startswith(b"2"):  # link lưu trữ, không gửi Authorization
        sys.exit(f"Lỗi tải video lên Zernio: HTTP {u.stdout.decode()} {u.stderr.decode()[:200]}")
    body["mediaItems"][0]["url"] = r["publicUrl"]
    # cùng khóa trong 24 giờ thì Zernio trả lại bài cũ, chạy lại sau lỗi mạng không tạo bài trùng
    code, r = zapi("POST", "posts", body, [f"Idempotency-Key: adtek-{x['id']}-{x.get('attempt', 0)}"])
    post = r.get("post") or {}
    if code not in (200, 201) or not post.get("_id") or post.get("status") == "failed":
        zfail("hẹn đăng trên Zernio", code, r)
    x.update({"status": "scheduled", "zernio_post_id": post["_id"],
              "scheduled_at": datetime.now(VN).isoformat(timespec="seconds")})
    save(data)
    print(json.dumps({"id": x["id"], "zernio_post_id": post["_id"], "zernio_status": post.get("status"),
                      "when": label(x), "caption": body["content"]}, ensure_ascii=False))


def status(data, x):
    if not x.get("zernio_post_id"):
        sys.exit(f"{x['id']}: chưa hẹn trên Zernio")
    code, r = zapi("GET", f"posts/{x['zernio_post_id']}")
    if code != 200:
        zfail("hỏi trạng thái", code, r)
    post = r.get("post") or {}
    p = next((e for e in post.get("platforms", []) if e.get("platform") == "tiktok"), {})
    if p.get("status") == "published" and x.get("status") != "posted":
        x.update({"status": "posted", "posted_at": p.get("publishedAt") or datetime.now(VN).isoformat(timespec="seconds")})
    if p.get("platformPostUrl"):
        x["tiktok_url"] = p["platformPostUrl"]  # TikTok có thể mất vài phút mới trả link
    if p.get("status") == "failed" or post.get("status") == "failed":
        x.update({"status": "failed", "fail_reason": p.get("errorMessage")})
    save(data)
    print(json.dumps({"id": x["id"], "zernio_status": post.get("status"), "tiktok_status": p.get("status"),
                      "status": x["status"], "tiktok_url": x.get("tiktok_url"), "fail_reason": x.get("fail_reason")},
                     ensure_ascii=False))


def cancel(data, x):
    if x.get("status") == "posted":
        sys.exit(f"{x['id']}: đã đăng lên TikTok, không hủy được bằng lệnh này")
    if x.get("zernio_post_id") and x.get("status") == "scheduled":
        code, r = zapi("DELETE", f"posts/{x['zernio_post_id']}")
        if code not in (200, 204):
            zfail("xóa lịch trên Zernio", code, r)
    x.update({"status": "cancelled", "zernio_post_id": None, "attempt": x.get("attempt", 0) + 1})
    save(data)
    print(json.dumps({"cancelled": x["id"]}))


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
    elif cmd == "schedule":
        schedule(data, item(data, args[0]), dry_run="--dry-run" in sys.argv)
    elif cmd == "status":
        status(data, item(data, args[0]))
    elif cmd == "cancel":
        cancel(data, item(data, args[0]))
    elif cmd == "upload":
        upload(data, item(data, args[0]), dry_run="--dry-run" in sys.argv)
    elif cmd == "inbox-status":
        inbox_status(data, item(data, args[0]))
    elif cmd == "posted":
        x = item(data, args[0])
        x.update({"status": "posted", "posted_at": datetime.now(VN).isoformat(timespec="seconds")})
        save(data)
        print(json.dumps({"posted": x["id"]}))
    else:
        sys.exit(__doc__)
