"""Bộ mẫu ảnh bìa Adtek: nhiều phong cách, mỗi bài một phong cách khác bài trước.

Mỗi phong cách dựng được 2 khổ từ cùng dữ liệu cover trong calendar.json:
  blog  bố cục 1200x630, file 2400x1260 (ảnh đại diện WordPress, ảnh xem trước khi chia sẻ link)
  fb    1080x1080 (ảnh bài đăng Facebook)

Dữ liệu dùng: cover.kicker, title, subtitle, chips (blog); cover.fb_kicker, hero, hero_text, subtitle (fb).
cover.style: phong cách của bài. Bỏ trống thì lần dựng đầu tiên tự chọn (pick) rồi ghi lại; muốn đổi thì sửa tay.
Lệnh dựng ảnh thật: python3 tools/blog_post.py cover X (blog) và python3 tools/fb_post.py cover X (Facebook).

Cách dùng:
  python3 tools/covers.py styles                     liệt kê phong cách
  python3 tools/covers.py pick                       xem phong cách tự chọn cho từng bài đã có cover
  python3 tools/covers.py render <số bài> [--style X] [--kind blog|fb|all] [--out thư-mục]   dựng thử, không ghi cover.style
  python3 tools/covers.py sheet <số bài> [--out thư-mục]   dựng mọi phong cách cho một bài để so sánh
  python3 tools/covers.py existing <wp_id>           dựng ảnh bìa blog cho bài cũ trong mục existing (vd 6076, 6078)
"""
import base64
import html
import json
import re
import subprocess
import sys
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "tools/assets"
SIZES = {"blog": (1200, 630), "fb": (1080, 1080)}  # kích thước bố cục (px CSS)
SCALE = {"blog": 2, "fb": 1}  # ảnh bìa blog xuất gấp đôi (2400x1260) cho khung 870px trên màn Retina; ảnh Facebook giữ 1080
# Khổ blog: trang danh sách bài của WordPress cắt giữa ảnh còn 370x250, mất khoảng 134px mỗi bên ảnh 1200x630.
# Trang /blog/ cắt ảnh thành 870x362 (tỉ lệ 2.4:1), mất khoảng 65px ở mép trên và mép dưới.
# Vùng an toàn cho chữ và logo khổ ngang: x 140 đến 1060, y 70 đến 560; chỉ họa tiết được tràn ra ngoài vùng này.
NAVY, ORANGE, CREAM = "#002D72", "#FF9014", "#F4EEE3"
esc = html.escape

HEAD = Template("""<!doctype html><html><head><meta charset="utf-8"><style>
$fontcss
*{box-sizing:border-box;margin:0;padding:0}
body{width:${w}px;height:${h}px;overflow:hidden;position:relative;font-family:IT,sans-serif;-webkit-font-smoothing:antialiased}
.fit{overflow:hidden;padding-top:.1em}.bal{text-wrap:balance}.abs{position:absolute}
.logo{aspect-ratio:440/369;-webkit-mask:url($logo) center/contain no-repeat;mask:url($logo) center/contain no-repeat}
.mark{-webkit-mask:url($mark) center/contain no-repeat;mask:url($mark) center/contain no-repeat}
$css
/* Chữ (theo mẫu anh Tin gửi 16/10/2026): tiêu đề Inter Tight đậm vừa, viết thường như câu, một từ khóa tô màu nhấn (.hl);
   mô tả Inter Tight nét thường; con số và cụm chữ đọc liền sau số (.cap, .phrase) dùng Newsreader có chân.
   Đặt sau CSS của từng phong cách để thống nhất kiểu chữ cho cả bộ. */
h1,h2,.name{font-family:IT,sans-serif;font-weight:600;text-transform:none;letter-spacing:-.02em}
.num,.cap,.phrase,.vs{font-family:NR,serif;font-weight:600;text-transform:none;letter-spacing:-.012em}
:where(.hl){color:#FF9014}  /* độ ưu tiên 0: mẫu nền cam ghi đè .hl{color:inherit} được */
.num{letter-spacing:-.03em;font-variant-numeric:lining-nums}
.kicker+.num{margin-top:.1em}  /* phần trên của chữ số cao hơn khung dòng, chừa chỗ để không chạm nhãn */
.kicker{font-weight:600;letter-spacing:0}
.sub,.band,p{font-weight:400}
</style></head><body class="$shape" data-fit="1">$body
<script>
// Co chữ: giảm cỡ chữ của .fit tới khi không tràn khung (chữ tiếng Việt dài ngắn khác nhau từng bài)
function fit(el){const cs=getComputedStyle(el);let s=parseFloat(cs.fontSize);const min=s*.45,lim=parseFloat(cs.maxHeight)||el.clientHeight;
 el.style.maxHeight=lim+"px";  // chốt khung theo px trước khi co (khung tính bằng em sẽ co theo chữ)
 while((el.scrollHeight>lim+2||el.scrollWidth>el.clientWidth+2)&&s>min){s-=1;el.style.fontSize=s+"px"}}
document.fonts.ready.then(()=>{document.querySelectorAll(".fit").forEach(fit);document.body.dataset.done=1});
</script></body></html>""")


VI = "U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB"
LATIN = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"


FONTS = {"IT": ("inter-tight", (400, 500, 600, 700)), "NR": ("newsreader", (500, 600)), "BVP": ("be-vietnam-pro", (400, 500, 600, 700, 800, 900))}


def font_css():
    """Mỗi font tách 2 file (tiếng Việt, Latin): mỗi file một @font-face kèm unicode-range.
    IT = Inter Tight (tiêu đề, nhãn, mô tả), NR = Newsreader (con số và cụm chữ đi liền sau số), BVP = Be Vietnam Pro (mẫu cũ neon3d)."""
    d = (ASSETS / "fonts").as_uri()
    return "\n".join(f"@font-face{{font-family:{fam};font-weight:{w};src:url({d}/{file}-{sub}-{w}-normal.woff2);unicode-range:{r}}}"
                     for fam, (file, weights) in FONTS.items() for w in weights for sub, r in (("vietnamese", VI), ("latin", LATIN)))


def logo(color, height, extra=""):
    return f'<div class="logo" style="height:{height}px;background:{color};{extra}"></div>'


def hl(text):
    """Thoát HTML rồi đổi *từ khóa* thành phần tô màu nhấn."""
    return re.sub(r"\*(.+?)\*", r'<span class="hl">\1</span>', esc(text))


def plain(text):
    return esc(text.replace("*", ""))


def fields(post, kind):
    c = post["cover"]
    fb = kind == "fb"
    return {
        "kicker": esc((c.get("fb_kicker") or c["kicker"]) if fb else c["kicker"]),
        "head": hl((c.get("hero_text") or c["title"]) if fb else c["title"]),
        "num": esc(c.get("hero") or f"{post['no']:02d}"),
        "cap": hl(c.get("hero_text") or ""),
        # paired: tiêu đề chính là cụm chữ đọc liền sau con số (khổ Facebook), nên số phải đứng ngay trước tiêu đề
        "paired": fb and bool(c.get("hero_text")),
        "title": plain(c["title"]),
        "sub": hl(c["subtitle"]),
        "chips": [esc(x) for x in c.get("chips", [])[:4]],
        "no": post["no"],
        "date": ".".join(reversed(post["date"].split("-")[1:])) + "." + post["date"][:4],
    }


# ---------------------------------------------------------------- phong cách

def neon3d(f, sq):
    """Tím neon 3D: mẫu Facebook anh Tin đã duyệt 16/10/2026."""
    num, head = f["num"], f["head"]
    side = len(num) <= 2
    hero = (380 if len(num) == 1 else 310) if side else 250 if len(num) <= 4 else 190
    if sq:
        k = .88
        v = dict(pad=64, padb=64, logo=104, kick=34 * k, sub=38 * k, gap=56, bodyb=40, hero=hero * k, side=44,
                 tsize=(86 if len(head) <= 16 else 76 if len(head) <= 28 else 68) * k, boxpad="30px 38px", rad=30)
    else:
        v = dict(pad=44, padb=44, logo=74, kick=24, sub=26, gap=26, bodyb=0, hero=hero * .62, side=36,
                 tsize=58 if len(head) <= 20 else 50, boxpad="20px 30px", rad=24)
    grid = "".join(f'<path d="M0 {y} H1000" stroke-opacity="{0.15 + y / 900:.2f}"/>' for y in (20, 55, 100, 160, 240, 340, 470))
    grid += "".join(f'<path d="M500 0 L{x} 500" stroke-opacity=".35"/>' for x in range(-900, 1901, 200))
    css = f"""
body{{color:#fff;background:radial-gradient(ellipse 70% 38% at 50% 0%,rgba(255,255,255,.38),transparent 70%),
linear-gradient(180deg,#A9ABF6 0%,#8384DA 34%,#4A4CA3 66%,#1E2056 100%)}}
.grid{{position:absolute;left:0;right:0;bottom:0;height:38%;opacity:.4}}
.horizon{{position:absolute;left:8%;right:8%;bottom:38%;height:2px;background:linear-gradient(90deg,transparent,rgba(170,215,255,.9),transparent);filter:blur(1px)}}
.wrap{{position:absolute;inset:{v['pad']}px 80px {v['padb']}px;display:flex;flex-direction:column;align-items:center}}
.ls .wrap{{align-items:flex-start;left:140px;right:140px}}
.body{{flex:1;width:100%;display:flex;flex-direction:column;justify-content:center;gap:{v['gap']}px;padding-bottom:{v['bodyb']}px}}
.main{{width:100%;display:flex;align-items:center;justify-content:center;gap:{v['side']}px}}
.ls .main{{justify-content:flex-start}}
.stack .main{{flex-direction:column;gap:16px}}
.side .text{{text-align:left;flex:1}}.stack .text{{text-align:center}}
.kicker{{color:#D3E7FF;font-weight:800;font-size:{v['kick']:.0f}px;letter-spacing:3px;text-transform:uppercase}}
.hero{{position:relative;flex:none;font-weight:900;font-size:{v['hero']:.0f}px;line-height:.9;letter-spacing:-4px;
background:linear-gradient(165deg,#FFFFFF 8%,#F6DCF2 38%,#CDB8F2 62%,#8F8CE4 88%);-webkit-background-clip:text;background-clip:text;color:transparent;
filter:drop-shadow(1px 1px 0 #6F6FC8) drop-shadow(2px 2px 0 #5E5EB6) drop-shadow(3px 3px 0 #5052A4) drop-shadow(4px 4px 0 #444694)
drop-shadow(5px 6px 0 #3A3C85) drop-shadow(0 18px 26px rgba(10,12,50,.55)) drop-shadow(0 0 30px rgba(140,205,255,.45))}}
.title{{margin-top:12px;font-weight:900;font-size:{v['tsize']:.0f}px;line-height:1.14;text-transform:uppercase;text-shadow:0 4px 18px rgba(20,20,70,.45);max-height:3.6em}}
.box{{width:100%;border:2px solid rgba(255,255,255,.9);border-radius:{v['rad']}px;padding:{v['boxpad']};background:rgba(255,255,255,.12);
font-weight:700;font-size:{v['sub']:.0f}px;line-height:1.38;text-align:left;text-shadow:0 2px 10px rgba(20,20,70,.4);max-height:4.4em}}"""
    body = f"""<svg class="grid" viewBox="0 0 1000 500" preserveAspectRatio="none" fill="none" stroke="#9FD4FF" stroke-width="1.4">{grid}
<path d="M120 380 h160 a18 18 0 0 0 18 -18 v-40 h120 M880 420 h-150 a18 18 0 0 1 -18 -18 v-30 h-110 M60 470 h300 M640 470 h300" stroke-opacity=".7"/>
<rect x="330" y="400" width="340" height="70" rx="16" stroke-opacity=".5"/></svg><div class="horizon"></div>
<div class="wrap {'side' if side else 'stack'}">{logo('#fff', v['logo'])}<div class="body"><div class="main"><div class="hero">{num}</div>
<div class="text"><div class="kicker">{f['kicker']}</div><div class="title fit bal">{f['cap'] if not sq and f['cap'] else head}</div></div></div>
<div class="box fit">{f['sub']}</div></div></div>"""
    return css, body


def editorial(f, sq):
    """Tạp chí: nền kem phẳng, số cam lớn đặt ngay trên cụm chữ đi kèm, chữ navy."""
    n = len(f["num"])
    chips = " &nbsp;·&nbsp; ".join(f["chips"][:3])
    if f["paired"]:  # số đọc liền với tiêu đề: số ở trên, tiêu đề ngay dưới
        hero = 400 if n == 1 else 340 if n == 2 else 230
        main = f"""<div class="copy"><div class="kicker">{f['kicker']}</div><div class="num">{f['num']}</div>
<h1 class="fit bal phrase">{f['head']}</h1><div class="sub fit">{f['sub']}</div></div>"""
    else:  # tiêu đề riêng; số và cụm chữ của nó thành một khối bên phải, số trên chữ dưới
        hero = 300 if n == 1 else 230 if n == 2 else 160
        unit = f'<div class="unit"><div class="num">{f["num"]}</div><div class="cap fit bal">{f["cap"]}</div></div>' if f["cap"] else ""
        main = f"""<div class="copy"><div class="kicker">{f['kicker']}</div><h1 class="fit bal">{f['head']}</h1><div class="sub fit">{f['sub']}</div></div>{unit}"""
    css = f"""
body{{background:{CREAM};color:{NAVY}}}
.meta{{position:absolute;text-align:right;font-weight:700;line-height:1.45;color:{NAVY}}}
.meta b{{font-weight:800;color:{ORANGE}}}
.num{{font-size:{hero}px;line-height:.8;color:{ORANGE};white-space:nowrap}}
.copy,.unit{{position:absolute}}
.kicker{{color:{ORANGE}}}
h1{{line-height:1.12}}
.sub{{line-height:1.42;color:rgba(0,45,114,.75)}}
.cap{{line-height:1.15;margin-top:-8px;max-height:3.6em}}
.foot{{position:absolute;display:flex;justify-content:space-between;font-weight:700;color:rgba(0,45,114,.6)}}
.sq .lg{{position:absolute;left:72px;top:64px}}.sq .meta{{right:72px;top:70px;font-size:20px}}
.sq .copy{{left:72px;right:72px;top:150px;bottom:120px;display:flex;flex-direction:column;justify-content:center}}
.sq .kicker{{font-size:30px;margin-bottom:22px}}
.sq h1{{font-size:104px;margin:-.12em 0 24px;max-height:3.4em}}
.sq .sub{{font-size:34px;max-width:860px;max-height:3em}}
.sq .foot{{left:72px;right:72px;bottom:64px;font-size:22px}}
.ls .lg{{position:absolute;left:140px;top:84px}}.ls .meta{{right:140px;top:88px;font-size:15px}}
.ls .copy{{left:140px;top:178px;width:520px}}
.ls .kicker{{font-size:22px}}
.ls h1{{font-size:76px;margin:10px 0 16px;max-height:2.3em}}
.ls .sub{{font-size:25px;max-height:4.4em}}
.ls .unit{{left:740px;right:140px;top:178px}}
.ls .cap{{font-size:28px}}
.ls .foot{{left:140px;right:140px;bottom:80px;font-size:17px}}"""
    body = f"""<div class="lg">{logo(NAVY, 78 if sq else 58)}</div><div class="meta"><b>Adtek Insights</b><br>Số {f['no']:02d}, {f['date']}</div>
{main}<div class="foot"><div>{chips}</div><div>adtek.agency</div></div>"""
    return css, body


def split(f, sq):
    """Khối tương phản: mảng cam cắt chéo chứa số navy và cụm chữ đi kèm ngay bên phải hoặc ngay bên dưới số."""
    n = len(f["num"])
    chips = " &nbsp;·&nbsp; ".join(f["chips"][:3])
    if sq:
        hero = 400 if n == 1 else 330 if n == 2 else 220
        css = f"""
body{{background:{NAVY};color:#fff}}
.panel{{position:absolute;left:0;top:0;right:0;height:580px;background:{ORANGE};clip-path:polygon(0 0,100% 0,100% 72%,0 100%)}}
.unit{{position:absolute;left:64px;right:72px;top:150px;display:flex;align-items:flex-end;gap:30px}}
.num{{flex:none;font-size:{hero}px;line-height:.8;color:{NAVY};white-space:nowrap}}
.cap{{flex:1;font-size:56px;line-height:1.1;color:{NAVY};max-height:3.4em;padding-bottom:6px}}
.cap .hl{{color:inherit}}
.lg{{position:absolute;right:72px;top:56px}}
.copy{{position:absolute;left:72px;right:72px;bottom:72px}}
.kicker{{color:{ORANGE};font-size:30px}}
h1{{font-size:68px;line-height:1.14;margin:12px 0 20px;max-height:3.5em}}
.sub{{font-size:32px;line-height:1.4;color:#C9D6EE;max-height:4.4em}}
.chips{{font-weight:600;font-size:24px;color:{ORANGE}}}"""
        rest = f'<h1 class="fit bal">{f["sub"]}</h1>' if f["paired"] else f'<h1 class="fit bal">{f["head"]}</h1><div class="sub fit">{f["sub"]}</div>'
        body = f"""<div class="panel"></div><div class="lg">{logo(NAVY, 84)}</div>
<div class="unit"><div class="num">{f['num']}</div><div class="cap fit bal">{f['cap'] or f['kicker']}</div></div>
<div class="copy"><div class="kicker">{f['kicker']}</div>{rest}<div class="chips">{chips}</div></div>"""
        return css, body
    hero = 300 if n == 1 else 220 if n == 2 else 150
    css = f"""
body{{background:{NAVY};color:#fff}}
.panel{{position:absolute;left:0;top:0;bottom:0;width:580px;background:{ORANGE};clip-path:polygon(0 0,100% 0,80% 100%,0 100%)}}
.unit{{position:absolute;left:140px;width:300px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}}
.num{{font-size:{hero}px;line-height:.8;color:{NAVY};white-space:nowrap}}
.cap{{margin-top:16px;font-size:32px;line-height:1.12;color:{NAVY};max-height:3.4em}}
.cap .hl{{color:inherit}}
.copy{{position:absolute;left:600px;right:140px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}}
.lg{{position:absolute;right:140px;top:84px}}
.kicker{{color:{ORANGE};font-size:23px}}
h1{{font-size:80px;line-height:1.1;margin:10px 0 16px;max-height:2.3em}}
.sub{{font-size:25px;line-height:1.4;color:#C9D6EE;max-height:4.3em}}
.chips{{margin-top:22px;font-weight:600;font-size:19px;color:{ORANGE}}}"""
    body = f"""<div class="panel"></div><div class="unit"><div class="num">{f['num']}</div><div class="cap fit bal">{f['cap']}</div></div>
<div class="lg">{logo('#fff', 60)}</div>
<div class="copy"><div class="kicker">{f['kicker']}</div><h1 class="fit bal">{f['head']}</h1><div class="sub fit">{f['sub']}</div><div class="chips">{chips}</div></div>"""
    return css, body


def mark(f, sq):
    """Chữ A của Adtek: nền navy phẳng, dấu A cam cỡ lớn tràn mép, tiêu đề trắng."""
    n = len(f["num"])
    fb = f["head"] == f["cap"]  # khổ Facebook: số lớn đọc liền với câu bên dưới
    css = f"""
body{{background:{NAVY};color:#fff}}
.big{{position:absolute;aspect-ratio:285/253;background:{ORANGE}}}
.kicker{{color:{ORANGE};font-weight:800}}
.num{{font-weight:900;line-height:.86;letter-spacing:-.05em;color:#fff;white-space:nowrap}}
h1{{font-weight:900;line-height:1.12;letter-spacing:-.01em}}
.sub{{font-weight:600;line-height:1.42;color:#C9D6EE}}
.site{{position:absolute;font-weight:700;color:rgba(255,255,255,.7)}}
.lg{{position:absolute}}
.sq .big{{height:700px;right:-200px;bottom:-260px}}
.sq .lg{{left:72px;top:64px}}
.sq .copy{{position:absolute;left:72px;top:210px;width:{720 if fb else 640}px}}
.sq .kicker{{font-size:30px}}
.sq .num{{font-size:{300 if n <= 2 else 200}px;margin:18px 0 6px}}
.sq h1{{font-size:{84 if fb else 96}px;margin:{'0 0 26px' if fb else '18px 0 26px'};max-height:3.4em}}
.sq .sub{{font-size:32px;max-height:4.3em;max-width:600px}}
.sq .site{{left:72px;bottom:64px;font-size:22px}}
.ls .big{{height:760px;right:-240px;bottom:-230px}}
.ls .lg{{left:140px;top:84px}}
.ls .copy{{position:absolute;left:140px;top:0;bottom:0;width:500px;display:flex;flex-direction:column;justify-content:center;padding-top:30px}}
.ls .kicker{{font-size:23px}}
.ls h1{{font-size:78px;margin:10px 0 16px;max-height:2.3em}}
.ls .sub{{font-size:25px;max-height:4.3em}}
.ls .site{{display:none}}"""
    num = f'<div class="num">{f["num"]}</div>' if sq and fb else ""
    body = f"""<div class="big mark"></div><div class="lg">{logo('#fff', 74 if sq else 56)}</div>
<div class="copy"><div class="kicker">{f['kicker']}</div>{num}<h1 class="fit bal{' phrase' if num else ''}">{f['head']}</h1><div class="sub fit">{f['sub']}</div></div>
<div class="site">adtek.agency</div>"""
    return css, body


def stack(f, sq):
    """Hai tầng màu: khối navy và nền kem; con số cam lớn, cụm chữ đi kèm nằm ngay bên phải hoặc ngay dưới số."""
    n = len(f["num"])
    if sq:
        css = f"""
body{{background:{CREAM};color:{NAVY}}}
.top{{position:absolute;left:0;right:0;top:0;height:660px;background:{NAVY};color:#fff;padding:190px 72px 0}}
.lg{{position:absolute;left:72px;top:64px}}
.kicker{{color:{ORANGE};font-size:30px;margin-bottom:30px}}
.row{{display:flex;align-items:center;gap:36px}}
.num{{flex:none;font-size:{280 if n == 1 else 230 if n == 2 else 150}px;line-height:.8;color:{ORANGE};white-space:nowrap}}
h1{{flex:1;font-size:74px;line-height:1.12;max-height:4.5em}}
.sub{{position:absolute;left:72px;right:72px;top:730px;font-size:40px;line-height:1.38;max-height:4.2em}}
.chips{{position:absolute;left:72px;bottom:64px;font-weight:600;font-size:24px;color:{ORANGE}}}"""
        head = f["head"] if f["paired"] else f["cap"] or f["head"]
        body = f"""<div class="top"><div class="kicker">{f['kicker']}</div><div class="row"><div class="num">{f['num']}</div>
<h1 class="fit bal{' phrase' if f['paired'] else ''}">{head}</h1></div></div><div class="lg">{logo('#fff', 74)}</div><div class="sub fit">{f['sub']}</div>
<div class="chips">{' &nbsp;·&nbsp; '.join(f['chips'][:3])}</div>"""
        return css, body
    css = f"""
body{{background:{CREAM};color:{NAVY}}}
.top{{position:absolute;left:0;top:0;bottom:0;width:740px;padding:0 60px 0 140px;background:{NAVY};color:#fff;display:flex;flex-direction:column;justify-content:center}}
.lg{{position:absolute;left:140px;top:84px}}
.kicker{{color:{ORANGE};font-size:23px}}
h1{{font-size:80px;line-height:1.12;margin:10px 0 16px;max-height:2.3em}}
.sub{{font-size:24px;line-height:1.42;color:#C9D6EE;max-height:4.3em}}
.unit{{position:absolute;left:780px;right:140px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}}
.num{{font-size:{230 if n == 1 else 170 if n == 2 else 110}px;line-height:.8;color:{ORANGE};white-space:nowrap}}
.cap{{margin-top:18px;font-size:30px;line-height:1.15;max-height:3.5em}}"""
    unit = f'<div class="unit"><div class="num">{f["num"]}</div><div class="cap fit bal">{f["cap"]}</div></div>' if f["cap"] else ""
    body = f"""<div class="top"><div class="kicker">{f['kicker']}</div><h1 class="fit bal">{f['head']}</h1><div class="sub fit">{f['sub']}</div></div>
<div class="lg">{logo('#fff', 56)}</div>{unit}"""
    return css, body


def poster(f, sq):
    """Áp phích: nền cam phẳng, logo navy, số navy rất lớn đứng ngay trước cụm chữ đi kèm (trên chữ ở khổ vuông, trái chữ ở khổ ngang)."""
    n = len(f["num"])
    css = f"""
body{{background:{ORANGE};color:{NAVY}}}
.hl{{color:inherit}}
.lg{{position:absolute}}
.num{{font-size:var(--hero);line-height:.78;color:{NAVY};white-space:nowrap}}
h1{{line-height:1.1}}
.sub{{line-height:1.4}}
.sq{{--hero:{560 if n == 1 else 470 if n == 2 else 320}px}}
.sq .lg{{right:64px;top:60px}}
.sq .copy{{position:absolute;left:64px;right:72px;top:64px}}
.sq .kicker{{font-size:30px;margin:0 0 20px 8px}}
.sq h1{{font-size:92px;margin:10px 0 18px 8px;max-height:3.4em}}
.sq .sub{{font-size:32px;max-height:2.9em;margin-left:8px}}
.ls{{--hero:{420 if n == 1 else 330 if n == 2 else 220}px}}
.ls .lg{{right:140px;top:84px}}
.ls .copy{{position:absolute;left:140px;right:140px;top:0;bottom:0;display:flex;align-items:center;gap:44px}}
.ls .num{{flex:none}}
.ls .text{{flex:1}}
.ls .kicker{{font-size:22px}}
.ls h1{{font-size:64px;margin:8px 0 14px;max-height:3.4em}}
.ls .sub{{font-size:23px;max-height:4.2em}}"""
    if sq:
        inner = f"""<div class="kicker">{f['kicker']}</div><div class="num">{f['num']}</div>
<h1 class="fit bal{' phrase' if f['paired'] else ''}">{f['head']}</h1><div class="sub fit">{f['sub']}</div>"""
    else:  # khổ ngang: số bên trái, cụm chữ của số làm tiêu đề ngay bên phải, tên bài làm nhãn
        inner = f"""<div class="num">{f['num']}</div><div class="text"><div class="kicker">{f['title']}</div>
<h1 class="fit bal{' phrase' if f['cap'] else ''}">{f['cap'] or f['head']}</h1><div class="sub fit">{f['sub']}</div></div>"""
    body = f"""<div class="lg">{logo(NAVY, 80 if sq else 58)}</div><div class="copy">{inner}</div>"""
    return css, body


def versus(f, sq):
    """Đối đầu: dành cho bài so sánh "A vs B", hai nửa navy và cam cắt chéo, chữ "vs" nghiêng màu cam trên nửa navy cạnh đường cắt."""
    src = html.unescape(f["title"])
    a, b = (re.split(r"\s+vs\.?\s+", src, flags=re.I) + ["", ""])[:2]
    a, b = esc(a.strip()), esc(re.sub(r"\s*(19|20)\d\d$", "", b.strip()))
    css = f"""
body{{background:{ORANGE};color:#fff}}
.l{{position:absolute;inset:0;background:{NAVY};clip-path:polygon(0 0,58% 0,42% 100%,0 100%)}}
.name{{position:absolute;font-weight:900;line-height:1.08;text-transform:uppercase;letter-spacing:-.01em}}
.na{{color:#fff}}.nb{{color:{NAVY};text-align:right}}
.vs{{position:absolute;transform:translate(-50%,-50%);color:{ORANGE};font-style:italic;line-height:1}}
.kicker{{position:absolute;font-weight:800;color:{ORANGE}}}
.band{{position:absolute;background:{NAVY};color:#fff;font-weight:800;line-height:1.35}}
.lg{{position:absolute}}
.sq .lg{{left:72px;top:64px}}.sq .kicker{{left:72px;top:190px;font-size:30px}}
.sq .na{{left:72px;top:270px;width:420px;font-size:96px;max-height:2.3em}}
.sq .nb{{right:72px;top:640px;width:420px;font-size:96px;max-height:2.3em}}
.sq .vs{{left:41%;top:52%;font-size:120px}}
.sq .band{{left:0;right:0;bottom:0;padding:34px 72px 40px;font-size:36px;max-height:4.4em}}
.ls .lg{{left:140px;top:84px}}.ls .kicker{{left:140px;top:170px;font-size:23px}}
.ls .na{{left:140px;top:210px;width:360px;font-size:80px;max-height:2.3em}}
.ls .nb{{right:140px;top:210px;width:360px;font-size:80px;max-height:2.3em}}
.ls .vs{{left:42%;top:46%;font-size:96px}}
.ls .band{{left:0;right:0;bottom:0;text-align:center;padding:22px 160px 84px;font-size:24px;max-height:5.6em}}"""
    cap = html.unescape(re.sub(r"<[^>]+>", "", f["cap"]))
    if cap[1:2].islower() and cap.split()[0] not in src:  # "Sàn, chia..." đọc liền sau số: "2 sàn, chia..."
        cap = cap[0].lower() + cap[1:]
    band = f"{f['num']} {esc(cap)}" if sq and cap else f["sub"]
    body = f"""<div class="l"></div><div class="lg">{logo('#fff', 80 if sq else 58)}</div>
<div class="kicker">{f['kicker']}</div><div class="name na fit bal">{a}</div><div class="name nb fit bal">{b}</div>
<div class="vs">vs</div><div class="band fit bal">{band}</div>"""
    return css, body


def dossier(f, sq):
    """Hồ sơ pháp lý: dành cho bài luật, nghị định. Nền navy phẳng, tờ checklist kem với ô đánh dấu cam."""
    check = '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    items = "".join(f"<li><b>{check}</b>{x}</li>" for x in f["chips"])
    css = f"""
body{{color:#fff;background:{NAVY}}}
.kicker{{color:{ORANGE};font-weight:800}}
h1{{font-weight:900;line-height:1.12}}
.sub{{font-weight:600;line-height:1.42;color:#C9D6EE}}
.paper{{position:absolute;background:{CREAM};color:{NAVY}}}
.paper h5{{font-weight:800;color:{ORANGE}}}
.paper ul{{list-style:none}}
.paper li{{display:flex;align-items:center;font-weight:800}}
.paper li b{{flex:none;background:{ORANGE};display:flex}}
.sq .lg{{position:absolute;left:72px;top:64px}}
.sq .copy{{position:absolute;left:72px;right:72px;top:190px}}
.sq .kicker{{font-size:30px}}.sq h1{{font-size:86px;margin:12px 0 16px;max-height:2.3em}}.sq .sub{{font-size:30px;max-height:4.3em}}
.sq .paper{{left:72px;right:72px;bottom:0;height:430px;padding:46px 56px}}
.sq .paper h5{{font-size:26px;margin-bottom:10px}}.sq .paper li{{font-size:32px;gap:22px;padding:13px 0}}.sq .paper li b{{width:44px;height:44px;padding:7px}}
.ls .lg{{position:absolute;left:140px;top:84px}}
.ls .copy{{position:absolute;left:140px;width:520px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;padding-top:40px}}
.ls .kicker{{font-size:23px}}.ls h1{{font-size:72px;margin:10px 0 14px;max-height:2.3em}}.ls .sub{{font-size:24px;max-height:4.3em}}
.ls .paper{{left:720px;right:0;top:0;bottom:0;padding:0 140px 0 46px;display:flex;flex-direction:column;justify-content:center}}
.ls .paper h5{{font-size:19px;margin-bottom:8px}}.ls .paper li{{font-size:22px;gap:14px;padding:10px 0}}.ls .paper li b{{width:32px;height:32px;padding:5px}}"""
    body = f"""<div class="lg">{logo('#fff', 74 if sq else 56)}</div>
<div class="copy"><div class="kicker">{f['kicker']}</div><h1 class="fit bal">{f['head']}</h1><div class="sub fit">{f['sub']}</div></div>
<div class="paper"><h5>Checklist tuân thủ</h5><ul>{items}</ul></div>"""
    return css, body


# Phong cách dùng chung cho mọi bài (xoay vòng), phong cách theo chủ đề (chỉ dùng khi bài hợp),
# và phong cách chỉ dùng khi ghi tay cover.style (không tự chọn).
GENERIC = {"editorial": editorial, "split": split, "mark": mark, "stack": stack, "poster": poster}
THEMED = {"versus": versus, "dossier": dossier}
MANUAL = {"neon3d": neon3d}
STYLES = {**GENERIC, **THEMED, **MANUAL}
LABELS = {"editorial": "Tạp chí nền kem", "split": "Khối cam navy cắt chéo", "mark": "Chữ A Adtek cỡ lớn",
          "stack": "Hai tầng màu, đĩa số cam", "poster": "Áp phích nền cam",
          "versus": "Đối đầu A vs B (bài so sánh)", "dossier": "Hồ sơ pháp lý (bài luật)",
          "neon3d": "Tím neon 3D (chỉ khi ghi tay cover.style)"}


def themed_for(post):
    c = post.get("cover") or {}
    text = " ".join([post.get("title", ""), c.get("title", ""), c.get("kicker", "")])
    if re.search(r"\svs\.?\s", c.get("title", ""), re.I):
        return "versus"
    if re.search(r"\b(Luật|Nghị định|Thông tư)\b", text):
        return "dossier"
    return None


def pick(data, post):
    """Chọn phong cách: cover.style nếu có; bài so sánh, bài luật dùng mẫu chủ đề (trừ khi 2 bài liền trước đã dùng);
    còn lại xoay vòng mẫu chung, tránh 3 bài liền trước."""
    c = post["cover"]
    if c.get("style"):
        return c["style"]
    before = sorted((p for p in data["posts"] if p.get("cover") and p["no"] < post["no"]), key=lambda p: p["no"])
    recent = [pick(data, p) for p in before[-3:]]
    t = themed_for(post)
    if t and t not in recent[-2:]:
        return t
    names = list(GENERIC)
    for i in range(len(names)):
        name = names[(post["no"] + i) % len(names)]
        if name not in recent:
            return name
    return names[post["no"] % len(names)]


def document(css, body, w, h):
    """Trang HTML hoàn chỉnh theo nhận diện chung (font, logo, co chữ) từ CSS và thân trang của một mẫu."""
    # mask-image không đọc được file:// (chặn CORS) nên nhúng logo dạng data URI
    uri = lambda name: "data:image/png;base64," + base64.b64encode((ASSETS / name).read_bytes()).decode()  # noqa: E731
    return HEAD.substitute(fontcss=font_css(), logo=uri("adtek-logo-white.png"), mark=uri("adtek-mark-white.png"),
                           w=w, h=h, css=css, body=body, shape="sq" if w == h else "ls")


def page(post, kind, style):
    w, h = SIZES[kind]
    css, body = STYLES[style](fields(post, kind), w == h)
    return document(css, body, w, h)


def shoot(pages):
    """pages: danh sách (html, output, rộng, cao[, hệ số điểm ảnh]). Chụp tất cả trong một lần mở trình duyệt."""
    tmp = ROOT / "previews/_covers"
    tmp.mkdir(parents=True, exist_ok=True)
    manifest = []
    for i, (html_text, out, w, h, *scale) in enumerate(pages):
        src = tmp / f"{i}.html"
        src.write_text(html_text, encoding="utf-8")
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        manifest.append({"input": str(src), "output": str(out), "width": w, "height": h, "scale": scale[0] if scale else 1})
    mf = tmp / "jobs.json"
    mf.write_text(json.dumps(manifest), encoding="utf-8")
    subprocess.run(["node", str(ROOT / "tools/render_cover.js"), str(mf)], check=True)
    for p in tmp.iterdir():
        p.unlink()
    tmp.rmdir()
    return [m["output"] for m in manifest]


def render(jobs):
    """jobs: danh sách (post, kind, style, output)."""
    return shoot([(page(post, kind, style), out, *SIZES[kind], SCALE[kind]) for post, kind, style, out in jobs])


def output_path(post, kind):
    return ROOT / f"content/posts/{post['slug']}-{'cover' if kind == 'blog' else 'fb'}.jpg"


def make(post, kind, out=None):
    """Dựng ảnh thật của bài. Lần đầu chọn phong cách bằng pick() và ghi cover.style vào calendar.json,
    để dựng lại (sửa bài, đổi ảnh) vẫn ra đúng phong cách cũ và các bài sau tính lịch sử đúng."""
    from blog_post import find, load, save
    style = post["cover"].get("style")
    if not style:
        data = load()
        fresh = find(data, post["no"])
        style = pick(data, fresh)
        fresh["cover"]["style"] = post["cover"]["style"] = style
        save(data)
    out = out or output_path(post, kind)
    render([(post, kind, style, out)])
    print(out)
    return out


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "tools"))
    from blog_post import find, load

    args = sys.argv[1:]
    opt = lambda k, d=None: args[args.index(k) + 1] if k in args else d  # noqa: E731
    data = load()
    cmd = args[0]
    if cmd == "styles":
        for k, v in LABELS.items():
            print(f"{k:10} {v}")
    elif cmd == "pick":
        for p in data["posts"]:
            if p.get("cover"):
                print(p["no"], pick(data, p), p["title"][:60])
    elif cmd == "render":
        post = find(data, int(args[1]))
        style = opt("--style") or pick(data, post)
        kinds = ["blog", "fb"] if opt("--kind", "all") == "all" else [opt("--kind")]
        out = opt("--out")
        jobs = [(post, k, style, Path(out) / f"{post['slug']}-{k}-{style}.jpg" if out else output_path(post, k)) for k in kinds]
        print("\n".join(render(jobs)))
    elif cmd == "existing":  # bài cũ trong mục existing của calendar.json (có slug, date, cover kèm style)
        e = next(x for x in data["existing"] if str(x.get("wp_id")) == args[1])
        post = {"no": 0, **e}
        print("\n".join(render([(post, "blog", e["cover"]["style"], output_path(post, "blog"))])))
    elif cmd == "sheet":
        post = find(data, int(args[1]))
        out = Path(opt("--out", ROOT / "previews/covers"))
        styles = [s for s in STYLES if s in GENERIC or themed_for(post) == s]
        jobs = [(post, k, s, out / f"{post['no']:02d}-{s}-{k}.jpg") for s in styles for k in SIZES]
        print("\n".join(render(jobs)))
