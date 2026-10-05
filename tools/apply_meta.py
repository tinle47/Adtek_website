"""Điền meta description Yoast còn trống qua REST API (cần mu-plugin adtek-seo-meta.php).

- Trang chính: lấy từ content/seo/meta-descriptions.json (viết tay).
- Trang thuật ngữ (mona_glossary): tạo tự động "<Thuật ngữ> là gì? <đoạn mở đầu>".
Chỉ ghi vào trang đang để trống mô tả.

Cách dùng: python3 tools/apply_meta.py [--apply]
"""
import html
import json
import re
import sys
import time
from pathlib import Path

from fix_alt import api, fetch_all

MAX = 155
APPLY = "--apply" in sys.argv
ROOT = Path(__file__).resolve().parent.parent


def shorten(text, limit=MAX):
    text = " ".join(text.replace("—", ",").split())
    if len(text) <= limit:
        return text
    cut = text[: limit - 3].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + "..."


def glossary_desc(title, content):
    term = title.split(" - ")[0].strip()
    paras = [
        " ".join(html.unescape(re.sub(r"<[^>]+>", " ", p)).split())
        for p in re.findall(r"<p[^>]*>(.*?)</p>", content, re.S | re.I)
    ]
    if not paras:  # nội dung không có thẻ <p>: bỏ các dòng tiêu đề, lấy dòng đầu đủ dài
        paras = [l.strip() for l in html.unescape(re.sub(r"<h\d[^>]*>.*?</h\d>", "\n", content, flags=re.S)).splitlines()]
        paras = [re.sub(r"<[^>]+>", "", l) for l in paras]
    # Bỏ các đoạn ngắn kiểu tiêu đề phụ, ví dụ "Attribution Modeling (Mô hình phân bổ)", rồi ghép đến đủ dài.
    body = ""
    for para in paras:
        if len(para.split()) < 10 or (para.endswith(")") and "." not in para):
            continue
        body = f"{body} {para}".strip()
        if len(body) >= 120:
            break
    return shorten(f"{term} là gì? {body}")


def main():
    manual = json.loads((ROOT / "content/seo/meta-descriptions.json").read_text(encoding="utf-8"))["items"]
    plan = []
    for item in manual:
        assert len(item["desc"]) <= 160, (item["id"], len(item["desc"]))
        cur = api("GET", f"{item['type']}/{item['id']}?context=edit&_fields=meta")
        if not (cur.get("meta", {}).get("_yoast_wpseo_metadesc") or "").strip():
            plan.append((item["type"], item["id"], item["desc"]))

    for p in fetch_all("mona_glossary?context=edit&status=publish", "id,title,content,meta"):
        if not (p["meta"].get("_yoast_wpseo_metadesc") or "").strip():
            plan.append(("mona_glossary", p["id"], glossary_desc(p["title"]["raw"], p["content"]["raw"])))

    print(f"Sẽ điền {len(plan)} meta description")
    for t, i, d in plan[:5] + plan[-5:]:
        print(f"  {t} {i} ({len(d)}): {d}")
    if not APPLY:
        print("Chạy thử xong. Thêm --apply để cập nhật website.")
        return
    errors = []
    for t, i, d in plan:
        r = api("POST", f"{t}/{i}?_fields=id,meta", {"meta": {"_yoast_wpseo_metadesc": d}})
        if r.get("meta", {}).get("_yoast_wpseo_metadesc") != d:
            errors.append((t, i, str(r)[:150]))
        time.sleep(1)
    print(f"Đã cập nhật {len(plan) - len(errors)}/{len(plan)}. Lỗi: {errors[:5]}")


if __name__ == "__main__":
    main()
