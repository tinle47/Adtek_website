"""Ghép nội dung case study (file JSON) vào templates/case-study-page.html.

Cách dùng: python3 tools/build_case_study.py content/case-studies/<ten>.json > out.html
"""
import html
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "case-study-page.html"


def paragraphs(items):
    return "\n\n".join(
        f"<!-- wp:paragraph -->\n<p>{html.escape(t)}</p>\n<!-- /wp:paragraph -->" for t in items
    )


def bullet_list(items, ordered=False):
    tag = "ol" if ordered else "ul"
    attrs = ' {"ordered":true}' if ordered else ""
    lis = "\n\n".join(
        f"<!-- wp:list-item -->\n<li>{html.escape(t)}</li>\n<!-- /wp:list-item -->" for t in items
    )
    return f'<!-- wp:list{attrs} -->\n<{tag} class="wp-block-list">{lis}</{tag}>\n<!-- /wp:list -->'


def result_column(value, label):
    return (
        "<!-- wp:column -->\n<div class=\"wp-block-column\">"
        '<!-- wp:heading {"textAlign":"center","style":{"color":{"text":"#FF9014"},"typography":{"fontSize":"40px"}}} -->\n'
        f'<h2 class="wp-block-heading has-text-align-center has-text-color" style="color:#FF9014;font-size:40px">{html.escape(value)}</h2>\n'
        "<!-- /wp:heading -->\n\n"
        '<!-- wp:paragraph {"align":"center"} -->\n'
        f'<p class="has-text-align-center">{html.escape(label)}</p>\n'
        "<!-- /wp:paragraph --></div>\n<!-- /wp:column -->"
    )


def testimonial(t):
    if not t:
        return ""
    return (
        '<!-- wp:quote {"style":{"spacing":{"margin":{"top":"32px"}}}} -->\n'
        '<blockquote class="wp-block-quote" style="margin-top:32px">'
        f"<!-- wp:paragraph -->\n<p>{html.escape(t['quote'])}</p>\n<!-- /wp:paragraph -->"
        f"<cite>{html.escape(t['author'])}</cite></blockquote>\n<!-- /wp:quote -->"
    )


def build(data):
    out = TEMPLATE.read_text(encoding="utf-8")
    parts = {
        "HEADLINE": html.escape(data["headline"]),
        "META": html.escape(data["meta"]),
        "RESULT_COLUMNS": "\n\n".join(result_column(r["value"], r["label"]) for r in data["key_results"]),
        "CONTEXT": paragraphs(data["context"]),
        "CHALLENGES": bullet_list(data["challenges"]),
        "SOLUTION": bullet_list(data["solution"], ordered=True),
        "RESULTS": paragraphs(data["results"]),
        "TESTIMONIAL": testimonial(data.get("testimonial")),
    }
    for key, value in parts.items():
        out = out.replace("{{" + key + "}}", value)
    return out


if __name__ == "__main__":
    sys.stdout.write(build(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))))
