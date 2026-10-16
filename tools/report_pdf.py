"""Dựng báo cáo PDF cho Trung Tâm Tài Nguyên (https://adtek.agency/resources-report/) từ file JSON nội dung.

Nội dung: content/reports/<slug>.json (cấu trúc: title, subtitle, period, key_stats, summary, sections, implications, sources).
Kết quả (cùng thư mục):
  <slug>.pdf         báo cáo A4: bìa, tóm tắt, các phần, khuyến nghị, nguồn, trang Về Adtek
  <slug>-cover.jpg   ảnh đại diện trên WordPress 1245x825 (trang danh sách cắt giữa còn tỉ lệ 370x250)

Cách dùng:
  python3 tools/report_pdf.py <slug> [<slug> ...]
  python3 tools/report_pdf.py all
"""
import html
import json
import subprocess
import sys
from pathlib import Path

from pypdf import PdfWriter

from covers import ASSETS, NAVY, ORANGE, font_css

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
figure{{margin:5mm 0 3mm;break-inside:avoid;border-top:.3mm solid {NAVY};padding-top:3mm}}
figcaption{{font-weight:700;color:{NAVY};font-size:9.6pt;margin-bottom:3mm}}
.bar{{display:grid;grid-template-columns:40% 1fr 22mm;align-items:center;gap:3mm;margin-bottom:2mm;font-size:8.8pt}}
.bar .t{{height:4.2mm;background:#EEF1F6}}
.bar .f{{height:100%;background:{NAVY}}}
.bar.top .f{{background:{ORANGE}}}
.bar.neg .f{{background:#9CA3AF}}
.bar .v{{font-weight:700;color:{NAVY};text-align:right;font-variant-numeric:tabular-nums}}
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
.note{{font-size:8pt;color:{MUTED};margin-top:6mm;border-top:.3mm solid {LINE};padding-top:3mm}}
.full{{width:210mm;height:297mm;position:relative;overflow:hidden;background:{NAVY};color:#fff}}
"""


def head(title):
    return f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>{esc(title)}</title><style>{CSS}</style></head><body>'


def cover_page(r):
    stats = "".join(f'<div><div class="nr" style="font-size:18pt;color:{ORANGE};line-height:1.1;white-space:nowrap">{esc(s["value"])}</div>'
                    f'<div style="font-size:8.6pt;margin-top:1.5mm;color:#D6DEEB">{esc(s["label"])}</div></div>'
                    for s in r["key_stats"][:3])
    return f"""{head(r["title"])}<div class="full">
<div style="position:absolute;right:-70mm;top:-55mm;width:190mm;height:190mm;border-radius:50%;border:16mm solid {ORANGE};opacity:.95"></div>
<div style="position:absolute;right:-40mm;top:-25mm;width:130mm;height:130mm;border-radius:50%;border:.5mm solid rgba(255,255,255,.35)"></div>
<img src="{uri("adtek-logo-white.png")}" alt="Adtek" style="position:absolute;left:18mm;top:18mm;height:17mm">
<div style="position:absolute;left:18mm;right:22mm;top:112mm">
 <div class="eyebrow" style="color:{ORANGE}">Báo cáo Adtek &nbsp;|&nbsp; {esc(r["period"])}</div>
 <div class="nr" style="font-size:33pt;line-height:1.12;margin:5mm 0 6mm;text-wrap:balance">{esc(r["title"])}</div>
 <div style="height:1.2mm;width:22mm;background:{ORANGE};margin-bottom:6mm"></div>
 <div style="font-size:12.5pt;line-height:1.5;color:#D6DEEB;max-width:150mm">{esc(r["subtitle"])}</div>
</div>
<div style="position:absolute;left:18mm;right:18mm;bottom:30mm;display:grid;grid-template-columns:repeat(3,1fr);gap:8mm;border-top:.3mm solid rgba(255,255,255,.35);padding-top:5mm">{stats}</div>
<div style="position:absolute;left:18mm;right:18mm;bottom:14mm;display:flex;justify-content:space-between;font-size:8.5pt;color:#B7C3D8">
 <span>adtek.agency</span><span>Growth Marketing Agency</span></div>
</div></body></html>"""


def chart(c):
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
        out.append(f'<section class="page"><div class="eyebrow">Phần {n:02d}</div><h2>{esc(s["heading"])}</h2><div class="rule"></div>'
                   f'<p class="lead">{esc(s["lead"])}</p><ul class="b">' + "".join(f"<li>{esc(b)}</li>" for b in s["bullets"]) + "</ul>")
        if s.get("chart"):
            out.append(chart(s["chart"]))
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


def back_page(r):
    return f"""{head(r["title"])}<div class="full">
<div style="position:absolute;left:-70mm;bottom:-95mm;width:160mm;height:160mm;border-radius:50%;border:14mm solid {ORANGE}"></div>
<img src="{uri("adtek-logo-white.png")}" alt="Adtek" style="position:absolute;left:18mm;top:18mm;height:17mm">
<div style="position:absolute;left:18mm;right:24mm;top:80mm">
 <div class="eyebrow">Về Adtek</div>
 <div class="nr" style="font-size:26pt;line-height:1.18;margin:4mm 0 6mm;text-wrap:balance">Biến dữ liệu thị trường thành kế hoạch tăng trưởng cho doanh nghiệp của bạn</div>
 <div style="font-size:11pt;line-height:1.6;color:#D6DEEB;max-width:150mm">Adtek là Growth Marketing Agency với hơn 100 khách hàng và 200 dự án. Đội ngũ Adtek triển khai quảng cáo tìm kiếm và mạng xã hội, thương mại điện tử, SEO và tạo khách hàng tiềm năng, đo lường bằng doanh thu thay vì lượt hiển thị.</div>
 <div style="margin-top:12mm;font-size:10.5pt;line-height:1.9">
  <div><span style="color:{ORANGE};font-weight:700">Website</span>&nbsp;&nbsp; adtek.agency</div>
  <div><span style="color:{ORANGE};font-weight:700">Email</span>&nbsp;&nbsp; contact@adtek.agency</div>
  <div><span style="color:{ORANGE};font-weight:700">Tài nguyên</span>&nbsp;&nbsp; adtek.agency/resources-report</div>
 </div>
</div>
<div style="position:absolute;right:18mm;bottom:14mm;max-width:95mm;text-align:right;font-size:8pt;line-height:1.5;color:#B7C3D8">© 2026 Adtek. Tài liệu được chia sẻ miễn phí, vui lòng ghi nguồn khi trích dẫn.</div>
</div></body></html>"""


def thumb(r):
    s = r["key_stats"][0]
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
body{{width:1245px;height:825px;overflow:hidden;background:{NAVY};color:#fff;position:relative}}</style></head><body>
<div style="position:absolute;right:-300px;top:-280px;width:600px;height:600px;border-radius:50%;border:56px solid {ORANGE}"></div>
<div style="position:absolute;left:150px;right:420px;top:150px">
 <div class="eyebrow" style="font-size:20px">Báo cáo Adtek &nbsp;|&nbsp; {esc(r["period"])}</div>
 <div class="nr" style="font-size:60px;line-height:1.1;margin:22px 0 26px;text-wrap:balance">{esc(r.get("short_title") or r["title"])}</div>
 <div style="height:6px;width:90px;background:{ORANGE};margin-bottom:26px"></div>
 <div class="nr" style="font-size:46px;color:{ORANGE};line-height:1">{esc(s["value"])}</div>
 <div style="font-size:21px;color:#D6DEEB;margin-top:10px">{esc(s["label"])}</div>
</div>
<img src="{uri("adtek-logo-white.png")}" alt="Adtek" style="position:absolute;right:150px;bottom:80px;height:78px">
<div style="position:absolute;left:150px;bottom:92px;font-size:20px;font-weight:600;letter-spacing:.06em;color:#fff">TẢI MIỄN PHÍ</div>
</body></html>"""


def build(slug):
    r = json.loads((DIR / f"{slug}.json").read_text(encoding="utf-8"))
    tmp = ROOT / "previews/_report"
    tmp.mkdir(parents=True, exist_ok=True)
    parts = {"cover": cover_page(r), "body": body_page(r), "back": back_page(r), "thumb": thumb(r)}
    for k, v in parts.items():
        (tmp / f"{k}.html").write_text(v, encoding="utf-8")
    foot = f"Adtek  |  {r.get('short_title') or r['title']}"
    jobs = [{"input": str(tmp / "cover.html"), "output": str(tmp / "cover.pdf")},
            {"input": str(tmp / "body.html"), "output": str(tmp / "body.pdf"), "margin": "16mm", "footer": esc(foot)},
            {"input": str(tmp / "back.html"), "output": str(tmp / "back.pdf")},
            {"input": str(tmp / "thumb.html"), "output": str(DIR / f"{slug}-cover.jpg"), "kind": "jpg", "width": 1245, "height": 825}]
    (tmp / "jobs.json").write_text(json.dumps(jobs), encoding="utf-8")
    subprocess.run(["node", str(ROOT / "tools/render_pdf.js"), str(tmp / "jobs.json")], check=True)
    w = PdfWriter()
    for k in ("cover", "body", "back"):
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
    slugs = [p.stem for p in sorted(DIR.glob("*.json"))] if sys.argv[1:] == ["all"] else sys.argv[1:]
    for s in slugs:
        build(s)
