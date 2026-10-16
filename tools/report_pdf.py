"""Dựng báo cáo PDF cho Trung Tâm Tài Nguyên (https://adtek.agency/resources-report/) từ file JSON nội dung.

Nội dung: content/reports/<slug>.json. Hai dạng:
  báo cáo nhanh: title, subtitle, period, key_stats, summary, sections, implications, sources
  báo cáo chuyên sâu: thêm executive {findings, dashboard}, chapters [{number, title, intro, sections}], appendix {tables, glossary};
  mỗi mục: heading, visual (bar, column, line, stacked, table, figures, timeline), body [đoạn], bullets, callout
Kết quả (cùng thư mục):
  <slug>.pdf         báo cáo A4: bìa, tóm tắt, các phần, khuyến nghị, nguồn, trang Về Adtek
  <slug>-cover.jpg   ảnh đại diện trên WordPress 1245x825 (trang danh sách cắt giữa còn tỉ lệ 370x250)

Cách dùng:
  python3 tools/report_pdf.py <slug> [<slug> ...]
  python3 tools/report_pdf.py --thumb <slug> [<slug> ...]   chỉ dựng lại ảnh đại diện, không dựng PDF
  python3 tools/report_pdf.py all
"""
import base64
import html
import io
import json
import subprocess
import sys
from pathlib import Path

from pypdf import PdfWriter

from covers import ASSETS, NAVY, ORANGE, REPORT_SIZE, REPORT_THEMES, font_css, hl, report_cover, shoot

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "content/reports"
esc = html.escape


def uri(name):
    return (ASSETS / name).as_uri()


INK, MUTED, LINE = "#1F2937", "#6B7280", "#E5E7EB"

CSS = f"""
{font_css()}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:BVP,sans-serif;color:{INK};font-size:10.2pt;line-height:1.55;background:#fff}}
.logo{{aspect-ratio:440/369;-webkit-mask:url({uri("adtek-logo-white.png")}) center/contain no-repeat;mask:url({uri("adtek-logo-white.png")}) center/contain no-repeat}}
.nr{{font-family:NR,serif;font-weight:600;letter-spacing:-.012em}}
.wrap{{padding:0 18mm}}
.page{{break-before:page;padding-top:.2mm}}  /* padding: không có thì Chromium in lọt một mẩu chữ đầu phần sang cuối trang trước */
.eyebrow{{font-weight:600;font-size:8.5pt;letter-spacing:.09em;text-transform:uppercase;color:{ORANGE}}}
h2{{font-family:NR,serif;font-weight:600;font-size:21pt;line-height:1.18;color:{NAVY};margin:2mm 0 4mm;text-wrap:balance}}
.lead{{font-size:11.2pt;color:#374151;margin-bottom:5mm}}
ul.b{{list-style:none;margin:0 0 5mm}}
ul.b li{{position:relative;padding-left:5mm;margin-bottom:2.2mm}}
ul.b li:before{{content:"";position:absolute;left:0;top:.62em;width:2mm;height:2mm;background:{ORANGE}}}
.rule{{height:1.2mm;width:22mm;background:{ORANGE};margin:0 0 6mm}}
.callout{{border-left:1mm solid {ORANGE};padding:1mm 0 1mm 5mm;margin:5mm 0;font-family:NR,serif;font-weight:500;font-size:13pt;line-height:1.4;color:{NAVY};break-inside:avoid}}
.callout small{{display:block;font-family:BVP;font-size:7.5pt;letter-spacing:.08em;text-transform:uppercase;color:{ORANGE};font-weight:600;margin-bottom:1mm}}
figure{{margin:2mm 0 6mm;break-inside:avoid;border-top:.3mm solid {NAVY};padding-top:3mm}}
figcaption{{font-weight:700;color:{NAVY};font-size:9.6pt;margin-bottom:3mm}}
.bar{{display:grid;grid-template-columns:38% 1fr 30mm;align-items:center;gap:3mm;margin-bottom:2mm;font-size:8.8pt}}
.bar .t{{height:4.2mm;background:#EEF1F6}}
.bar .f{{height:100%;background:{NAVY}}}
.bar.top .f{{background:{ORANGE}}}
.bar.neg .f{{background:#9CA3AF}}
.bar .v{{white-space:nowrap;font-weight:700;color:{NAVY};text-align:right;font-variant-numeric:tabular-nums}}
.tl{{display:grid;grid-template-columns:20mm 1fr;gap:4mm;padding:2mm 0;border-bottom:.3mm solid {LINE};font-size:9pt;align-items:baseline}}
.tl .d{{color:{ORANGE};font-size:13pt}}
.figs{{display:grid;gap:8mm;margin:1mm 0 2mm}}
.fig .v{{font-family:NR,serif;font-weight:600;font-size:24pt;line-height:1.1;color:{NAVY};letter-spacing:-.02em}}
.fig .l{{font-size:8.8pt;margin-top:1.5mm;color:#374151}}
.src{{font-size:7.6pt;color:{MUTED};margin-top:1.5mm}}
.stats{{display:grid;grid-template-columns:1fr 1fr;gap:7mm 10mm;margin:3mm 0 9mm}}
.stat{{border-top:.3mm solid {NAVY};padding-top:3mm}}
.stat .v{{font-family:NR,serif;font-weight:600;font-size:25pt;line-height:1.1;color:{NAVY};letter-spacing:-.02em}}
.stat .l{{font-size:9.4pt;margin-top:1.5mm}}
.stat .s{{font-size:7.6pt;color:{MUTED};margin-top:1mm}}
ol.sum{{list-style:none;counter-reset:s}}
ol.sum li{{counter-increment:s;position:relative;padding:0 0 3mm 10mm;break-inside:avoid}}
ol.sum li:before{{content:counter(s,decimal-leading-zero);position:absolute;left:0;top:0;font-family:NR,serif;font-weight:600;color:{ORANGE};font-size:12pt;line-height:1.3}}
.imp{{display:grid;grid-template-columns:13mm 1fr;gap:0 2mm;padding:4mm 0;border-top:.3mm solid {LINE};break-inside:avoid}}
.imp .n{{font-family:NR,serif;font-weight:600;font-size:20pt;color:{ORANGE};line-height:1}}
.imp h3{{font-size:11pt;color:{NAVY};margin-bottom:1.2mm}}
.imp .ex{{margin-top:1.5mm;font-size:9.2pt;color:#374151}}
.imp .ex b{{color:{NAVY}}}
ol.srcs{{font-size:8pt;line-height:1.45;padding-left:5mm}}
ol.srcs li{{margin-bottom:1.8mm;break-inside:avoid}}
ol.srcs .u{{color:{MUTED};word-break:break-all}}
ol.srcs.two{{columns:2;column-gap:8mm;font-size:7.2pt}}
figure.tbl{{break-inside:auto}}
figure.tbl thead{{display:table-header-group}}
figure.tbl tr{{break-inside:avoid}}
.note{{font-size:8pt;color:{MUTED};margin-top:6mm;border-top:.3mm solid {LINE};padding-top:3mm}}
.full{{width:210mm;height:297mm;position:relative;overflow:hidden;background:{NAVY};color:#fff}}
/* Báo cáo chuyên sâu (khóa chapters): mục lục, trang mở chương, mục chảy liên tục */
.opener{{break-before:page;padding-top:60mm}}
.opener .no{{font-family:NR,serif;font-weight:600;font-size:64pt;color:{ORANGE};line-height:1}}
.opener h1{{font-family:IT,sans-serif;font-weight:600;font-size:30pt;line-height:1.12;color:{NAVY};margin:6mm 0 8mm;letter-spacing:-.015em;text-wrap:balance}}
.opener p{{font-size:12pt;line-height:1.6;color:#374151;max-width:150mm}}
.opener ol{{list-style:none;margin-top:12mm;font-size:10pt;color:#374151}}
.opener ol li{{padding:2mm 0}}
.sec{{margin-bottom:9mm}}
.sec.pg{{break-before:page;padding-top:.2mm}}
.sec h2{{break-after:avoid}}
.sec p.body{{margin-bottom:3mm;text-align:left}}
.sec .visual{{break-inside:avoid}}
h2.sub{{font-size:17pt}}
.toc{{list-style:none;margin-top:4mm}}
.toc li{{display:grid;grid-template-columns:14mm 1fr 14mm;padding:3.2mm 0;border-bottom:.3mm solid {LINE};font-size:11pt;align-items:baseline}}
.toc .n{{font-family:NR,serif;font-weight:600;color:{ORANGE};font-size:13pt}}
.toc .p{{text-align:right;color:{MUTED};font-variant-numeric:tabular-nums}}
.cols{{display:grid;align-items:end;gap:2mm;height:52mm;padding-top:6mm}}
.cols .c{{min-width:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}}
.cols .c .f{{width:100%;background:{NAVY}}}
.cols .c.top .f{{background:{ORANGE}}}
.cols .c .v{{font-size:7.6pt;font-weight:700;color:{NAVY};margin-bottom:1mm;white-space:nowrap}}
.cols-l{{display:grid;gap:2mm;font-size:6.8pt;color:#374151;margin-top:1.5mm}}
.cols-l div{{min-width:0;text-align:center;line-height:1.2}}
.stk{{display:grid;grid-template-columns:24mm 1fr;gap:3mm;align-items:center;margin-bottom:2mm;font-size:8.6pt}}
.stk .t{{display:flex;height:6mm}}
.stk .t div{{height:100%;color:#fff;font-size:7.2pt;font-weight:700;display:flex;align-items:center;justify-content:center;overflow:hidden;white-space:nowrap}}
.legend{{display:flex;flex-wrap:wrap;gap:2mm 6mm;font-size:8pt;color:#374151;margin:2mm 0 1mm}}
.legend i{{display:inline-block;width:3mm;height:3mm;margin-right:1.5mm;vertical-align:-.3mm}}
table.t{{width:100%;border-collapse:collapse;font-size:8.4pt;line-height:1.35}}
table.t th{{text-align:left;background:{NAVY};color:#fff;font-weight:600;padding:2mm 2.2mm}}
table.t td{{padding:1.8mm 2.2mm;border-bottom:.3mm solid {LINE};vertical-align:top}}
table.t tr:nth-child(even) td{{background:#FAF7F1}}
table.t td.n,table.t th.n{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}}
dl.gl{{display:grid;grid-template-columns:32mm 1fr;gap:2.4mm 5mm;font-size:9pt}}
dl.gl dt{{font-weight:700;color:{NAVY}}}
"""


def head(title):
    return f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>{esc(title)}</title><style>{CSS}</style></head><body>'


def theme(r):
    """Phối màu bìa và trang cuối PDF: nền, chữ, khối dưới, thẻ trong khối, chữ thẻ, màu số.
    Anh Tin chốt (16/10/2026): mọi báo cáo dùng chung mẫu navy trên, khối kem dưới (REPORT_THEMES[0]);
    cover.theme chỉ còn đổi màu ảnh đại diện trên web."""
    return REPORT_THEMES[0]


# Trang bìa và trang cuối theo series "Báo cáo Adtek" (giống ảnh đại diện): phẳng, không đường kẻ, không hình tròn,
# tiêu đề Inter Tight có từ khóa tô cam, số Newsreader, không đặt chữ trên nền cam (khối cam luôn có thẻ kem hoặc navy).
def logo_img(color):
    """Logo Adtek tô sẵn một màu, nhúng data URI (in PDF bằng mask để lại vạch mảnh ở mép, nên dùng ảnh)."""
    from PIL import Image
    im = Image.open(ASSETS / "adtek-logo-white.png").convert("RGBA")
    fill = Image.new("RGBA", im.size, color)
    fill.putalpha(im.getchannel("A"))
    buf = io.BytesIO()
    fill.save(buf, "PNG")
    src = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    return f'<img src="{src}" alt="Adtek" style="position:absolute;left:18mm;top:18mm;height:15mm">'


FULL_CSS = """
.full{font-family:IT,sans-serif}
.full .lab{font-weight:600;font-size:11pt;opacity:.75}
.full h1{font-weight:600;letter-spacing:-.02em;text-wrap:balance}
.full .hl{color:%s}
.full .num{font-family:NR,serif;font-weight:600;letter-spacing:-.02em;line-height:1}
.block{position:absolute;left:0;right:0;bottom:0}
.inner{position:absolute;inset:0;display:flex;flex-direction:column}
""" % ORANGE


def block(r, height, content):
    """Khối màu ở cuối trang; khối cam thì nội dung nằm trên thẻ kem hoặc navy bên trong."""
    bg, fg, panel, card, pfg, numc = theme(r)
    inner = f'<div class="inner" style="padding:16mm 18mm 14mm;color:{pfg}">{content}</div>'
    if card:
        inner = (f'<div class="inner" style="inset:12mm 12mm 12mm;background:{card};padding:12mm 14mm 10mm;color:{pfg}">{content}</div>')
    return f'<div class="block" style="height:{height}mm;background:{panel}">{inner}</div>'


def cover_page(r):
    bg, fg, panel, card, pfg, numc = theme(r)
    c = r.get("cover") or {}
    main = c.get("stat", 0)
    st = r["key_stats"][main]
    others = [s for i, s in enumerate(r["key_stats"]) if i != main][:2]
    small = "".join(f'<div><div class="num" style="font-size:20pt;color:{numc}">{esc(s["value"])}</div>'
                    f'<div style="font-size:9.5pt;line-height:1.4;margin-top:2mm">{esc(s["label"])}</div></div>' for s in others)
    content = f"""<div class="num" style="font-size:44pt;color:{numc}">{esc(st["value"])}</div>
<div style="font-size:13pt;line-height:1.35;margin-top:4mm;max-width:150mm">{esc(st["label"])}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10mm;margin-top:10mm">{small}</div>
<div style="margin-top:auto;display:flex;justify-content:space-between;font-size:8.5pt;opacity:.7"><span>adtek.agency</span><span>Growth Marketing Agency</span></div>"""
    return f"""{head(r["title"])}<style>{FULL_CSS}</style><div class="full" style="background:{bg};color:{fg}">
{logo_img(fg)}
<div style="position:absolute;left:18mm;right:22mm;top:58mm">
 <div class="lab">Báo cáo Adtek &nbsp;·&nbsp; {esc(r["period"])}</div>
 <h1 style="font-size:{40 if len(c.get("title") or r["title"]) > 30 else 46}pt;line-height:1.06;margin:7mm 0 9mm">{hl(c.get("title") or r["title"])}</h1>
 <div style="font-size:14pt;line-height:1.45;opacity:.85;max-width:160mm">{esc(r["subtitle"])}</div>
</div>
{block(r, 118, content)}
</div></body></html>"""


def timeline(c):
    rows = "".join(f'<div class="tl"><div class="d nr">{esc(i["date"])}</div><div>{esc(i["label"])}</div></div>' for i in c["items"])
    return (f'<figure><figcaption>{esc(c["title"])}</figcaption>{rows}'
            f'<div class="src">Nguồn: {esc(c["source"])}</div></figure>')


def figures(c):
    """Hình mô tả dạng 2-3 con số lớn, cho phần không có chuỗi số để vẽ biểu đồ (văn bản luật, mốc thời gian)."""
    cells = "".join(f'<div class="fig"><div class="v">{esc(i["value"])}</div><div class="l">{esc(i["label"])}</div></div>' for i in c["items"])
    return (f'<figure><figcaption>{esc(c["title"])}</figcaption><div class="figs" style="grid-template-columns:repeat({len(c["items"]) if len(c["items"]) <= 4 else 3},1fr)">{cells}</div>'
            f'<div class="src">Nguồn: {esc(c["source"])}</div></figure>')


def chart(c):
    if c.get("type") == "timeline":
        return timeline(c)
    if c.get("type") == "figures":
        return figures(c)
    items = c["items"]
    top = max(abs(i["value"]) for i in items) or 1
    unit = c.get("unit", "")
    best = max(range(len(items)), key=lambda k: items[k]["value"])
    rows = []
    for k, i in enumerate(items):
        v = i["value"]
        num = f"{v:,.2f}".rstrip("0").rstrip(".").replace(",", "_").replace(".", ",").replace("_", ".")
        sign = "+" if unit == "%" and v > 0 and any(x["value"] < 0 for x in items) else ""
        cls = "neg" if v < 0 else ("top" if k == best else "")
        rows.append(f'<div class="bar {cls}"><div>{esc(i["label"])}</div><div class="t"><div class="f" style="width:{abs(v) / top * 100:.1f}%"></div></div>'
                    f'<div class="v">{sign}{num}{"" if unit in ("", None) else (unit if unit == "%" else " " + unit)}</div></div>')
    return (f'<figure><figcaption>{esc(c["title"])}</figcaption>{"".join(rows)}'
            f'<div class="src">Nguồn: {esc(c["source"])}</div></figure>')


def body_page(r):
    out = [head(r["title"]), '<div class="wrap">']
    out.append('<div class="eyebrow">Tóm tắt</div><h2>Những con số chính</h2><div class="rule"></div><div class="stats">')
    out += [f'<div class="stat"><div class="v">{esc(s["value"])}</div><div class="l">{esc(s["label"])}</div>'
            f'<div class="s">Nguồn: {esc(s["source"])}</div></div>' for s in r["key_stats"]]
    out.append('</div><ol class="sum">' + "".join(f"<li>{esc(x)}</li>" for x in r["summary"]) + "</ol>")
    for n, s in enumerate(r["sections"], 1):
        # Bố cục mỗi phần (anh Tin chốt): tiêu đề, biểu đồ hoặc hình mô tả, diễn giải, nhận định của Adtek
        out.append(f'<section class="page"><div class="eyebrow">Phần {n:02d}</div><h2>{esc(s["heading"])}</h2><div class="rule"></div>')
        if s.get("chart"):
            out.append(chart(s["chart"]))
        out.append(f'<p class="lead">{esc(s["lead"])}</p><ul class="b">' + "".join(f"<li>{esc(b)}</li>" for b in s["bullets"]) + "</ul>")
        if s.get("callout"):
            out.append(f'<div class="callout"><small>Nhận định của Adtek</small>{esc(s["callout"])}</div>')
        out.append("</section>")
    out.append('<section class="page"><div class="eyebrow">Khuyến nghị</div><h2>Doanh nghiệp nên làm gì</h2><div class="rule"></div>')
    out += [f'<div class="imp"><div class="n">{n:02d}</div><div><h3>{esc(i["title"])}</h3><div>{esc(i["text"])}</div>'
            f'<div class="ex"><b>Ví dụ:</b> {esc(i["example"])}</div></div></div>' for n, i in enumerate(r["implications"], 1)]
    out.append('</section><section class="page"><div class="eyebrow">Phụ lục</div><h2>Nguồn dữ liệu</h2><div class="rule"></div><ol class="srcs">')
    out += [f'<li>{esc(s["publisher"])}, {esc(s["name"])}{", " + esc(s["date"]) if s.get("date") else ""}.'
            f'{"<br><span class=u>" + esc(s["url"]) + "</span>" if s.get("url") else ""}</li>' for s in r["sources"]]
    out.append(f'</ol><div class="note">Báo cáo do Adtek tổng hợp từ các nguồn công khai nêu trên, số liệu cập nhật tới {esc(r["period"].replace("Cập nhật ", ""))}. '
               "Số liệu thuộc về đơn vị công bố; một số đơn vị dùng phương pháp đo khác nhau nên con số có thể chênh lệch. "
               "Tài liệu dùng để tham khảo, không thay thế tư vấn chuyên môn hoặc pháp lý.</div>")
    out.append("</section></div></body></html>")
    return "".join(out)


PALETTE = [NAVY, ORANGE, "#5B7DB1", "#E8B36B", "#9CA3AF", "#2F4F7F"]


def fmt(v):
    """Số kiểu Việt Nam: 411.800; 9,95."""
    if isinstance(v, str):
        return v
    s = f"{v:,.2f}".rstrip("0").rstrip(".")
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def unit_txt(unit):
    return "" if not unit else (unit if unit == "%" else " " + unit)


def fig_wrap(c, inner):
    cls = "visual tbl" if c.get("type") == "table" else "visual"  # bảng dài được ngắt trang, lặp dòng tiêu đề
    return (f'<figure class="{cls}"><figcaption>{esc(c.get("title", ""))}</figcaption>{inner}'
            f'<div class="src">Nguồn: {esc(c.get("source", ""))}</div></figure>')


def columns(c):
    items = c["items"]
    top = max(abs(i["value"]) for i in items) or 1
    best = max(range(len(items)), key=lambda k: items[k]["value"])
    cols = "".join(f'<div class="c {"top" if k == best else ""}"><div class="v">{fmt(i["value"])}{unit_txt(c.get("unit")) if c.get("unit") == "%" else ""}</div>'
                   f'<div class="f" style="height:{max(abs(i["value"]) / top * 100, 1):.1f}%"></div></div>' for k, i in enumerate(items))
    labels = "".join(f"<div>{esc(str(i['label'])).replace('/', '/<wbr>')}</div>" for i in items)  # nhãn dài xuống dòng sau dấu /
    u = c.get("unit")
    note = f'<div class="src" style="margin-top:0">Đơn vị: {esc(u)}</div>' if u and u != "%" else ""
    g = f'style="grid-template-columns:repeat({len(items)},minmax(0,1fr))"'  # cột và nhãn cùng lưới để thẳng hàng
    return fig_wrap(c, f'<div class="cols" {g}>{cols}</div><div class="cols-l" {g}>{labels}</div>{note}')


def legend(series):
    return '<div class="legend">' + "".join(f'<span><i style="background:{PALETTE[k % len(PALETTE)]}"></i>{esc(s["name"])}</span>'
                                            for k, s in enumerate(series)) + "</div>"


def line(c):
    labels, series = c["labels"], c["series"][:4]
    vals = [v for s in series for v in s["values"] if isinstance(v, (int, float))]
    lo, hi = min(0, min(vals)), max(vals) * 1.12 or 1
    W, H, L, B, T = 640, 250, 46, 30, 12
    n = max(len(labels) - 1, 1)
    x = lambda k: L + (W - L - 12) * k / n
    y = lambda v: T + (H - T - B) * (1 - (v - lo) / (hi - lo))
    grid = ""
    for g in range(5):
        gv = lo + (hi - lo) * g / 4
        grid += (f'<line x1="{L}" x2="{W - 12}" y1="{y(gv):.1f}" y2="{y(gv):.1f}" stroke="#E5E7EB" stroke-width="1"/>'
                 f'<text x="{L - 6}" y="{y(gv) + 3:.1f}" text-anchor="end" font-size="10" fill="#6B7280">{fmt(round(gv, 1))}</text>')
    step = max(1, len(labels) // 10)
    xl = "".join(f'<text x="{x(k):.1f}" y="{H - 10}" text-anchor="middle" font-size="9.5" fill="#374151">{esc(str(l))}</text>'
                 for k, l in enumerate(labels) if k % step == 0 or k == len(labels) - 1)
    paths = ""
    for si, s in enumerate(series):
        col = PALETTE[si % len(PALETTE)]
        pts = [(x(k), y(v)) for k, v in enumerate(s["values"]) if isinstance(v, (int, float))]
        if not pts:
            continue
        paths += f'<polyline fill="none" stroke="{col}" stroke-width="2.6" points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}"/>'
        paths += "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="2.6" fill="{col}"/>' for a, b in pts)
        lastk = max(k for k, v in enumerate(s["values"]) if isinstance(v, (int, float)))
        paths += (f'<text x="{x(lastk) - 4:.1f}" y="{y(s["values"][lastk]) - 7:.1f}" text-anchor="end" font-size="10" font-weight="700" '
                  f'fill="{col}">{fmt(s["values"][lastk])}</text>')
    svg = (f'<svg viewBox="0 0 {W} {H}" width="100%" style="font-family:BVP,sans-serif">{grid}{xl}{paths}</svg>')
    u = c.get("unit")
    return fig_wrap(c, (legend(series) if len(series) > 1 else "") + svg + (f'<div class="src" style="margin-top:0">Đơn vị: {esc(u)}</div>' if u else ""))


def stacked(c):
    labels, series = c["labels"], c["series"]
    rows = ""
    for k, lab in enumerate(labels):
        vals = [s["values"][k] if k < len(s["values"]) and isinstance(s["values"][k], (int, float)) else 0 for s in series]
        tot = sum(vals) or 1
        segs = "".join(f'<div style="width:{v / tot * 100:.2f}%;background:{PALETTE[si % len(PALETTE)]}">{fmt(round(v, 1)) if v / tot > .07 else ""}</div>'
                       for si, v in enumerate(vals))
        rows += f'<div class="stk"><div>{esc(str(lab))}</div><div class="t">{segs}</div></div>'
    return fig_wrap(c, legend(series) + rows)


def table(c):
    cols = c["columns"]
    num = [all(isinstance(r[j], (int, float)) or (isinstance(r[j], str) and r[j].replace(".", "").replace(",", "").replace("%", "").replace("+", "").replace("-", "").strip().isdigit())
               for r in c["rows"] if j < len(r)) for j in range(len(cols))]
    th = "".join(f'<th class="{"n" if num[j] and j else ""}">{esc(str(h))}</th>' for j, h in enumerate(cols))
    trs = "".join("<tr>" + "".join(f'<td class="{"n" if num[j] and j else ""}">{esc(fmt(v) if isinstance(v, (int, float)) else str(v))}</td>'
                                   for j, v in enumerate(r)) + "</tr>" for r in c["rows"])
    return fig_wrap(c, f'<table class="t"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>')


def visual(c):
    if not c:
        return ""
    t = c.get("type", "bar")
    return {"column": columns, "line": line, "stacked": stacked, "table": table}.get(t, chart)(c)


def section_html(s, sub=False, page=False):
    out = [f'<div class="sec{" pg" if page else ""}"><h2 class="{"sub" if sub else ""}">{esc(s["heading"])}</h2>']
    out.append(visual(s.get("visual") or s.get("chart")))
    out += [f'<p class="body">{esc(p)}</p>' for p in s.get("body", [])]
    if s.get("bullets"):
        out.append('<ul class="b">' + "".join(f"<li>{esc(b)}</li>" for b in s["bullets"]) + "</ul>")
    if s.get("callout"):
        out.append(f'<div class="callout"><small>Nhận định của Adtek</small>{esc(s["callout"])}</div>')
    out.append("</div>")
    return "".join(out)


def deep_body(r):
    """Thân báo cáo chuyên sâu: tóm tắt điều hành, các chương (trang mở chương + mục), phụ lục, nguồn.
    Mỗi trang mở chương có dấu CH-<số> ẩn để tìm số trang dựng mục lục."""
    out = [head(r["title"]), '<div class="wrap">']
    ex = r["executive"]
    out.append('<div class="eyebrow">Tóm tắt điều hành</div><h2>Mười phát hiện chính</h2><div class="rule"></div>')
    out.append(visual(ex.get("dashboard")))
    out.append('<ol class="sum">' + "".join(f"<li>{esc(x)}</li>" for x in ex["findings"]) + "</ol>")
    for ch in r["chapters"]:
        n = ch["number"]
        out.append(f'<div class="opener"><div class="eyebrow">Chương {n:02d}<span style="color:#fff;font-size:1pt">CH-{n:02d}</span></div>'
                   f'<div class="no">{n:02d}</div><h1>{esc(ch["title"])}</h1><p>{esc(ch.get("intro", ""))}</p>'
                   f'<ol>{"".join(f"<li>{esc(s["heading"])}</li>" for s in ch["sections"])}</ol></div>')
        out += [section_html(s, page=True) for s in ch["sections"]]  # mỗi mục một trang mới: tiêu đề, hình, diễn giải, nhận định
    ap = r.get("appendix") or {}
    out.append('<div class="opener"><div class="eyebrow">Phụ lục<span style="color:#fff;font-size:1pt">CH-AP</span></div>'
               '<h1>Bảng số liệu, thuật ngữ và nguồn</h1></div><div class="page"></div>')
    out += [visual(t) for t in ap.get("tables", [])]
    if ap.get("glossary"):
        out.append('<div class="sec"><h2 class="sub">Thuật ngữ</h2><dl class="gl">' +
                   "".join(f'<dt>{esc(g["term"])}</dt><dd>{esc(g["def"])}</dd>' for g in ap["glossary"]) + "</dl></div>")
    out.append('<div class="page"></div><div class="sec"><h2 class="sub">Nguồn dữ liệu</h2><ol class="srcs two">')
    out += [f'<li>{esc(s["publisher"])}, {esc(s["name"])}{", " + esc(s["date"]) if s.get("date") else ""}.'
            f'{"<br><span class=u>" + esc(s["url"]) + "</span>" if s.get("url") else ""}</li>' for s in r["sources"]]
    out.append(f'</ol><div class="note">Báo cáo do Adtek tổng hợp và phân tích từ các nguồn công khai nêu trên, số liệu cập nhật tới '
               f'{esc(r["period"].replace("Cập nhật ", ""))}. Số liệu thuộc về đơn vị công bố; các đơn vị dùng phương pháp đo khác nhau nên con số có thể chênh lệch. '
               "Dự báo và mô hình là ước tính của Adtek dựa trên giả định nêu trong báo cáo. Tài liệu dùng để tham khảo, không thay thế tư vấn chuyên môn hoặc pháp lý.</div></div>")
    out.append("</div></body></html>")
    return "".join(out)


def toc_page(r, pages):
    """Mục lục; pages: {"01": số trang, ..., "AP": số trang} (đánh số theo chân trang phần thân)."""
    rows = [("", "Tóm tắt điều hành", 1)] + [(f'{c["number"]:02d}', c["title"], pages.get(f'{c["number"]:02d}', "")) for c in r["chapters"]]
    rows.append(("", "Phụ lục: bảng số liệu, thuật ngữ và nguồn", pages.get("AP", "")))
    li = "".join(f'<li><span class="n">{n}</span><span>{esc(t)}</span><span class="p">{p}</span></li>' for n, t, p in rows)
    return f'{head(r["title"])}<div class="wrap" style="padding-top:16mm"><div class="eyebrow">Mục lục</div><h2>Nội dung báo cáo</h2><div class="rule"></div><ol class="toc">{li}</ol></div></body></html>'


def chapter_pages(pdf_path):
    from pypdf import PdfReader
    import re
    found = {}
    for i, pg in enumerate(PdfReader(str(pdf_path)).pages, 1):
        for m in re.findall(r"CH-(\d\d|AP)", re.sub(r"\s+", "", pg.extract_text() or "")):  # pypdf tách chữ cách quãng
            found.setdefault(m, i)
    return found


def back_page(r):
    bg, fg, panel, card, pfg, numc = theme(r)
    rows = "".join(f'<div style="display:grid;grid-template-columns:30mm 1fr;padding:1.6mm 0"><b style="font-weight:600">{k}</b><span>{v}</span></div>'
                   for k, v in (("Website", "adtek.agency"), ("Email", "contact@adtek.agency"), ("Tài nguyên", "adtek.agency/resources-report")))
    content = f"""<div class="lab">Liên hệ</div><div style="font-size:12pt;margin-top:4mm">{rows}</div>
<div style="margin-top:auto;font-size:8pt;line-height:1.5;opacity:.7">© 2026 Adtek. Tài liệu được chia sẻ miễn phí, vui lòng ghi nguồn khi trích dẫn.</div>"""
    return f"""{head(r["title"])}<style>{FULL_CSS}</style><div class="full" style="background:{bg};color:{fg}">
{logo_img(fg)}
<div style="position:absolute;left:18mm;right:24mm;top:60mm">
 <div class="lab">Về Adtek</div>
 <h1 style="font-size:34pt;line-height:1.08;margin:6mm 0 8mm">Biến dữ liệu thị trường thành <span class="hl">kế hoạch tăng trưởng</span> cho doanh nghiệp của bạn</h1>
 <div style="font-size:11.5pt;line-height:1.6;opacity:.85;max-width:155mm">Adtek là Growth Marketing Agency với hơn 100 khách hàng và 200 dự án. Đội ngũ Adtek triển khai quảng cáo tìm kiếm và mạng xã hội, thương mại điện tử, SEO và tạo khách hàng tiềm năng, đo lường bằng doanh thu thay vì lượt hiển thị.</div>
</div>
{block(r, 96, content)}
</div></body></html>"""


def thumb(r):
    """Ảnh đại diện 1245x825 theo series "Báo cáo Adtek" trong tools/covers.py (report_cover)."""
    return report_cover(r)


def build(slug):
    r = json.loads((DIR / f"{slug}.json").read_text(encoding="utf-8"))
    tmp = ROOT / "previews/_report"
    tmp.mkdir(parents=True, exist_ok=True)
    deep = "chapters" in r  # báo cáo chuyên sâu: có mục lục và trang mở chương
    parts = {"cover": cover_page(r), "body": deep_body(r) if deep else body_page(r), "back": back_page(r)}
    for k, v in parts.items():
        (tmp / f"{k}.html").write_text(v, encoding="utf-8")
    foot = f"Adtek  |  {r.get('short_title') or r['title']}"
    jobs = [{"input": str(tmp / "cover.html"), "output": str(tmp / "cover.pdf")},
            {"input": str(tmp / "body.html"), "output": str(tmp / "body.pdf"), "margin": "16mm", "footer": esc(foot)},
            {"input": str(tmp / "back.html"), "output": str(tmp / "back.pdf")}]
    (tmp / "jobs.json").write_text(json.dumps(jobs), encoding="utf-8")
    subprocess.run(["node", str(ROOT / "tools/render_pdf.js"), str(tmp / "jobs.json")], check=True)
    order = ["cover", "body", "back"]
    if deep:  # mục lục dựng sau, khi đã biết số trang từng chương trong phần thân
        (tmp / "toc.html").write_text(toc_page(r, chapter_pages(tmp / "body.pdf")), encoding="utf-8")
        (tmp / "jobs.json").write_text(json.dumps([{"input": str(tmp / "toc.html"), "output": str(tmp / "toc.pdf"), "margin": "16mm"}]), encoding="utf-8")
        subprocess.run(["node", str(ROOT / "tools/render_pdf.js"), str(tmp / "jobs.json")], check=True)
        order = ["cover", "toc", "body", "back"]
    shoot([(thumb(r), DIR / f"{slug}-cover.jpg", *REPORT_SIZE)])  # ảnh đại diện: cùng bộ dựng với ảnh bìa blog (co chữ, logo)
    w = PdfWriter()
    for k in order:
        w.append(str(tmp / f"{k}.pdf"))
    w.add_metadata({"/Title": r["title"], "/Author": "Adtek", "/Subject": r["subtitle"]})
    out = DIR / f"{slug}.pdf"
    with open(out, "wb") as f:
        w.write(f)
    for p in tmp.iterdir():
        p.unlink()
    tmp.rmdir()
    print(out, f"{out.stat().st_size // 1024} KB", f"{len(w.pages)} trang")


if __name__ == "__main__":
    args = sys.argv[1:]
    only_thumb = "--thumb" in args
    args = [a for a in args if a != "--thumb"]
    slugs = [p.stem for p in sorted(DIR.glob("*.json"))] if args == ["all"] else args
    for s in slugs:
        if only_thumb:
            r = json.loads((DIR / f"{s}.json").read_text(encoding="utf-8"))
            print(shoot([(thumb(r), DIR / f"{s}-cover.jpg", *REPORT_SIZE)])[0])
        else:
            build(s)
