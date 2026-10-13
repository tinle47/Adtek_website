"""Đồng bộ trang chủ tiếng Anh theo trang chủ tiếng Việt (bản chuẩn), dữ liệu trong content/pages/home.json.

Các bước:
  1. Đọc trường ACF của 2 trang (cần mu-plugin adtek-acf-rest.php), lưu bản sao vào content/backups/.
  2. Sửa bản VI theo vi_fixes.
  3. Chép toàn bộ trường của bản VI sang bản EN: ảnh, logo, thứ tự giữ nguyên; chữ dịch theo "en",
     link đổi theo "en_links", form tư vấn đổi sang form tiếng Anh theo "en_form".
  Chữ nào chưa có bản dịch thì dừng lại và liệt kê, không ghi gì.

Cách dùng: python3 tools/sync_home.py [--apply]  (mặc định chỉ chạy thử, in các thay đổi)
"""
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import fix_alt

ROOT = Path(__file__).resolve().parent.parent
APPLY = "--apply" in sys.argv


WP_API = fix_alt.API


def acf(method, pid, data=None):
    # Dùng lại hàm gọi API của fix_alt (có thử lại khi gặp trang chống bot), tạm đổi sang namespace adtek/v1.
    fix_alt.API = "https://adtek.agency/wp-json/adtek/v1"
    try:
        return fix_alt.api(method, f"acf/{pid}", data)
    finally:
        fix_alt.API = WP_API


def map_media(vi, en_cur, path=""):
    """Chọn ID ảnh cho bản EN: giữ ID bản EN đang dùng nếu cùng file với bản VI, nếu không thì dùng
    bản sao tiếng Anh WPML tạo cho ảnh đó (cùng file, khác ID), không có bản sao thì dùng chung ID bản VI."""
    if isinstance(vi, dict):
        cur = en_cur if isinstance(en_cur, dict) else {}
        return {k: map_media(v, cur.get(k), f"{path}.{k}") for k, v in vi.items()}
    if isinstance(vi, list):
        cur = en_cur if isinstance(en_cur, list) else []
        return [map_media(v, cur[i] if i < len(cur) else None, f"{path}.{i}") for i, v in enumerate(vi)]
    if not isinstance(vi, int) or isinstance(vi, bool):
        return vi
    url = media_url(vi)
    if isinstance(en_cur, int) and not isinstance(en_cur, bool) and media_url(en_cur) == url:
        return en_cur
    name = url.rsplit("/", 1)[-1].rsplit(".", 1)[0] if url else ""
    for m in fix_alt.api("GET", f"media?lang=en&search={quote(name)}&_fields=id,source_url") if name else []:
        if isinstance(m, dict) and m.get("source_url") == url:
            return m["id"]
    return vi


_urls = {}


def media_url(mid):
    if mid not in _urls:
        _urls[mid] = fix_alt.api("GET", f"media/{mid}?_fields=source_url").get("source_url")
    return _urls[mid]


def norm(text):
    return " ".join(text.split())


def walk(value, fn, path=""):
    """Gọi fn(path, chuỗi) cho mọi chuỗi trong dữ liệu ACF, trả bản mới."""
    if isinstance(value, dict):
        return {k: walk(v, fn, f"{path}.{k}" if path else k) for k, v in value.items()}
    if isinstance(value, list):
        return [walk(v, fn, f"{path}.{i}") for i, v in enumerate(value)]
    if isinstance(value, str):
        return fn(path, value)
    return value


def unformat(path, text):
    """Bỏ <br /> mà ACF tự thêm trước dấu xuống dòng khi hiển thị (ô textarea), để ghi lại đúng giá trị gốc."""
    return re.sub(r"<br />(\r?\n)", r"\1", text)


def same(a, b):
    """So 2 giá trị sau khi bỏ định dạng hiển thị của ACF và WordPress (<br />, dấu nháy cong, &#8217;)."""
    def clean(path, text):
        return norm(html.unescape(unformat(path, text)).replace("\u2019", "'"))
    return walk(a, clean) == walk(b, clean)


def is_neutral(text):
    """Chuỗi giữ nguyên ở bản EN: rỗng, số, link, email, số điện thoại, tên riêng không dấu."""
    t = norm(re.sub(r"<[^>]+>", " ", text))
    if not t or re.fullmatch(r"[\d\s+().-]+", t) or re.fullmatch(r"(https?://|mailto:|tel:)\S+", t):
        return True
    if re.fullmatch(r"\S+@\S+", t):
        return True
    # Không có chữ tiếng Việt có dấu thì coi là tên riêng/thuật ngữ tiếng Anh (Brand Commerce, SEO...).
    return not re.search(r"[À-ỹĐđ]", t)


def main():
    data = json.loads((ROOT / "content/pages/home.json").read_text(encoding="utf-8"))
    ids = data["page_ids"]
    cur = {lang: acf("GET", pid) for lang, pid in ids.items()}
    for lang, r in cur.items():
        if "fields" not in r:
            sys.exit(f"Không đọc được ACF bản {lang}: {r}. Đã upload adtek-acf-rest.php chưa?")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    for lang, r in cur.items() if APPLY else ():
        out = ROOT / f"content/backups/home-acf-{lang}-{ids[lang]}-{stamp}.json"
        out.write_text(json.dumps(r["fields"], ensure_ascii=False, indent=2), encoding="utf-8")
    vi_old = cur["vi"]["fields"]

    # 2. Sửa bản VI
    fixes_used = set()

    def fix_vi(path, text):
        for i, f in enumerate(data["vi_fixes"]):
            if f.get("path") and f["path"] != path:
                continue
            if f["old"] in text:
                text = text.replace(f["old"], f["new"])
                fixes_used.add(i)
            elif norm(f["old"]) in norm(text):
                text = norm(text).replace(norm(f["old"]), f["new"])
                fixes_used.add(i)
        return text

    vi_new = walk(vi_old, fix_vi)
    for i, f in enumerate(data["vi_fixes"]):
        if i not in fixes_used:
            print(f"- Không còn chỗ cần sửa (có thể đã sửa trước đó): {f['old'][:60]}")

    # 3. Dựng bản EN từ bản VI
    tr = {norm(k): v for k, v in data["en"].items()}
    links = data["en_links"]
    form = data["en_form"]
    missing = []

    def to_en(path, text):
        if "[contact-form-7" in text:
            if any(f'id="{i}"' in text for i in form["vi_ids"]):
                return form["shortcode"]
            missing.append((path, text))
            return text
        if text.strip() in links:
            return links[text.strip()]
        key = norm(text)
        if key in tr:
            return tr[key]
        if is_neutral(text):
            return text
        # Chuỗi có xuống dòng/thẻ HTML: dịch từng dòng chữ bên trong.
        plain = norm(re.sub(r"<[^>]+>", " ", text))
        if plain in tr:
            return tr[plain]
        missing.append((path, text))
        return text

    en_new = walk(vi_new, to_en)
    en_new = map_media(en_new, cur["en"]["fields"])
    if missing:
        print("Chưa có bản dịch (thêm vào content/pages/home.json):")
        for path, text in missing:
            print(f"  {path}: {text!r}")
        sys.exit(1)

    def changes(old, new):
        rows = []

        def diff(a, b, path=""):
            if isinstance(b, dict):
                for k in b:
                    diff(a.get(k) if isinstance(a, dict) else None, b[k], f"{path}.{k}" if path else k)
            elif isinstance(b, list):
                for i, v in enumerate(b):
                    diff(a[i] if isinstance(a, list) and i < len(a) else None, v, f"{path}.{i}")
                if isinstance(a, list) and len(a) > len(b):
                    rows.append((path, f"{len(a)} mục", f"{len(b)} mục"))
            elif not same(a, b):
                rows.append((path, a, b))

        diff(old, new)
        return rows

    for lang, old, new in (("vi", vi_old, vi_new), ("en", cur["en"]["fields"], en_new)):
        rows = changes(old, new)
        print(f"\n== Bản {lang} (trang {ids[lang]}): {len(rows)} thay đổi")
        for path, a, b in rows:
            print(f"  {path}\n    cũ: {str(a)[:110]!r}\n    mới: {str(b)[:110]!r}")

    if not APPLY:
        print("\nChạy thử, chưa ghi. Thêm --apply để cập nhật.")
        return
    for lang, fields, old in (("vi", vi_new, vi_old), ("en", en_new, cur["en"]["fields"])):
        payload = {k: walk(v, unformat) for k, v in fields.items() if not same(old.get(k), v)}
        if not payload:
            print(lang, "không đổi")
            continue
        r = acf("POST", ids[lang], {"fields": payload})
        print(lang, ids[lang], r.get("result", r))
        if r.get("fields") is not None and any(not same(r["fields"].get(k), fields[k]) for k in payload):
            print(f"! Bản {lang}: dữ liệu đọc lại khác dữ liệu đã gửi, cần kiểm tra.")
    # Xóa cache cả 2 trang (cần adtek-acf-rest.php từ bản 1.1.0; bản cũ bỏ qua yêu cầu này).
    for lang, pid in ids.items():
        print("xóa cache", lang, acf("POST", pid, {"purge": True}).get("purged", "chưa hỗ trợ"))


if __name__ == "__main__":
    main()
