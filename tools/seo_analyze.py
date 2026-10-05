"""Phân tích kết quả seo_audit.py thành danh sách vấn đề.

Cách dùng: python3 tools/seo_analyze.py crawl.json issues.json
"""
import json
import sys
from collections import Counter, defaultdict

TEMPLATE_IMG_SHARE = 0.3  # ảnh xuất hiện trên >= 30% số trang được coi là ảnh của giao diện


def analyze(rows):
    # Sitemap có thể liệt kê một URL nhiều lần (lỗi WPML + Yoast), chỉ phân tích mỗi URL một lần.
    rows = list({r["url"]: r for r in rows}.values())
    ok = [r for r in rows if r["status"] == 200 and not r["challenge"]]
    titles = Counter(r["title"] for r in ok if r["title"])
    descs = Counter(r["description"] for r in ok if r["description"])
    img_pages = Counter(src for r in ok for src in set(r["images_no_alt"]))
    template_imgs = {s for s, n in img_pages.items() if n >= TEMPLATE_IMG_SHARE * len(ok)}

    issues = []

    def add(r, severity, code, detail=""):
        issues.append({"url": r["url"], "group": r["group"], "severity": severity, "code": code, "detail": detail})

    for r in rows:
        if r["challenge"]:
            add(r, "info", "crawl_blocked", "Bị tường lửa chặn khi quét")
            continue
        if r["status"] != 200:
            add(r, "high", "status", f"HTTP {r['status']}")
            continue
        if r["final_url"].rstrip("/") != r["url"].rstrip("/"):
            add(r, "medium", "redirect_in_sitemap", r["final_url"])
        if "noindex" in r["robots"]:
            add(r, "high", "noindex_in_sitemap", r["robots"])
        t = r["title"]
        if not t:
            add(r, "high", "title_missing")
        else:
            if len(t) > 60:
                add(r, "low", "title_long", f"{len(t)} ký tự")
            if len(t) < 30:
                add(r, "low", "title_short", f"{len(t)} ký tự")
            if titles[t] > 1:
                add(r, "medium", "title_duplicate", t)
        d = r["description"]
        if not d:
            add(r, "high", "description_missing")
        else:
            if len(d) > 160:
                add(r, "low", "description_long", f"{len(d)} ký tự")
            if len(d) < 70:
                add(r, "low", "description_short", f"{len(d)} ký tự")
            if descs[d] > 1:
                add(r, "medium", "description_duplicate", d[:80])
        if not r["h1"]:
            add(r, "high", "h1_missing")
        elif len(r["h1"]) > 1:
            add(r, "medium", "h1_multiple", " | ".join(h[:40] for h in r["h1"]))
        if not r["canonical"]:
            add(r, "medium", "canonical_missing")
        elif r["canonical"].rstrip("/") != r["final_url"].rstrip("/"):
            add(r, "medium", "canonical_other", r["canonical"])
        if not r["og_image"]:
            add(r, "low", "og_image_missing")
        if r["words"] < 300 and r["group"] not in ("category",):
            add(r, "medium", "thin_content", f"{r['words']} từ")
        content_no_alt = [s for s in r["images_no_alt"] if s not in template_imgs]
        if content_no_alt:
            add(r, "medium", "img_alt_missing", f"{len(content_no_alt)} ảnh")

    return issues, sorted(template_imgs)


if __name__ == "__main__":
    rows = json.load(open(sys.argv[1], encoding="utf-8"))
    issues, template_imgs = analyze(rows)
    json.dump({"issues": issues, "template_images_no_alt": template_imgs},
              open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    by = defaultdict(int)
    for i in issues:
        by[(i["severity"], i["code"])] += 1
    for (sev, code), n in sorted(by.items()):
        print(f"{sev:6} {code:24} {n}")
    print("template images without alt:", len(template_imgs))
