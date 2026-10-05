"""Dựng HTML cho trang Báo chí và FAQ từ content/pages/*.json, và cập nhật lên website.

Cách dùng:
  python3 tools/build_pages.py build            # chỉ dựng HTML vào build/pages/
  python3 tools/build_pages.py apply press      # cập nhật trang Báo chí (vi + en)
  python3 tools/build_pages.py apply faq        # cập nhật trang FAQ (vi + en)
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "pages"
PAGE_IDS = {"press": {"vi": 4340, "en": 5242}, "faq": {"vi": 1145, "en": 412}}


def esc(text):
    return html.escape(text, quote=True)


def press_html(data, lang):
    t = data[lang]
    cards = []
    for it in data["items"]:
        cards.append(
            '<div style="border:1px solid #E3E8F0;border-radius:12px;padding:24px;margin-bottom:20px">'
            f'<p style="margin:0 0 8px;color:#FF9014;font-weight:700">{esc(it["source"])}{" · " + esc(it["date"]) if it.get("date") else ""}</p>'
            f'<h2 style="margin:0 0 12px;font-size:2rem;line-height:1.4"><a href="{esc(it["url"])}" target="_blank" rel="noopener">{esc(it["title"])}</a></h2>'
            f'<p style="margin:0 0 12px">{esc(it[lang])}</p>'
            f'<p style="margin:0"><a href="{esc(it["url"])}" target="_blank" rel="noopener" style="color:#002D72;font-weight:700">{esc(t["read"])} &rarr;</a></p>'
            "</div>"
        )
    return f'<p>{esc(t["intro"])}</p>\n' + "\n".join(cards) + f'\n<p style="margin-top:32px">{t["contact"]}</p>'


def faq_html(items):
    parts = []
    for it in items:
        parts.append(f"<h2>{esc(it['q'])}</h2>\n<p>{it['a']}</p>")
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": it["q"],
             "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", it["a"])}}
            for it in items
        ],
    }
    ld = json.dumps(schema, ensure_ascii=False).replace("</", "<\\/")
    return "\n".join(parts) + f'\n<script type="application/ld+json">{ld}</script>'


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    press = json.loads((ROOT / "content/pages/press.json").read_text(encoding="utf-8"))
    faq = json.loads((ROOT / "content/pages/faq.json").read_text(encoding="utf-8"))
    pages = {}
    for lang in ("vi", "en"):
        pages[("press", lang)] = press_html(press, lang)
        pages[("faq", lang)] = faq_html(faq[lang])
    for (name, lang), body in pages.items():
        (OUT / f"{name}-{lang}.html").write_text(body, encoding="utf-8")
    return pages


if __name__ == "__main__":
    pages = build()
    print("Đã dựng:", ", ".join(f"{n}-{l}" for n, l in pages))
    if len(sys.argv) >= 3 and sys.argv[1] == "apply":
        sys.path.insert(0, str(Path(__file__).parent))
        from fix_alt import api

        name = sys.argv[2]
        for lang, pid in PAGE_IDS[name].items():
            r = api("POST", f"pages/{pid}?_fields=id,link", {"content": pages[(name, lang)]})
            print(lang, pid, "ok" if r.get("id") == pid else r)
