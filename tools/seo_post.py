"""Tối ưu SEO bài blog sau khi lên sóng (phiên Adtek - SEO, lịch thứ Ba và thứ Năm 21:43).

Cách dùng:
  python3 tools/seo_post.py due                 bài đã lên sóng mà chưa tối ưu SEO (tự đổi scheduled thành published)
  python3 tools/seo_post.py check <số bài>      kiểm tra bài đang live, in kết quả từng mục (JSON)
  python3 tools/seo_post.py fix <số bài>        tự sửa phần kỹ thuật: focus keyphrase, alt ảnh, nofollow link ngoài, xóa cache
  python3 tools/seo_post.py links <số bài>      các bài nên trỏ link về bài này, bài nào đã có link
  python3 tools/seo_post.py meta <số bài>       ghi seo_title, meta_desc trong calendar.json lên Yoast
  python3 tools/seo_post.py get <ID WP> <file>  tải nội dung gốc của bài về file để sửa
  python3 tools/seo_post.py put <ID WP> <file> <lý do>  backup bản đang có vào content/backups, ghi nội dung mới, xóa cache
  python3 tools/seo_post.py done <số bài>       ghi seo_optimized (ngày giờ) vào calendar.json

Chỉ kiểm tra được link nội bộ: mạng của môi trường chặn site bên ngoài, link ngoài do lịch rà soát ngày 1 hằng tháng xử lý.
"""
import html
import json
import re
import subprocess
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path

from blog_post import VN, find, load, nofollow, save
from fix_alt import api, clean, fetch_all, fill_content_alts
from seo_audit import PageParser, fetch

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://adtek.agency"
BAD_ANCHORS = ("xem thêm", "tại đây", "click", "bấm vào", "đây", "link này")


def slugify(text):
    text = unicodedata.normalize("NFD", text.lower().replace("đ", "d"))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def norm(text):
    return " ".join(unicodedata.normalize("NFC", html.unescape(text)).lower().split())


def has_kw(text, kw):
    """Đủ cụm từ khóa (exact), hoặc đủ mọi từ của từ khóa như cách Yoast so khớp (words)."""
    text, kw = norm(text), norm(kw)
    if kw in text:
        return "exact"
    words = re.findall(r"\w+", text)
    return "words" if all(w in words for w in re.findall(r"\w+", kw)) else ""


def plain(content):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", " ", content, flags=re.S))).split())


def wp_post(wp_id):
    return api("GET", f"posts/{wp_id}?context=edit&_fields=id,status,date,link,title,content,meta,featured_media")


def url_of(ref, data):
    """ref: số bài trong lịch (int) hoặc ID bài WordPress (chuỗi). Trả về (wp_id, url) hoặc (None, None)."""
    if isinstance(ref, int):
        p = next((x for x in data["posts"] if x["no"] == ref), None)
        if not p or p["status"] != "published" or not p.get("wp_id"):
            return None, None
        return p["wp_id"], f"{SITE}/{p['slug']}/"
    r = api("GET", f"posts/{ref}?_fields=id,link,status")
    return (int(ref), r["link"]) if r.get("status") == "publish" else (None, None)


def write(path, body):
    """Ghi qua REST một lần, không chờ thử lại: khi cập nhật bài đã đăng, proxy hay cắt phản hồi dù WordPress đã lưu.
    Nơi gọi tự đọc lại để xác nhận."""
    subprocess.run(["curl", "-sS", "-o", "/dev/null", "--max-time", "90", "-X", "POST", f"{SITE}/wp-json/wp/v2/{path}",
                    "-H", "Content-Type: application/json; charset=utf-8", "--data-binary", "@-"],
                   input=json.dumps(body, ensure_ascii=False), capture_output=True, text=True)


def purge(wp_id):
    r = subprocess.run(["curl", "-sS", "--max-time", "60", "-X", "POST", f"{SITE}/wp-json/adtek/v1/acf/{wp_id}",
                        "-H", "Content-Type: application/json", "--data-binary", '{"purge": true}'],
                       capture_output=True, text=True)
    return "purged" in r.stdout


def write_content(wp_id, content, reason, extra=None):
    """Backup nội dung và meta đang có, ghi nội dung mới, đọc lại để xác nhận (proxy có thể cắt phản hồi khi cập nhật bài đã đăng)."""
    cur = wp_post(wp_id)
    stamp = datetime.now(VN).strftime("%Y%m%d-%H%M")
    backup = ROOT / f"content/backups/post-{wp_id}-before-{slugify(reason)[:40]}-{stamp}.json"
    backup.write_text(json.dumps({"id": wp_id, "modified": stamp, "content": cur["content"]["raw"], "meta": cur.get("meta")},
                                 ensure_ascii=False, indent=1), encoding="utf-8")
    body = {"content": content, **(extra or {})}
    write(f"posts/{wp_id}?_fields=id", body)
    after = wp_post(wp_id)
    if after["content"]["raw"] != content:
        sys.exit(f"Lỗi: nội dung bài {wp_id} chưa được ghi, backup tại {backup.relative_to(ROOT)}")
    # Bài trong lịch: giữ file HTML trong repo khớp với bản đang live.
    post = next((p for p in load()["posts"] if p.get("wp_id") == wp_id), None)
    if post:
        (ROOT / f"content/posts/{post['slug']}.html").write_text(content, encoding="utf-8")
    return backup, purge(wp_id)


def due(data):
    out, changed = [], False
    for post in data["posts"]:
        if post["status"] not in ("scheduled", "published") or not post.get("wp_id") or post.get("seo_optimized"):
            continue
        r = api("GET", f"posts/{post['wp_id']}?_fields=status,date")
        if r.get("status") != "publish":
            continue
        if post["status"] == "scheduled":
            post["status"], post["published"], changed = "published", r["date"][:10], True
        out.append({"no": post["no"], "wp_id": post["wp_id"], "url": f"{SITE}/{post['slug']}/", "published": post["published"]})
    if changed:
        save(data)
    print(json.dumps({"due": out}, ensure_ascii=False, indent=1))


def sitemap_urls():
    idx = fetch(f"{SITE}/sitemap_index.xml")[3]
    urls = set()
    for sm in re.findall(r"<loc>([^<]*post-sitemap\d*\.xml)</loc>", idx):
        urls |= set(re.findall(r"<loc>([^<]+)</loc>", fetch(sm)[3]))
    return urls


def inbound(slug, wp_id):
    """ID các bài đã đăng có link trỏ tới bài này."""
    pat = re.compile(rf'href="(https?://(www\.)?adtek\.agency)?/{re.escape(slug)}/?["#?]')
    return sorted(p["id"] for p in fetch_all("posts?context=edit&status=publish", "id,content")
                  if p["id"] != wp_id and pat.search(p["content"]["raw"]))


def link_status(url):
    r = subprocess.run(["curl", "-sS", "-o", "/dev/null", "-L", "--max-time", "30", "-A", "AdtekSEOAudit/1.0",
                        "-w", "%{http_code}", url], capture_output=True, text=True)
    return int(r.stdout) if r.stdout.isdigit() else 0


def check(data, post):
    url = f"{SITE}/{post['slug']}/"
    kw = post["keyword"]
    wp = wp_post(post["wp_id"])
    raw = wp["content"]["raw"]
    status, final, _, page = fetch(url)
    p = PageParser()
    p.feed(page)
    title, desc = " ".join(p.title.split()), p.meta.get("description", "")
    h1 = [" ".join(x.split()) for x in p.h["h1"]]
    h2 = [clean(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", raw, re.S | re.I)]
    text = plain(raw)
    first = " ".join(text.split()[:120])
    media = api("GET", f"media/{wp['featured_media']}?_fields=alt_text") if wp.get("featured_media") else {}
    imgs = re.findall(r"<img\b[^>]*>", raw, re.I)
    links = re.findall(r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>', raw, re.S | re.I)
    # Link nội bộ trong bài thường viết dạng tương đối (/slug/): đổi về URL đầy đủ.
    internal = sorted({re.sub(r"^https?://(www\.)?adtek\.agency", SITE, SITE + h if h.startswith("/") else h).split("#")[0]
                       for h, _ in links if re.match(r"(https?://(www\.)?adtek\.agency)?/(?!/)", h)})
    external_tags = [t for t in re.findall(r'<a\s[^>]*href="https?://[^"]*"[^>]*>', raw)
                     if not re.search(r'href="https?://(www\.)?adtek\.agency', t)]
    pillar = data["clusters"][post["cluster"]]["pillar"]
    pillar_url = url_of(pillar, data)[1] if pillar and pillar != post["no"] else None
    targets = [u for u in (url_of(r, data)[1] for r in post.get("links_to", [])) if u]
    inb = inbound(post["slug"], post["wp_id"])
    pillar_id = url_of(pillar, data)[0] if pillar_url else None
    broken = []
    for link in internal:
        code = link_status(link)
        if code != 200:
            broken.append(f"{code} {link}")
        time.sleep(0.7)
    kw_count = len(re.findall(re.escape(norm(kw)), norm(text)))
    words = len(text.split())

    res = []

    def add(code, ok, detail="", fix=""):
        res.append({"code": code, "ok": bool(ok), "detail": detail, **({"fix": fix} if fix and not ok else {})})

    add("http_200", status == 200 and final.rstrip("/") == url.rstrip("/"), f"{status} {final}")
    add("indexable", "noindex" not in p.meta.get("robots", ""), p.meta.get("robots", ""))
    add("canonical_self", (p.canonical or "").rstrip("/") == url.rstrip("/"), p.canonical or "")
    add("in_sitemap", url in sitemap_urls(), "post-sitemap.xml")
    add("schema_article", '"Article"' in "".join(p.jsonld), "")
    add("og_image", p.meta.get("og:image"), p.meta.get("og:image", ""))
    add("h1_single", len(h1) == 1, " | ".join(h1))
    add("title_length", 30 <= len(title) <= 60, f"{len(title)} ký tự: {title}", "sửa seo_title")
    add("desc_length", 120 <= len(desc) <= 156, f"{len(desc)} ký tự", "sửa meta_desc")
    add("focus_keyphrase", norm(wp["meta"].get("_yoast_wpseo_focuskw", "")) == norm(kw),
        wp["meta"].get("_yoast_wpseo_focuskw", ""), "fix")
    add("kw_in_title", has_kw(title, kw), has_kw(title, kw) or title, "sửa seo_title")
    add("kw_at_title_start", 0 <= norm(title).find(norm(kw)) <= 15, title, "đưa từ khóa lên đầu seo_title")
    add("kw_in_desc", has_kw(desc, kw), has_kw(desc, kw), "sửa meta_desc")
    add("kw_in_slug", slugify(kw) in post["slug"] or all(w in post["slug"].split("-") for w in slugify(kw).split("-")),
        post["slug"], "không đổi slug bài đã đăng, chỉ ghi nhận")
    add("kw_in_intro", has_kw(first, kw), has_kw(first, kw) or "120 chữ đầu chưa có", "thêm từ khóa vào đoạn mở đầu")
    add("kw_in_h2", any(has_kw(h, kw) for h in h2), f"{sum(bool(has_kw(h, kw)) for h in h2)}/{len(h2)} H2",
        "thêm từ khóa vào 1 đến 2 H2")
    add("kw_density", 3 <= kw_count <= max(6, words // 150), f"{kw_count} lần đúng cụm / {words} chữ",
        "thêm hoặc bớt cụm từ khóa trong thân bài")
    add("featured_alt", (media.get("alt_text") or "").strip(), media.get("alt_text", ""), "fix")
    add("img_alt", all(re.search(r'\balt="[^"]+"', t) for t in imgs), f"{len(imgs)} ảnh trong bài", "fix")
    add("external_nofollow", all('nofollow' in t and 'noopener' in t and '_blank' in t for t in external_tags),
        f"{len(external_tags)} link ngoài", "fix")
    add("external_sources", len(external_tags) >= 3, f"{len(external_tags)} link ngoài", "thêm nguồn uy tín")
    add("anchor_text", not [a for _, a in links if norm(plain(a)) in BAD_ANCHORS],
        ", ".join(norm(plain(a)) for _, a in links if norm(plain(a)) in BAD_ANCHORS), "đổi anchor thành từ khóa bài đích")
    add("internal_out", len(internal) >= 3, f"{len(internal)} link nội bộ", "thêm link nội bộ")
    no_pillar = "không có trụ cột" if not pillar or pillar == post["no"] else f"trụ cột {pillar} chưa đăng"
    add("links_pillar", not pillar_url or pillar_url in internal, pillar_url or no_pillar, "thêm link lên trụ cột")
    add("links_to", all(t in internal for t in targets), ", ".join(t for t in targets if t not in internal),
        "thêm link tới bài trong links_to")
    add("internal_broken", not broken, "; ".join(broken), "sửa link hỏng")
    add("inbound_pillar", not pillar_id or pillar_id in inb, f"trụ cột {pillar_id}" if pillar_id else no_pillar,
        "liên kết ngược từ trụ cột")
    add("inbound_count", len(inb) >= 3 if pillar_id else len(inb) >= 2, f"{len(inb)} bài trỏ về: {inb}",
        "liên kết ngược từ 2 đến 3 bài liên quan")
    add("words", words >= 1500, f"{words} chữ")
    failed = [r for r in res if not r["ok"]]
    print(json.dumps({"no": post["no"], "wp_id": post["wp_id"], "url": url, "keyword": kw,
                      "passed": len(res) - len(failed), "total": len(res), "failed": failed, "all": res},
                     ensure_ascii=False, indent=1))


def fix(data, post):
    wp_id, kw = post["wp_id"], post["keyword"]
    wp = wp_post(wp_id)
    done = []
    if norm(wp["meta"].get("_yoast_wpseo_focuskw", "")) != norm(kw):
        write(f"posts/{wp_id}?_fields=id", {"meta": {"_yoast_wpseo_focuskw": kw}})
        r = api("GET", f"posts/{wp_id}?context=edit&_fields=meta")
        done.append(f"focus keyphrase: {kw}" if r.get("meta", {}).get("_yoast_wpseo_focuskw") == kw
                    else f"LỖI focus keyphrase: {str(r)[:200]}")
    if wp.get("featured_media"):
        media = api("GET", f"media/{wp['featured_media']}?_fields=alt_text")
        if not (media.get("alt_text") or "").strip():
            write(f"media/{wp['featured_media']}?_fields=id", {"alt_text": post["title"]})
            done.append(f"alt ảnh đại diện: {post['title']}")
    raw = wp["content"]["raw"]
    content, media_alts = fill_content_alts(nofollow(raw), post["title"])
    for mid, alt in media_alts.items():
        write(f"media/{mid}?_fields=id", {"alt_text": alt})
    if content != raw:
        backup, purged = write_content(wp_id, content, "seo-fix")
        done.append(f"nội dung: nofollow/alt ảnh, backup {backup.relative_to(ROOT)}")
    elif done:
        purge(wp_id)
    print(json.dumps({"no": post["no"], "fixed": done or ["không có gì cần sửa"]}, ensure_ascii=False, indent=1))


def meta(data, post):
    want = {"_yoast_wpseo_title": post["seo_title"], "_yoast_wpseo_metadesc": post["meta_desc"]}
    write(f"posts/{post['wp_id']}?_fields=id", {"meta": want})
    got = api("GET", f"posts/{post['wp_id']}?context=edit&_fields=meta").get("meta", {})
    if any(got.get(k) != v for k, v in want.items()):
        sys.exit(f"Lỗi: Yoast chưa nhận SEO title/meta description bài {post['no']}")
    print(f"Bài {post['no']}: SEO title ({len(post['seo_title'])}), meta description ({len(post['meta_desc'])}), xóa cache: "
          f"{'có' if purge(post['wp_id']) else 'không'}")


def links(data, post):
    """Bài nên trỏ về bài này: trụ cột của cụm, bài trong links_to của bài này, bài đã đăng có links_to chứa bài này."""
    pillar = data["clusters"][post["cluster"]]["pillar"]
    refs = []
    if pillar and pillar != post["no"]:
        refs.append(("trụ cột", pillar))
    refs += [("links_to của bài này", r) for r in post.get("links_to", [])]
    refs += [(f"bài {p['no']} có links_to trỏ tới", p["no"]) for p in data["posts"]
             if post["no"] in p.get("links_to", []) and p["no"] != post["no"]]
    inb = inbound(post["slug"], post["wp_id"])
    out, seen = [], set()
    for why, ref in refs:
        wp_id, url = url_of(ref, data)
        if not wp_id or wp_id in seen:
            continue
        seen.add(wp_id)
        out.append({"ref": ref, "why": why, "wp_id": wp_id, "url": url, "already_links": wp_id in inb})
    print(json.dumps({"no": post["no"], "url": f"{SITE}/{post['slug']}/", "anchor_keyword": post["keyword"],
                      "inbound_now": inb, "candidates": out}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    data = load()
    if cmd == "due":
        due(data)
    elif cmd == "get":
        Path(sys.argv[3]).write_text(wp_post(int(sys.argv[2]))["content"]["raw"], encoding="utf-8")
        print(f"Đã lưu nội dung bài {sys.argv[2]} vào {sys.argv[3]}")
    elif cmd == "put":
        backup, purged = write_content(int(sys.argv[2]), Path(sys.argv[3]).read_text(encoding="utf-8"), sys.argv[4])
        print(f"Đã ghi bài {sys.argv[2]}, backup {backup.relative_to(ROOT)}, xóa cache thủ công: {'có' if purged else 'không (cần adtek-acf-rest 1.1.0 trở lên; WordPress vẫn tự xóa cache bài khi lưu)'}")
    elif cmd == "done":
        post = find(data, int(sys.argv[2]))
        post["seo_optimized"] = datetime.now(VN).strftime("%Y-%m-%d %H:%M")
        save(data)
        print(f"Bài {post['no']}: seo_optimized {post['seo_optimized']}")
    else:
        post = find(data, int(sys.argv[2]))
        {"check": check, "fix": fix, "links": links, "meta": meta}[cmd](data, post)
