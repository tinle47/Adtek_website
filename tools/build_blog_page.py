"""Dựng trang artifact "Lịch blog Adtek" (danh sách bài, lịch đăng, SOP) từ content/editorial/calendar.json.

Cách dùng: python3 tools/build_blog_page.py <file ra .html>
"""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ("no", "date", "time", "title", "keyword", "cluster", "role", "refresh", "status", "approval", "wp_id")

data = json.loads((ROOT / "content/editorial/calendar.json").read_text(encoding="utf-8"))
payload = {"posts": [{k: p.get(k) for k in FIELDS} for p in data["posts"]], "clusters": data["clusters"]}
page = (ROOT / "templates/blog-plan.html").read_text(encoding="utf-8")
page = page.replace("__DATA__", json.dumps(payload, ensure_ascii=False).replace("</", "<\\/"))
page = page.replace("__UPDATED__", date.today().strftime("%d/%m/%Y"))
Path(sys.argv[1]).write_text(page, encoding="utf-8")
print(sys.argv[1])
