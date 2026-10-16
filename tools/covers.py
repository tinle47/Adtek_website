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
  python3 tools/covers.py fbcover [classic|arrow|bars|cream|pattern|columns|minimal|center|split] [--out thư-mục]   ảnh bìa Fanpage Facebook 1640x624 (content/brand/fb-cover.jpg)
  python3 tools/covers.py og [navy|cream|panel] [--out thư-mục]   ảnh chia sẻ mặc định của website (content/brand/og-default.jpg và @2x)
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
.kicker,.chips,.paper h5{color:inherit;opacity:.75;font-weight:600;letter-spacing:0}  /* nhãn nhỏ không dùng màu cam (anh Tin 17/10/2026): cam chỉ cho số và từ khóa */
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
.meta b{{font-weight:700}}
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
    """Khối tương phản: mảng kem cắt chéo chứa số cam và cụm chữ đi kèm ngay bên phải hoặc ngay bên dưới số; phần còn lại navy."""
    n = len(f["num"])
    chips = " &nbsp;·&nbsp; ".join(f["chips"][:3])
    if sq:
        hero = 400 if n == 1 else 330 if n == 2 else 220
        css = f"""
body{{background:{NAVY};color:#fff}}
.panel{{position:absolute;left:0;top:0;right:0;height:580px;background:{CREAM};clip-path:polygon(0 0,100% 0,100% 72%,0 100%)}}
.unit{{position:absolute;left:64px;right:72px;top:150px;display:flex;align-items:flex-end;gap:30px}}
.num{{flex:none;font-size:{hero}px;line-height:.8;color:{ORANGE};white-space:nowrap}}
.cap{{flex:1;font-size:56px;line-height:1.1;color:{NAVY};max-height:3.4em;padding-bottom:6px}}
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
.panel{{position:absolute;left:0;top:0;bottom:0;width:580px;background:{CREAM};clip-path:polygon(0 0,100% 0,80% 100%,0 100%)}}
.unit{{position:absolute;left:140px;width:300px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}}
.num{{font-size:{hero}px;line-height:.8;color:{ORANGE};white-space:nowrap}}
.cap{{margin-top:16px;font-size:32px;line-height:1.12;color:{NAVY};max-height:3.4em}}
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
    """Áp phích: nền navy phẳng, số cam rất lớn đứng ngay trước cụm chữ đi kèm (trên chữ ở khổ vuông, trái chữ ở khổ ngang)."""
    n = len(f["num"])
    css = f"""
body{{background:{NAVY};color:#fff}}
.lg{{position:absolute}}
.num{{font-size:var(--hero);line-height:.78;color:{ORANGE};white-space:nowrap}}
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
    body = f"""<div class="lg">{logo('#fff', 80 if sq else 58)}</div><div class="copy">{inner}</div>"""
    return css, body


def versus(f, sq):
    """Đối đầu: dành cho bài so sánh "A vs B", hai nửa navy và kem cắt chéo, chữ "vs" nghiêng màu cam trên nửa navy cạnh đường cắt."""
    src = html.unescape(f["title"])
    a, b = (re.split(r"\s+vs\.?\s+", src, flags=re.I) + ["", ""])[:2]
    a, b = esc(a.strip()), esc(re.sub(r"\s*(19|20)\d\d$", "", b.strip()))
    css = f"""
body{{background:{CREAM};color:#fff}}
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
    return HEAD.substitute(fontcss=font_css(), logo=uri("adtek-logo-white.png"), mark=uri("adtek-mark-white-hd.png"),
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


# ---------------------------------------------------------------- ảnh chia sẻ mặc định của website

OG_SIZE = (1200, 630)  # og:image mặc định (trang chủ VI, EN và trang không có ảnh đại diện), xuất thêm bản @2x
OG_TEXT = {"head": "*Growth* marketing agency", "sub": "Brand Commerce, Lead Generation, SEO", "site": "adtek.agency"}
OG_VARIANTS = ("navy", "cream", "panel")


def og_default(variant="navy"):
    """Ảnh chia sẻ mặc định cho adtek.agency. Vùng an toàn cho chữ và logo: x 100 đến 1100, y 60 đến 570
    (Facebook, Zalo, LinkedIn cắt mép khác nhau); chỉ dấu A cam (không chữ) được tràn ra ngoài.
    navy: nền navy, chữ trắng, dấu A cam. cream: nền kem, chữ navy, dấu A cam. panel: chữ trên nền navy, logo navy trên khối kem bên phải."""
    bg, fg, sub = (CREAM, NAVY, NAVY) if variant == "cream" else (NAVY, "#fff", "#C9D6EE")
    css = f"""
body{{background:{bg};color:{fg}}}
.big{{position:absolute;aspect-ratio:285/253;background:{ORANGE};height:760px;right:-230px;bottom:-250px}}
.lg{{position:absolute;left:100px;top:72px}}
.copy{{position:absolute;left:100px;top:196px;width:640px}}
h1{{font-size:88px;line-height:1.05;max-height:2.2em}}
.sub{{font-size:30px;line-height:1.35;margin-top:26px;color:{sub};{'opacity:.85;' if variant == 'cream' else ''}}}
.site{{position:absolute;left:100px;top:510px;font-size:24px;font-weight:600;opacity:.75}}
.panel{{position:absolute;left:780px;top:0;right:0;bottom:0;background:{CREAM};display:flex;align-items:center;justify-content:center}}
.panel .logo{{background:{NAVY}}}"""
    if variant == "panel":
        art = f'<div class="panel">{logo(NAVY, 168)}</div>'
        css += ".copy{width:620px}"
    else:
        art = '<div class="big mark"></div>'
    top = "" if variant == "panel" else f'<div class="lg">{logo(fg, 76)}</div>'
    body = f"""{art}{top}
<div class="copy"><h1 class="fit bal">{hl(OG_TEXT['head'])}</h1><div class="sub">{esc(OG_TEXT['sub'])}</div></div>
<div class="site">{OG_TEXT['site']}</div>"""
    return document(css, body, *OG_SIZE)


def og_render(variant="navy", out=None):
    """Ghi content/brand/og-default.jpg (1200x630) và og-default@2x.jpg (2400x1260); out: thư mục khác để xem thử."""
    d = Path(out) if out else ROOT / "content/brand"
    name = "og-default" if not out else f"og-{variant}"
    page_html = og_default(variant)
    return shoot([(page_html, d / f"{name}.jpg", *OG_SIZE, 1), (page_html, d / f"{name}@2x.jpg", *OG_SIZE, 2)])


# ---------------------------------------------------------------- ảnh bìa Fanpage Facebook

FB_COVER_SIZE = (1640, 624)  # khổ tải lên Facebook khuyến nghị (hiển thị 820x312 trên máy tính)
# Ứng dụng Facebook trên điện thoại (đo từ ảnh chụp anh Tin gửi 16/10/2026): chỉ thấy x 315 đến 1325; thanh trạng thái che y < 80;
# nút menu, sửa, tìm kiếm ở hai góc trên (y 155 đến 210); ảnh đại diện Page là hình tròn tâm (818, 573) bán kính khoảng 200
# che giữa phía dưới (chủ Page còn thấy bong bóng "Share a note" ở x 670 đến 965, y 305 đến 400); khung trắng che y > 595.
# Máy tính: ảnh đại diện đè góc dưới bên trái. Mẫu "columns": logo, tiêu đề giữa phía trên; dịch vụ hai cột hai bên hình tròn.
SERVICES = ["User acquisition strategy", "CRM management", "Integrated marketing communication", "Growth consultancy", "SEO services"]
FB_COVER_VARIANTS = ("columns", "minimal", "center", "split", "cream")  # anh Tin chọn bố cục giữa, chỉnh lại thành columns cho điện thoại
FB_COVER_BOLD = ("arrow", "bars", "cream", "pattern")
FB_MOBILE = {"view": (315, 1325), "top": 80, "icons": [(330, 155, 400, 210), (1020, 155, 1290, 210)],
             "circle": (818, 573, 200), "note": (670, 305, 965, 400), "bottom": 595}


def fb_cover(variant="columns"):
    """columns: nền navy, logo và tiêu đề giữa phía trên, dịch vụ 01 đến 03 cột trái, 04 đến 05 cột phải, dấu A cam giữa phía dưới
    (trên điện thoại nằm sau ảnh đại diện Page). minimal: như columns nhưng bỏ danh sách dịch vụ, tiêu đề lớn hơn.
    split: nền navy, tiêu đề bên trái, 5 dịch vụ đánh số bên phải, dấu A cam tràn mép phải.
    center: nền navy, bố cục giữa như ảnh bìa cũ, 5 dịch vụ thành hàng (số trên, chữ dưới), dấu A cam ở hai góc dưới.
    cream: nền kem, tiêu đề navy bên trái, dịch vụ trên khối navy tràn mép phải, dấu A cam ở mép phải."""
    items = "".join(f'<li><span class="num">{i:02d}</span><span class="t">{esc(t)}</span></li>' for i, t in enumerate(SERVICES, 1))
    head = hl("*Growth* marketing agency")
    if variant in ("columns", "minimal"):
        li = lambda i, t: f'<li><span class="num">{i:02d}</span><span class="t">{esc(t)}</span></li>'  # noqa: E731
        left = "".join(li(i, t) for i, t in enumerate(SERVICES[:3], 1))
        right = "".join(li(i, t) for i, t in enumerate(SERVICES[3:], 4))
        mini = variant == "minimal"
        css = f"""
body{{background:{NAVY};color:#fff}}
.big{{position:absolute;aspect-ratio:285/253;background:{ORANGE};width:{460 if mini else 400}px;left:50%;transform:translateX(-50%);bottom:{-162 if mini else -112}px}}
.lg{{position:absolute;left:0;right:0;top:{96 if mini else 88}px;display:flex;justify-content:center}}
h1{{position:absolute;left:330px;right:330px;top:{230 if mini else 214}px;text-align:center;font-size:{74 if mini else 68}px;line-height:1}}
ul{{position:absolute;top:340px;width:262px;list-style:none;display:flex;flex-direction:column;gap:20px}}
ul.l{{left:345px}}ul.r{{left:1040px}}
li{{display:flex;align-items:baseline;gap:12px}}
.num{{font-size:34px;line-height:1;color:{ORANGE};width:42px;flex:none}}
.t{{font-size:23px;line-height:1.2;font-weight:500;color:#DCE4F2}}"""
        lists = "" if mini else f'<ul class="l">{left}</ul><ul class="r">{right}</ul>'
        body = f"""<div class="big mark"></div><div class="lg">{logo('#fff', 80)}</div><h1>{head}</h1>{lists}"""
    elif variant == "center":
        css = f"""
body{{background:{NAVY};color:#fff}}
.big{{position:absolute;aspect-ratio:285/253;background:{ORANGE};height:430px}}
.b1{{left:-150px;bottom:-130px}}.b2{{right:-150px;bottom:-130px}}
.lg{{position:absolute;left:0;right:0;top:84px;display:flex;justify-content:center}}
h1{{position:absolute;left:300px;right:300px;top:236px;text-align:center;font-size:76px;line-height:1}}
ul{{position:absolute;left:290px;right:290px;top:388px;list-style:none;display:grid;grid-template-columns:repeat(5,1fr);gap:26px}}
li{{display:flex;flex-direction:column;gap:6px}}
.num{{font-size:46px;line-height:1;color:{ORANGE}}}
.t{{font-size:25px;line-height:1.24;font-weight:500;color:#DCE4F2}}"""
        body = f"""<div class="big mark b1"></div><div class="big mark b2"></div>
<div class="lg">{logo('#fff', 104)}</div><h1>{head}</h1><ul>{items}</ul>"""
    else:
        cream = variant == "cream"
        bg, fg = (CREAM, NAVY) if cream else (NAVY, "#fff")
        css = f"""
body{{background:{bg};color:{fg}}}
.big{{position:absolute;aspect-ratio:285/253;background:{ORANGE};height:820px;right:{-470 if cream else -420}px;bottom:-330px}}
.panel{{position:absolute;left:860px;top:0;right:0;bottom:0;background:{NAVY}}}
.lg{{position:absolute;left:300px;top:96px}}
h1{{position:absolute;left:300px;top:{232 if cream else 222}px;width:520px;font-size:80px;line-height:1.04}}
ul{{position:absolute;left:{920 if cream else 880}px;top:0;bottom:0;width:{420 if cream else 460}px;list-style:none;display:flex;flex-direction:column;justify-content:center;gap:24px}}
li{{display:flex;align-items:baseline;gap:18px}}
.num{{font-size:40px;line-height:1;color:{ORANGE};width:48px;flex:none}}
.t{{font-size:28px;line-height:1.15;font-weight:500;color:{'#fff' if cream else '#DCE4F2'}}}"""
        art = ('<div class="panel"></div>' if cream else '') + '<div class="big mark"></div>'
        body = f"""{art}<div class="lg">{logo(fg, 92)}</div><h1>{head}</h1><ul>{items}</ul>"""
    return document(css, body, *FB_COVER_SIZE)


def growth_arrow(points, color=CREAM, width=14, head=46):
    """Mũi tên cong đi qua các điểm (đường Catmull-Rom đổi sang Bezier), đầu mũi tên tam giác theo hướng cuối đường.
    Đường kéo dài thêm từ điểm cuối theo hướng đi lên để đầu mũi tên ra khỏi cột cuối."""
    import math
    pts = [points[0]] + points + [points[-1]]
    d = f"M{pts[1][0]},{pts[1][1]}"
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]},{p2[1]}"
    (x1, y1), (x2, y2) = points[-2], points[-1]
    a = math.atan2(y2 - y1, x2 - x1)
    tip = (x2 + head * .9 * math.cos(a), y2 + head * .9 * math.sin(a))
    d += f" L{x2 + head * .2 * math.cos(a):.1f},{y2 + head * .2 * math.sin(a):.1f}"
    left = (tip[0] - head * math.cos(a - .5), tip[1] - head * math.sin(a - .5))
    right = (tip[0] - head * math.cos(a + .5), tip[1] - head * math.sin(a + .5))
    tri = " ".join(f"{x:.1f},{y:.1f}" for x, y in (tip, left, right))
    return (f'<svg class="abs" style="left:0;top:0" width="{FB_COVER_SIZE[0]}" height="{FB_COVER_SIZE[1]}">'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<polygon points="{tri}" fill="{color}" stroke="{color}" stroke-width="6" stroke-linejoin="round"/></svg>')


def fb_cover_bold(variant):
    """Bản gọn nhiều hình hơn (anh Tin 16/10/2026: bản gọn chưa đủ ấn tượng). Tiêu đề giữa phía trên, hình nằm ngoài vùng chữ.
    bars: biểu đồ cột tăng dần từ trái sang phải trên nền navy; ba cột cuối chuyển cam (giai đoạn tăng trưởng).
    cream: cùng biểu đồ trên nền kem, cột navy đặc, ba cột cuối cam.
    pattern: lưới dấu A chìm trên nền navy, một dấu A cam lớn nổi bật ở cột phải (thấy cả trên điện thoại).
    arrow: như bars, thêm mũi tên kem cong vút lên theo đỉnh cột (anh Tin chọn 16/10/2026)."""
    cream = variant == "cream"
    bg, fg = (CREAM, NAVY) if cream else (NAVY, "#fff")
    css = f"""
body{{background:{bg};color:{fg}}}
.lg{{position:absolute;left:0;right:0;top:92px;display:flex;justify-content:center}}
h1{{position:absolute;left:315px;right:315px;top:224px;text-align:center;font-size:80px;line-height:1}}
.bar{{position:absolute;bottom:0;width:150px;background:{NAVY if cream else 'rgba(244,238,227,.10)'}}}
.bar.o{{background:{ORANGE}}}
.pa{{position:absolute;aspect-ratio:285/253;background:rgba(244,238,227,.07)}}
.pa.o{{background:{ORANGE}}}"""
    if variant in ("bars", "cream", "arrow"):
        hs = [36, 50, 68, 92, 124, 168, 232, 316]  # tăng nhanh dần như đường cong tăng trưởng
        art = "".join(f'<div class="bar{" o" if i >= 5 else ""}" style="left:{40 + 200 * i}px;height:{h}px"></div>' for i, h in enumerate(hs))
        if variant == "arrow":
            # sát đỉnh cột ở đầu, càng về cuối càng xa đỉnh cột để đường cong dốc dần lên (vút)
            art += growth_arrow([(115 + 200 * i, 624 - h - 22 - (i / 7) ** 2.2 * 96) for i, h in enumerate(hs)], width=16, head=54)
    else:
        cells = []
        for r, y in enumerate(range(-30, 640, 120)):
            for x in range(-60 + (70 if r % 2 else 0), 1700, 140):
                if 280 < x < 1300 and 40 < y < 330:  # chừa chỗ cho logo và tiêu đề
                    continue
                if 1080 < x < 1300 and 330 <= y < 560:  # chỗ của dấu A cam
                    continue
                cells.append(f'<div class="pa mark" style="left:{x}px;top:{y}px;height:72px"></div>')
        art = "".join(cells) + '<div class="pa mark o" style="left:1080px;top:362px;height:190px"></div>'
    body = f"""{art}<div class="lg">{logo(fg, 64)}</div><h1>{hl("*Growth* marketing agency")}</h1>"""
    return document(css, body, *FB_COVER_SIZE)

def fb_cover_classic():
    """Ảnh bìa Fanpage theo mẫu cũ của Adtek (anh Tin 16/10/2026: làm lại mẫu cũ, bỏ 5 ô dịch vụ). Riêng ảnh này giữ phong cách
    mẫu cũ (nền chuyển màu navy sang hồng, chữ A lớn mờ, tam giác, mạng lưới chấm, tiêu đề in hoa đậm Lexend Zetta), khác quy tắc
    thiết kế phẳng của ảnh bìa blog. Bố cục theo khung điện thoại FB_MOBILE: logo và tiêu đề giữa phía trên, trên hình tròn ảnh đại diện."""
    import random
    rnd = random.Random(7)
    W, H = FB_COVER_SIZE
    font = (ASSETS / "fonts/lexend-zetta-latin-900-normal.woff2").as_uri()
    dots = "".join(f'<circle cx="{rnd.randint(0, W)}" cy="{rnd.randint(0, H)}" r="{rnd.choice((1.4, 1.8, 2.4))}" fill="#fff" opacity="{rnd.choice((.35, .5, .7))}"/>'
                   for _ in range(70))
    # mạng lưới: điểm nối bằng đường mảnh, góc dưới trái và mép phải như mẫu cũ
    nets = [[(0, 500), (70, 538), (160, 540), (215, 624)], [(70, 538), (40, 624)], [(70, 538), (0, 590)],
            [(1445, 320), (1530, 318), (1590, 330), (1640, 300)], [(1445, 320), (1350, 420), (1455, 476), (1560, 500), (1640, 470)],
            [(1530, 318), (1455, 476), (1300, 560), (1300, 624)], [(1590, 330), (1560, 500), (1600, 624)], [(1455, 476), (1500, 624)],
            [(1350, 420), (1300, 560)], [(1560, 500), (1640, 560)]]
    lines = "".join(f'<polyline points="{" ".join(f"{x},{y}" for x, y in n)}" fill="none" stroke="#fff" stroke-width="1.6" opacity=".55"/>' for n in nets)
    nodes = {pt for n in nets for pt in n if 0 < pt[0] < W and 0 < pt[1] < H}
    knots = "".join(f'<circle cx="{x}" cy="{y}" r="{4 if (x + y) % 3 else 6}" fill="#fff"/>' for x, y in nodes)
    # tam giác: (điểm, màu, độ mờ, chỉ viền)
    tris = [([(45, 370), (130, 395), (75, 450)], "#6F86D6", .55, 0), ([(195, 425), (310, 380), (330, 470)], "#6F86D6", .6, 0),
            ([(230, 490), (270, 570), (300, 520)], "#6F86D6", .5, 0), ([(160, 465), (200, 510), (160, 505)], "#fff", .45, 1),
            ([(1290, 160), (1370, 195), (1300, 240)], "#7F7FE0", .6, 0), ([(1205, 440), (1258, 470), (1210, 480)], "#fff", .5, 1),
            ([(925, 520), (960, 560), (915, 552)], "#4C6FE0", .7, 0), ([(1405, 255), (1440, 250), (1430, 290)], "#fff", .45, 1),
            ([(380, 520), (410, 495), (420, 545)], "#fff", .35, 1)]
    tri = "".join(f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" '
                  + (f'fill="none" stroke="{c}" stroke-width="1.6" opacity="{o}"/>' if outline else f'fill="{c}" opacity="{o}"/>')
                  for pts, c, o, outline in tris)
    css = f"""
@font-face{{font-family:LZ;font-weight:900;src:url({font})}}
body{{background:linear-gradient(100deg,#1D3271 0%,#2E3F7C 30%,#5B5E92 55%,#A88DB8 78%,#EBBEDD 100%)}}
.haze{{position:absolute;inset:0;background:radial-gradient(ellipse 520px 260px at 0 0,rgba(205,170,210,.55),transparent 70%),
  radial-gradient(ellipse 600px 300px at 100% 0,rgba(255,215,240,.35),transparent 70%)}}
.bigA{{position:absolute;aspect-ratio:285/253;height:900px;left:50%;top:-40px;transform:translateX(-50%);
  background:linear-gradient(105deg,rgba(14,28,84,.75) 0%,rgba(96,122,196,.7) 38%,rgba(36,44,104,.6) 58%,rgba(170,160,215,.3) 100%)}}
svg{{position:absolute;inset:0}}
.lg{{position:absolute;left:0;right:0;top:108px;display:flex;justify-content:center}}
h1.cl{{position:absolute;left:0;right:0;top:278px;text-align:center;font-family:LZ;font-weight:900;font-size:44px;letter-spacing:-.11em;
  color:#fff;text-transform:uppercase;text-shadow:0 3px 6px rgba(10,20,60,.45)}}
.rule{{position:absolute;left:340px;right:340px;top:350px;height:2px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.85) 30%,rgba(255,255,255,.85) 70%,transparent)}}"""
    body = f"""<div class="haze"></div><div class="bigA mark"></div>
<svg width="{W}" height="{H}">{tri}{lines}{knots}{dots}</svg>
<div class="lg">{logo('#fff', 132)}</div><h1 class="cl">Growth marketing agency</h1><div class="rule"></div>"""
    return document(css, body, W, H)


def fb_cover_render(variant="arrow", out=None):
    """Ghi content/brand/fb-cover.jpg (1640x624); out: thư mục khác để xem thử."""
    d = Path(out) if out else ROOT / "content/brand"
    html_text = fb_cover_classic() if variant == "classic" else fb_cover_bold(variant) if variant in FB_COVER_BOLD else fb_cover(variant)
    return shoot([(html_text, d / ("fb-cover.jpg" if not out else f"fb-cover-{variant}.jpg"), *FB_COVER_SIZE, 1)])


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
    elif cmd == "og":  # ảnh chia sẻ mặc định của website: og [navy|cream|panel] [--out thư-mục để xem thử]
        v = args[1] if len(args) > 1 and not args[1].startswith("--") else "navy"
        print("\n".join(og_render(v, opt("--out"))))
    elif cmd == "fbcover":  # ảnh bìa Fanpage: fbcover [classic|arrow|bars|cream|pattern|columns|minimal|center|split] [--out thư-mục để xem thử]
        v = args[1] if len(args) > 1 and not args[1].startswith("--") else "arrow"
        print("\n".join(fb_cover_render(v, opt("--out"))))
    elif cmd == "sheet":
        post = find(data, int(args[1]))
        out = Path(opt("--out", ROOT / "previews/covers"))
        styles = [s for s in STYLES if s in GENERIC or themed_for(post) == s]
        jobs = [(post, k, s, out / f"{post['no']:02d}-{s}-{k}.jpg") for s in styles for k in SIZES]
        print("\n".join(render(jobs)))
