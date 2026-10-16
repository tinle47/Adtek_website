"""Đưa bài dịch cũ (thư mục Submission trên Google Drive) lên WordPress theo đúng ngày viết.

Mỗi thư mục bài (đã chuẩn bị) có: vi.html (bài tiếng Việt, ảnh dạng <img src="media/...">), meta.json
(title, slug, seo_title, meta_desc, excerpt, categories, featured, ...), media/ (ảnh tách từ file .docx).
Ngày đăng lấy từ cột đầu của docs.tsv (YYYYMMDD, ngày ghi ở tên thư mục trên Drive), giờ 09:00.

Cách dùng:
  python3 tools/archive_post.py <thư mục submission> <aNN> [--publish]
    mặc định tạo hoặc cập nhật bản nháp (lùi ngày); --publish chuyển bài sang đăng (giữ ngày cũ).
Chạy lại an toàn: ảnh đã tải ghi trong aNN/result.json, không tải lại.
"""
import io
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

from blog_post import AUTHOR, api, nofollow
from fix_alt import API

MAX_W = 1600


def compress(src):
    """Ảnh lớn đổi sang JPEG rộng tối đa 1600px; ảnh nhỏ giữ nguyên định dạng."""
    im = Image.open(src)
    if src.stat().st_size < 250_000 and im.width <= MAX_W:
        return src, {"png": "image/png", "jpeg": "image/jpeg", "gif": "image/gif"}.get(im.format.lower(), "image/jpeg")
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    out = src.with_suffix(".web.jpg")
    im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
    return out, "image/jpeg"


def upload(path, ctype, name, alt):
    r = subprocess.run(["curl", "-sS", "--max-time", "300", "-X", "POST", f"{API}/media",
                        "-H", f'Content-Disposition: attachment; filename="{name}"',
                        "-H", f"Content-Type: {ctype}", "--data-binary", f"@{path}"],
                       capture_output=True, text=True)
    media = json.loads(r.stdout)
    if "id" not in media:
        sys.exit(f"Lỗi tải ảnh {path}: {r.stdout[:300]}")
    api("POST", f"media/{media['id']}?_fields=id", {"alt_text": alt})
    return media["id"], media["source_url"]


def run(root, folder, publish=False):
    root, d = Path(root), Path(root) / folder
    n = int(folder[1:])
    date = root.joinpath("docs.tsv").read_text(encoding="utf-8").splitlines()[n - 1].split("\t")[0]
    when = f"{date[:4]}-{date[4:6]}-{date[6:]}T09:00:00"
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    res_path = d / "result.json"
    res = json.loads(res_path.read_text(encoding="utf-8")) if res_path.exists() else {"images": {}}
    html = (d / "vi.html").read_text(encoding="utf-8")

    for i, m in enumerate(re.finditer(r'<img [^>]*src="(media/[^"]+)"[^>]*>', html), 1):
        rel = m.group(1)
        if rel in res["images"]:
            continue
        alt = re.search(r'alt="([^"]*)"', m.group(0))
        path, ctype = compress(d / rel)
        mid, url = upload(path, ctype, f"{meta['slug']}-{i}{path.suffix if path.suffix != '.jpg' else '.jpg'}",
                          alt.group(1) if alt else meta["title"])
        res["images"][rel] = {"id": mid, "url": url}
        res_path.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{folder}: ảnh {rel} -> {mid}")

    feat = meta.get("featured")
    if feat and feat not in res["images"]:  # ảnh đại diện không nằm trong thân bài
        path, ctype = compress(d / feat)
        mid, url = upload(path, ctype, f"{meta['slug']}-cover.jpg", meta["title"])
        res["images"][feat] = {"id": mid, "url": url}
        res_path.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

    for rel, info in res["images"].items():
        html = html.replace(f'src="{rel}"', f'src="{info["url"]}"')
    content = nofollow(html)
    body = {"title": meta["title"], "slug": meta["slug"], "author": AUTHOR, "content": content,
            "excerpt": meta.get("excerpt", ""), "categories": meta.get("categories") or [185], "date": when,
            "meta": {"_yoast_wpseo_title": meta.get("seo_title", ""), "_yoast_wpseo_metadesc": meta.get("meta_desc", "")}}
    if feat:
        body["featured_media"] = res["images"][feat]["id"]
    if publish:
        body["status"] = "publish"
    elif not res.get("post_id"):
        body["status"] = "draft"
    r = api("POST", f"posts/{res['post_id']}" if res.get("post_id") else "posts", body)
    if "id" not in r:  # cập nhật có thể xong mà proxy cắt phản hồi: đọc lại
        if res.get("post_id"):
            r = api("GET", f"posts/{res['post_id']}?context=edit&_fields=id,status,date,link")
        if "id" not in r:
            sys.exit(f"Lỗi tạo bài {folder}: {str(r)[:300]}")
    res.update(post_id=r["id"], status=r.get("status"), date=r.get("date"), link=r.get("link"))
    res_path.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{folder}: post {r['id']} ({r.get('status')}, {r.get('date')}) {meta['title']}")


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], "--publish" in sys.argv)
