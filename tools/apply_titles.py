"""Ghi SEO title (Yoast) từ content/seo/titles.json lên website.

- Bài viết, trang, thuật ngữ: meta _yoast_wpseo_title (cần mu-plugin adtek-seo-meta.php).
- Chuyên mục: trường REST adtek_seo (cần adtek-seo-meta.php từ bản 1.3).

Cách dùng: python3 tools/apply_titles.py [--apply] [--only posts,pages,mona_glossary,categories]
"""
import json
import sys
import time
from pathlib import Path

from fix_alt import api

ROOT = Path(__file__).resolve().parent.parent
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None


def main():
    data = json.loads((ROOT / "content/seo/titles.json").read_text(encoding="utf-8"))
    errors, done = [], 0
    cat_desc = data.get("category_desc", {})
    for group, items in data.items():
        if group.startswith("_") or group == "category_desc" or (ONLY and group not in ONLY):
            continue
        for pid, title in items.items():
            assert 30 <= len(title) <= 60, (group, pid, len(title))
            if not APPLY:
                print(f"  {group} {pid} ({len(title)}): {title}")
                continue
            if group == "categories":
                seo = {"title": title, "desc": cat_desc.get(pid, "")}
                r = api("POST", f"categories/{pid}?_fields=id,adtek_seo", {"adtek_seo": seo})
                ok = (r.get("adtek_seo") or {}).get("title") == title
            else:
                r = api("POST", f"{group}/{pid}?_fields=id,meta", {"meta": {"_yoast_wpseo_title": title}})
                ok = r.get("meta", {}).get("_yoast_wpseo_title") == title
            done += ok
            if not ok:
                errors.append((group, pid, str(r)[:150]))
            time.sleep(1)
    if APPLY:
        print(f"Đã cập nhật {done}. Lỗi: {len(errors)} {errors[:5]}")


if __name__ == "__main__":
    main()
