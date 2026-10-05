"""Điền alt text còn trống cho ảnh trên adtek.agency qua REST API.

- Ảnh trong nội dung bài viết: alt = tiêu đề mục (H2/H3) gần nhất phía trên ảnh,
  nếu ảnh nằm trước mọi tiêu đề thì dùng tên bài viết.
- Ảnh đại diện (featured image): alt = tên bài/trang.
- Logo trong dữ liệu E-Commerce: alt = "Logo <tên doanh nghiệp>".
Chỉ điền vào alt đang trống, không sửa alt đã có.

Cách dùng: python3 tools/fix_alt.py [--apply]  (mặc định chỉ chạy thử)
"""
import html
import json
import re
import subprocess
import sys
import time

API = "https://adtek.agency/wp-json/wp/v2"
APPLY = "--apply" in sys.argv


def api(method, path, data=None):
    cmd = ["curl", "-sS", "-X", method, f"{API}/{path}"]
    if data is not None:
        cmd += ["-H", "Content-Type: application/json; charset=utf-8", "--data-binary", "@-"]
    r = subprocess.run(cmd, input=json.dumps(data, ensure_ascii=False) if data is not None else None,
                       capture_output=True, text=True)
    return json.loads(r.stdout)


def fetch_all(path, fields):
    out, page = [], 1
    while True:
        batch = api("GET", f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}&_fields={fields}")
        if not isinstance(batch, list) or not batch:
            return out
        out += batch
        page += 1


def clean(text, limit=125):
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    text = " ".join(text.split()).strip(" :.-")
    text = re.sub(r"^\d+[.)]\s*", "", text)  # bỏ số thứ tự đầu tiêu đề, ví dụ "1. "
    return text if len(text) <= limit else text[: limit - 1].rsplit(" ", 1)[0]


def fill_content_alts(content, title):
    """Trả về (nội dung mới, {attachment_id: alt})."""
    heading = title
    media_alts = {}
    used = {}
    out, pos = [], 0
    for m in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>|<img\b[^>]*>", content, re.S | re.I):
        if m.group(0).lower().startswith("<h"):
            h = clean(m.group(1))
            if h:
                heading = h
            continue
        tag = m.group(0)
        alt = re.search(r'\balt="([^"]*)"', tag)
        wid = re.search(r"wp-image-(\d+)", tag)
        if alt and alt.group(1).strip():
            # Ảnh đã có alt trong bài: dùng lại cho thư viện nếu thư viện còn trống.
            if wid:
                media_alts.setdefault(int(wid.group(1)), html.unescape(alt.group(1)))
            continue
        used[heading] = used.get(heading, 0) + 1
        text = heading if used[heading] == 1 else f"{heading} (hình {used[heading]})"
        safe = html.escape(text, quote=True)
        new_tag = tag.replace(alt.group(0), f'alt="{safe}"', 1) if alt else tag.replace("<img", f'<img alt="{safe}"', 1)
        out.append(content[pos:m.start()] + new_tag)
        pos = m.end()
        if wid:
            media_alts.setdefault(int(wid.group(1)), text)
    out.append(content[pos:])
    return "".join(out), media_alts


def main():
    media = {m["id"]: m for m in fetch_all("media?media_type=image", "id,alt_text")}
    empty = {i for i, m in media.items() if not m["alt_text"].strip()}
    print(f"Ảnh trong thư viện: {len(media)}, thiếu alt: {len(empty)}")

    media_updates = {}
    post_updates = []
    for p in fetch_all("posts?context=edit", "id,title,content,featured_media"):
        title = clean(p["title"]["raw"])
        new, alts = fill_content_alts(p["content"]["raw"], title)
        strip_alt = lambda c: re.sub(r'\s*alt="[^"]*"', "", c)
        assert strip_alt(new) == strip_alt(p["content"]["raw"]), f"bài {p['id']}: thay đổi ngoài alt"
        if new != p["content"]["raw"]:
            post_updates.append((p["id"], title, new, len(alts)))
        for mid, alt in alts.items():
            if mid in empty:
                media_updates.setdefault(mid, alt)
        if p["featured_media"] in empty:
            media_updates.setdefault(p["featured_media"], title)

    for path in ("pages", "mona_solution", "mona_reports", "mona_recruitment", "mona_glossary", "mona_team"):
        for p in fetch_all(f"{path}?context=edit", "id,title,featured_media"):
            if p["featured_media"] in empty:
                media_updates.setdefault(p["featured_media"], clean(p["title"]["raw"]))

    for p in fetch_all("mona_ecommerce?context=edit", "id,title,featured_media"):
        if p["featured_media"] in empty:
            name = clean(p["title"]["raw"].split(" - ")[0])
            media_updates.setdefault(p["featured_media"], f"Logo {name}")

    print(f"Bài viết cần sửa alt trong nội dung: {len(post_updates)}")
    print(f"Ảnh trong thư viện sẽ được điền alt: {len(media_updates)}")
    for pid, title, _, n in post_updates[:5]:
        print(f"  bài {pid}: {n} ảnh | {title[:60]}")
    for mid, alt in list(media_updates.items())[:10]:
        print(f"  media {mid}: {alt}")

    if not APPLY:
        print("Chạy thử xong. Thêm --apply để cập nhật website.")
        return
    log = []
    for pid, title, new, _ in post_updates:
        r = api("POST", f"posts/{pid}?_fields=id", {"content": new})
        log.append(("post", pid, "ok" if r.get("id") == pid else r))
        time.sleep(0.5)
    for mid, alt in media_updates.items():
        r = api("POST", f"media/{mid}?_fields=id,alt_text", {"alt_text": alt})
        log.append(("media", mid, "ok" if r.get("alt_text") == alt else r))
        time.sleep(0.3)
    errors = [l for l in log if l[2] != "ok"]
    print(f"Đã cập nhật {len(log) - len(errors)}/{len(log)}. Lỗi: {errors[:5]}")


if __name__ == "__main__":
    main()
