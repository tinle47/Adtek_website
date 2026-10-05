"""Thu thập dữ liệu SEO on-page cho danh sách URL.

Cách dùng: python3 tools/seo_audit.py urls.txt out.json
- urls.txt: mỗi dòng "<nhóm> <url>"
- Chạy chậm (1 request/giây) để không kích hoạt tường lửa chống bot của hosting.
"""
import json
import re
import subprocess
import sys
import time
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

SITE = "adtek.agency"
DELAY = 1.0
CHALLENGE = "One moment, please"


def fetch(url):
    """Trả về (status, final_url, seconds, html). Thử lại khi gặp trang chống bot."""
    for attempt in range(3):
        r = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", "30", "-A", "AdtekSEOAudit/1.0",
             "-w", "\n__META__%{http_code} %{time_total} %{url_effective}", url],
            capture_output=True, text=True, errors="replace",
        )
        body, _, meta = r.stdout.rpartition("\n__META__")
        parts = meta.split(" ", 2)
        status = int(parts[0]) if parts and parts[0].isdigit() else 0
        if CHALLENGE in body[:3000] and attempt < 2:
            time.sleep(10)
            continue
        secs = float(parts[1]) if len(parts) > 1 else 0.0
        final = parts[2] if len(parts) > 2 else url
        return status, final, secs, body
    return status, final, secs, body


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.in_title = "", False
        self.meta, self.links, self.canonical, self.hreflang = {}, [], None, []
        self.h = {"h1": [], "h2": []}
        self.cur_h = None
        self.images = []
        self.jsonld, self.in_jsonld = [], False
        self.skip = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript"):
            self.skip += 1
            if tag == "script" and a.get("type") == "application/ld+json":
                self.in_jsonld = True
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link":
            rel = (a.get("rel") or "").lower()
            if rel == "canonical":
                self.canonical = a.get("href")
            elif rel == "alternate" and a.get("hreflang"):
                self.hreflang.append(a.get("hreflang"))
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "img":
            self.images.append({"src": a.get("src") or a.get("data-src") or "", "alt": a.get("alt")})
        elif tag in self.h:
            self.cur_h = tag
            self.h[tag].append("")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self.skip = max(0, self.skip - 1)
            self.in_jsonld = False
        elif tag == "title":
            self.in_title = False
        elif tag == self.cur_h:
            self.cur_h = None

    def handle_data(self, data):
        if self.in_jsonld:
            self.jsonld.append(data)
            return
        if self.in_title:
            self.title += data
        if self.skip:
            return
        if self.cur_h:
            self.h[self.cur_h][-1] += data
        self.text.append(data)


def main_text_words(html):
    """Đếm từ trong <main> (bỏ header/footer)."""
    m = re.search(r"<main\b.*?</main>", html, re.S | re.I)
    p = PageParser()
    p.feed(m.group(0) if m else html)
    return len(" ".join(p.text).split())


def schema_types(blobs):
    types = set()
    for b in blobs:
        for t in re.findall(r'"@type"\s*:\s*"([^"]+)"', b):
            types.add(t)
    return sorted(types)


def audit(group, url):
    status, final, secs, html = fetch(url)
    p = PageParser()
    p.feed(html)
    internal = set()
    for href in p.links:
        full = urljoin(final, href.split("#")[0])
        u = urlparse(full)
        if u.scheme in ("http", "https") and u.netloc.endswith(SITE):
            internal.add(full)
    imgs = [i for i in p.images if i["src"] and not i["src"].startswith("data:")]
    return {
        "group": group,
        "url": url,
        "status": status,
        "final_url": final,
        "seconds": round(secs, 2),
        "title": " ".join(p.title.split()),
        "description": p.meta.get("description", ""),
        "robots": p.meta.get("robots", ""),
        "canonical": p.canonical,
        "og_image": p.meta.get("og:image", ""),
        "hreflang": p.hreflang,
        "h1": [" ".join(x.split()) for x in p.h["h1"]],
        "h2_count": len(p.h["h2"]),
        "images": len(imgs),
        "images_no_alt": [i["src"] for i in imgs if not (i["alt"] or "").strip()],
        "words": main_text_words(html),
        "internal_links": sorted(internal),
        "schema": schema_types(p.jsonld),
        "challenge": CHALLENGE in html[:3000],
    }


if __name__ == "__main__":
    rows = []
    lines = [l.split() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
    for i, (group, url) in enumerate(lines, 1):
        rows.append(audit(group, url))
        print(f"{i}/{len(lines)} {rows[-1]['status']} {url}", flush=True)
        time.sleep(DELAY)
    json.dump(rows, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
