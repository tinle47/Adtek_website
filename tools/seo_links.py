"""Kiểm tra link nội bộ hỏng từ kết quả seo_audit.py.

Cách dùng: python3 tools/seo_links.py crawl.json links.json
"""
import json
import subprocess
import sys
import time
from collections import defaultdict

SKIP = ("/wp-admin", "/wp-login", "/feed", "/xmlrpc", "replytocom=", "/wp-json", "mailto:", "tel:")


def status(url):
    r = subprocess.run(
        ["curl", "-sS", "-o", "/dev/null", "-L", "--max-time", "30", "-A", "AdtekSEOAudit/1.0",
         "-w", "%{http_code} %{url_effective}", url],
        capture_output=True, text=True,
    )
    code, _, final = r.stdout.partition(" ")
    return int(code) if code.isdigit() else 0, final


if __name__ == "__main__":
    rows = json.load(open(sys.argv[1], encoding="utf-8"))
    crawled = {r["url"].rstrip("/"): r["status"] for r in rows}
    sources = defaultdict(set)
    for r in rows:
        for link in r["internal_links"]:
            if not any(s in link for s in SKIP):
                sources[link].add(r["url"])
    results = []
    todo = [l for l in sources if l.rstrip("/") not in crawled]
    for i, link in enumerate(sorted(todo), 1):
        code, final = status(link)
        results.append({"link": link, "status": code, "final": final, "found_on": sorted(sources[link])})
        print(f"{i}/{len(todo)} {code} {link}", flush=True)
        time.sleep(0.7)
    for link, srcs in sources.items():
        code = crawled.get(link.rstrip("/"))
        if code is not None:
            results.append({"link": link, "status": code, "final": link, "found_on": sorted(srcs)})
    json.dump(results, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
