"""Bộ mẫu ảnh bìa Adtek: nhiều phong cách, mỗi bài một phong cách khác bài trước.

Mỗi phong cách dựng được 2 khổ từ cùng dữ liệu cover trong calendar.json:
  blog  1200x630 (ảnh đại diện WordPress, ảnh xem trước khi chia sẻ link)
  fb    1080x1080 (ảnh bài đăng Facebook)

Dữ liệu dùng: cover.kicker, title, subtitle, chips (blog); cover.fb_kicker, hero, hero_text, subtitle (fb).
cover.style (không bắt buộc) ép một phong cách; bỏ trống thì pick() tự chọn.

Cách dùng:
  python3 tools/covers.py styles                     liệt kê phong cách
  python3 tools/covers.py pick                       xem phong cách tự chọn cho từng bài đã có cover
  python3 tools/covers.py render <số bài> [--style X] [--kind blog|fb|all] [--out thư-mục]
  python3 tools/covers.py sheet <số bài> [--out thư-mục]   dựng mọi phong cách cho một bài để so sánh
"""
import base64
import html
import json
import random
import re
import subprocess
import sys
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "tools/assets"
SIZES = {"blog": (1200, 630), "fb": (1080, 1080)}
NAVY, ORANGE, CREAM = "#002D72", "#FF9014", "#F4EEE3"
esc = html.escape

HEAD = Template("""<!doctype html><html><head><meta charset="utf-8"><style>
$fontcss
*{box-sizing:border-box;margin:0;padding:0}
body{width:${w}px;height:${h}px;overflow:hidden;position:relative;font-family:BVP,sans-serif;-webkit-font-smoothing:antialiased}
.fit{overflow:hidden;padding-top:.1em}.bal{text-wrap:balance}.abs{position:absolute}
.logo{aspect-ratio:440/369;-webkit-mask:url($logo) center/contain no-repeat;mask:url($logo) center/contain no-repeat}
$css
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


def font_css():
    """Be Vietnam Pro tách 2 file (tiếng Việt, Latin): mỗi file một @font-face kèm unicode-range."""
    d = (ASSETS / "fonts").as_uri()
    return "\n".join(f"@font-face{{font-family:BVP;font-weight:{w};src:url({d}/be-vietnam-pro-{sub}-{w}-normal.woff2);unicode-range:{r}}}"
                     for w in (600, 700, 800, 900) for sub, r in (("vietnamese", VI), ("latin", LATIN)))


def logo(color, height, extra=""):
    return f'<div class="logo" style="height:{height}px;background:{color};{extra}"></div>'


def fields(post, kind):
    c = post["cover"]
    fb = kind == "fb"
    return {
        "kicker": esc((c.get("fb_kicker") or c["kicker"]) if fb else c["kicker"]),
        "head": esc((c.get("hero_text") or c["title"]) if fb else c["title"]),
        "num": esc(c.get("hero") or f"{post['no']:02d}"),
        "cap": esc(c.get("hero_text") or ""),
        "title": esc(c["title"]),
        "sub": esc(c["subtitle"]),
        "chips": [esc(x) for x in c.get("chips", [])[:4]],
        "no": post["no"],
        "date": ".".join(reversed(post["date"].split("-")[1:])) + "." + post["date"][:4],
        "rng": random.Random(post["no"] * 7919),  # trang trí khác nhau theo bài nhưng dựng lại vẫn y hệt
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
.ls .wrap{{align-items:flex-start}}
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
    """Tạp chí: nền kem, số cam khổng lồ có bóng in lệch, chữ xanh navy, đường kẻ mảnh."""
    n = len(f["num"])
    hero = (560 if n == 1 else 440 if n == 2 else 300) if sq else (400 if n == 1 else 330 if n == 2 else 220)
    css = f"""
body{{background:{CREAM};color:{NAVY}}}
body::after{{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,45,114,.025) 0 1px,transparent 1px 4px);pointer-events:none}}
.mast{{position:absolute;left:var(--px);right:var(--px);top:var(--py);display:flex;align-items:center;justify-content:space-between;
border-bottom:3px solid {NAVY};padding-bottom:var(--mb)}}
.mast .meta{{text-align:right;font-weight:800;font-size:var(--meta);letter-spacing:4px;text-transform:uppercase;line-height:1.5}}
.mast .meta b{{color:{ORANGE}}}
.num{{position:absolute;font-weight:900;font-size:{hero}px;line-height:.8;letter-spacing:-.06em;color:{ORANGE};
text-shadow:.035em .035em 0 {NAVY};white-space:nowrap}}
.copy{{position:absolute;left:var(--px)}}
.kicker{{font-weight:800;font-size:var(--kick);letter-spacing:4px;text-transform:uppercase;display:flex;align-items:center;gap:14px}}
.kicker i{{width:.7em;height:.7em;background:{ORANGE};display:block}}
h1{{font-weight:900;line-height:1.16;letter-spacing:-.01em;margin:.3em 0 .35em}}
.sub{{font-weight:600;line-height:1.4;color:rgba(0,45,114,.78)}}
.foot{{position:absolute;left:var(--px);right:var(--px);bottom:var(--py);border-top:1.5px solid rgba(0,45,114,.35);padding-top:18px;
display:flex;justify-content:space-between;font-weight:700;font-size:var(--foot);letter-spacing:1px}}
.foot span+span::before{{content:"/";margin:0 14px;color:{ORANGE}}}
.sq{{--px:72px;--py:64px;--mb:22px;--meta:20px;--kick:28px;--foot:24px}}
.sq .num{{right:40px;top:140px}}
.sq .copy{{right:72px;bottom:150px}}
.sq h1{{font-size:88px;max-height:3.6em;max-width:620px}}
.sq .sub{{font-size:36px;max-width:820px;max-height:4.5em}}
.ls{{--px:64px;--py:48px;--mb:16px;--meta:15px;--kick:22px;--foot:19px}}
.ls .num{{right:40px;top:120px}}
.ls .copy{{top:150px;width:700px}}
.ls h1{{font-size:72px;max-height:2.5em}}
.ls .sub{{font-size:27px;max-height:4.5em}}"""
    chips = "".join(f"<span>{x}</span>" for x in f["chips"][:3])
    body = f"""<div class="mast">{logo(NAVY, 78 if sq else 58)}<div class="meta">Adtek <b>Insights</b><br>Số {f['no']:02d} · {f['date']}</div></div>
<div class="num">{f['num']}</div>
<div class="copy"><div class="kicker"><i></i>{f['kicker']}</div><h1 class="fit bal">{f['head']}</h1><div class="sub fit">{f['sub']}</div></div>
<div class="foot"><div>{chips}</div><div>adtek.agency</div></div>"""
    return css, body


def split(f, sq):
    """Khối tương phản: mảng cam cắt chéo chứa số navy, nửa còn lại navy chứa tiêu đề."""
    n = len(f["num"])
    if sq:
        hero = 520 if n == 1 else 400 if n == 2 else 260
        css = f"""
body{{background:{NAVY};color:#fff}}
.panel{{position:absolute;left:0;top:0;right:0;height:560px;background:{ORANGE};clip-path:polygon(0 0,100% 0,100% 74%,0 100%)}}
.panel::after{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 85% 20%,rgba(255,255,255,.35),transparent 45%)}}
.num{{position:absolute;left:56px;top:60px;font-weight:900;font-size:{hero}px;line-height:.82;letter-spacing:-.05em;color:{NAVY};white-space:nowrap;z-index:1}}
.cap{{position:absolute;right:72px;top:250px;width:420px;font-weight:900;font-size:46px;line-height:1.12;color:{NAVY};text-transform:uppercase;max-height:4.7em;z-index:1}}
.lg{{position:absolute;right:72px;top:64px;z-index:1}}
.copy{{position:absolute;left:72px;right:72px;bottom:72px}}
.kicker{{color:{ORANGE};font-weight:800;font-size:26px;letter-spacing:4px;text-transform:uppercase}}
h1{{font-weight:900;font-size:68px;line-height:1.12;margin:16px 0 22px;max-height:3.6em}}
.chips{{display:flex;flex-wrap:wrap;gap:12px}}
.chips span{{border:2px solid rgba(255,255,255,.35);border-radius:40px;padding:10px 22px;font-weight:700;font-size:24px}}
.chips span:first-child{{border-color:{ORANGE};color:{ORANGE}}}
.sub{{font-weight:600;font-size:32px;line-height:1.4;color:#C9D6EE;max-height:4.5em}}"""
        body = f"""<div class="panel"></div><div class="num">{f['num']}</div><div class="lg">{logo(NAVY, 92)}</div>
<div class="cap fit bal">{f['cap'] or f['kicker']}</div>
<div class="copy"><div class="kicker">{f['kicker']}</div><h1 class="fit bal">{f['head'] if f['head'] != f['cap'] else f['sub']}</h1>
{'' if f['head'] == f['cap'] else f'<div class="sub fit">{f["sub"]}</div>'}<div class="chips">{"".join(f"<span>{x}</span>" for x in f["chips"][:3])}</div></div>"""
        return css, body
    hero = 400 if n == 1 else 300 if n == 2 else 190
    chips = "".join(f"<span>{x}</span>" for x in f["chips"])
    css = f"""
body{{background:{NAVY};color:#fff}}
.panel{{position:absolute;left:0;top:0;bottom:0;width:470px;background:{ORANGE};clip-path:polygon(0 0,100% 0,78% 100%,0 100%)}}
.panel::after{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 20% 15%,rgba(255,255,255,.35),transparent 50%)}}
.num{{position:absolute;left:40px;top:50%;transform:translateY(-54%);width:360px;text-align:center;font-weight:900;font-size:{hero}px;line-height:.82;letter-spacing:-.05em;color:{NAVY};white-space:nowrap}}
.cap{{position:absolute;left:40px;bottom:46px;width:320px;text-align:center;font-weight:800;font-size:22px;line-height:1.25;color:{NAVY};max-height:2.7em}}
.copy{{position:absolute;left:500px;right:64px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}}
.lg{{position:absolute;right:56px;top:44px}}
.kicker{{color:{ORANGE};font-weight:800;font-size:22px;letter-spacing:4px;text-transform:uppercase}}
h1{{font-weight:900;font-size:76px;line-height:1.16;margin:14px 0 18px;max-height:2.5em}}
.sub{{font-weight:600;font-size:26px;line-height:1.4;color:#C9D6EE;max-height:4.5em}}
.chips{{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}}
.chips span{{border:1.5px solid rgba(255,255,255,.35);border-radius:40px;padding:8px 18px;font-weight:700;font-size:18px}}
.chips span:first-child{{border-color:{ORANGE};color:{ORANGE}}}"""
    body = f"""<div class="panel"></div><div class="num">{f['num']}</div><div class="cap fit bal">{f['cap']}</div>
<div class="lg">{logo('#fff', 64)}</div>
<div class="copy"><div class="kicker">{f['kicker']}</div><h1 class="fit bal">{f['head']}</h1><div class="sub fit">{f['sub']}</div><div class="chips">{chips}</div></div>"""
    return css, body


def dashboard(f, sq):
    """Bảng số liệu: nền xanh đêm chấm lưới, thẻ báo cáo kính mờ có biểu đồ tăng trưởng và KPI cam."""
    rng = f["rng"]
    pts, y = [], 150
    for i in range(9):
        y = max(18, min(165, y - rng.uniform(-6, 26)))
        pts.append((i * 50, y))
    line = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    area = f"0,190 {line} 400,190"
    bars = "".join(f'<rect x="{i * 34}" y="{60 - h:.0f}" width="22" height="{h:.0f}" rx="4" fill="{ORANGE if i == 6 else "rgba(255,255,255,.22)"}"/>'
                   for i, h in enumerate(rng.uniform(14, 58) for _ in range(8)))
    tabs = "".join(f"<span>{x}</span>" for x in f["chips"][:3]) or "<span>Report</span>"
    card = f"""<div class="card"><div class="bar"><i></i><i></i><i></i><div class="tabs">{tabs}</div></div>
<div class="kpi"><div class="v">{f['num']}</div><div class="l fit bal">{f['cap'] or f['kicker']}</div></div>
<svg class="chart" viewBox="0 0 400 190" preserveAspectRatio="none"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{ORANGE}" stop-opacity=".45"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></linearGradient></defs>
<path d="M0 47H400M0 95H400M0 143H400" stroke="rgba(255,255,255,.08)"/><polygon points="{area}" fill="url(#g)"/>
<polyline points="{line}" fill="none" stroke="{ORANGE}" stroke-width="3.5" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>
<circle cx="{pts[-1][0]}" cy="{pts[-1][1]:.0f}" r="7" fill="#fff" stroke="{ORANGE}" stroke-width="4"/></svg>
<svg class="bars" viewBox="0 0 270 60">{bars}</svg></div>"""
    css = f"""
body{{color:#fff;background:radial-gradient(circle at 12% 8%,rgba(40,110,255,.45),transparent 42%),radial-gradient(circle at 95% 100%,rgba(255,144,20,.22),transparent 40%),#061533}}
body::before{{content:"";position:absolute;inset:0;background:radial-gradient(rgba(255,255,255,.16) 1.2px,transparent 1.3px) 0 0/28px 28px;
-webkit-mask:linear-gradient(180deg,#000,transparent 85%)}}
.kicker{{display:inline-block;border:1.5px solid {ORANGE};color:{ORANGE};border-radius:40px;font-weight:800;letter-spacing:3px;text-transform:uppercase}}
h1{{font-weight:900;line-height:1.16}}
.sub{{font-weight:600;line-height:1.42;color:#B8C7E6}}
.card{{position:absolute;border-radius:26px;background:linear-gradient(160deg,rgba(255,255,255,.13),rgba(255,255,255,.04));
border:1.5px solid rgba(255,255,255,.18);box-shadow:0 40px 80px rgba(0,0,0,.45);backdrop-filter:blur(10px);padding:22px 26px}}
.bar{{display:flex;align-items:center;gap:8px}}.bar i{{width:12px;height:12px;border-radius:50%;background:rgba(255,255,255,.25)}}
.bar i:first-child{{background:{ORANGE}}}
.tabs{{margin-left:auto;display:flex;gap:8px}}.tabs span{{font-weight:700;font-size:15px;padding:6px 12px;border-radius:8px;background:rgba(255,255,255,.08);color:#C9D6EE;white-space:nowrap}}
.tabs span:first-child{{background:rgba(255,144,20,.18);color:{ORANGE}}}
.kpi{{display:flex;align-items:center;gap:20px;margin:18px 0 6px}}
.kpi .v{{font-weight:900;line-height:.9;color:{ORANGE};letter-spacing:-.04em;white-space:nowrap}}
.kpi .l{{font-weight:800;line-height:1.2;color:#fff;max-height:3.8em}}
.chart{{display:block;width:100%}}.bars{{display:block;margin-top:14px}}
.sq .top{{position:absolute;left:72px;right:72px;top:64px}}
.sq .lg{{position:absolute;right:72px;top:64px}}
.sq .kicker{{font-size:22px;padding:10px 20px}}
.sq h1{{font-size:78px;margin:26px 0 18px;max-height:2.5em}}
.sq .sub{{font-size:30px;max-height:4.5em;max-width:880px}}
.sq .card{{left:72px;right:72px;bottom:-30px;height:530px;transform:perspective(1400px) rotateX(10deg);transform-origin:bottom}}
.sq .kpi .v{{font-size:120px}}.sq .kpi .l{{font-size:32px}}
.sq .chart{{height:250px}}.sq .bars{{width:290px;height:64px}}
.ls .top{{position:absolute;left:64px;top:0;bottom:0;width:560px;display:flex;flex-direction:column;justify-content:center}}
.ls .lg{{position:absolute;left:64px;top:44px}}
.ls .kicker{{font-size:17px;padding:8px 16px;align-self:flex-start}}
.ls h1{{font-size:64px;margin:20px 0 16px;max-height:2.5em}}
.ls .sub{{font-size:24px;max-height:4.5em}}
.ls .card{{left:680px;width:470px;top:70px;bottom:70px;transform:perspective(1200px) rotateY(-12deg) rotateZ(-1.5deg)}}
.ls .kpi .v{{font-size:96px}}.ls .kpi .l{{font-size:22px}}
.ls .chart{{height:180px}}.ls .bars{{width:230px;height:50px}}"""
    body = f"""<div class="lg">{logo('#fff', 70 if sq else 52)}</div>
<div class="top"><div class="kicker">{f['kicker']}</div><h1 class="fit bal">{f['head'] if not sq else f['head']}</h1><div class="sub fit">{f['sub']}</div></div>{card}"""
    if sq:  # khổ vuông: logo nằm cạnh nhãn, tránh chồng chữ
        body = body.replace('<div class="top">', '<div class="top" style="right:200px">')
    return css, body


def aurora(f, sq):
    """Kính mờ: nền đêm với quầng sáng cam và xanh, thẻ kính chứa tiêu đề, số viền rỗng khổng lồ phía sau."""
    rng = f["rng"]
    orbs = [(ORANGE, rng.uniform(55, 85), rng.uniform(5, 35), 46), ("#1E5BFF", rng.uniform(5, 30), rng.uniform(55, 90), 52),
            ("#7B3DFF", rng.uniform(60, 95), rng.uniform(65, 95), 38)]
    orb_html = "".join(f'<div class="orb" style="left:{x:.0f}%;top:{y:.0f}%;width:{s}%;background:{c}"></div>' for c, x, y, s in orbs)
    n = len(f["num"])
    hero = (900 if n == 1 else 700 if n == 2 else 420) if sq else (680 if n == 1 else 520 if n == 2 else 320)
    chips = " · ".join(f["chips"][:3])
    css = f"""
body{{background:#040B26;color:#fff}}
.orb{{position:absolute;aspect-ratio:1;border-radius:50%;transform:translate(-50%,-50%);filter:blur(90px);opacity:.85}}
.grain{{position:absolute;inset:0;opacity:.12;mix-blend-mode:overlay}}
.num{{position:absolute;font-weight:900;font-size:{hero}px;line-height:.8;letter-spacing:-.05em;color:transparent;
-webkit-text-stroke:3px rgba(255,255,255,.28);white-space:nowrap}}
.glass{{position:absolute;border-radius:36px;background:rgba(255,255,255,.09);border:1.5px solid rgba(255,255,255,.28);
backdrop-filter:blur(26px) saturate(140%);box-shadow:0 30px 80px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.35);display:flex;flex-direction:column}}
.kicker{{align-self:flex-start;background:{ORANGE};color:#1A1240;border-radius:40px;font-weight:800;letter-spacing:3px;text-transform:uppercase}}
h1{{font-weight:900;line-height:1.16}}
.sub{{font-weight:600;line-height:1.42;color:rgba(255,255,255,.82)}}
.foot{{margin-top:auto;display:flex;align-items:center;justify-content:space-between;border-top:1px solid rgba(255,255,255,.2);font-weight:700;color:rgba(255,255,255,.75)}}
.sq .num{{right:-30px;top:-60px}}
.sq .glass{{left:72px;right:72px;bottom:72px;height:600px;padding:52px 56px 40px}}
.sq .kicker{{font-size:22px;padding:11px 22px}}
.sq h1{{font-size:84px;margin:30px 0 22px;max-height:3.6em}}
.sq .sub{{font-size:32px;max-height:4.5em}}
.sq .foot{{padding-top:26px;font-size:22px}}
.ls .num{{right:-20px;top:-40px}}
.ls .glass{{left:64px;top:56px;bottom:56px;width:760px;padding:40px 46px 30px}}
.ls .kicker{{font-size:16px;padding:8px 18px}}
.ls h1{{font-size:78px;margin:22px 0 16px;max-height:2.5em}}
.ls .sub{{font-size:26px;max-height:4.5em}}
.ls .foot{{padding-top:18px;font-size:17px}}
.ls .side{{position:absolute;right:64px;bottom:56px}}"""
    grain = """<svg class="grain" width="100%" height="100%"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>"""
    foot = f'<div class="foot">{logo("#fff", 54 if sq else 40)}<div>{chips}</div></div>'
    body = f"""{orb_html}{grain}<div class="num">{f['num']}</div>
<div class="glass"><div class="kicker">{f['kicker']}</div><h1 class="fit bal">{f['head']}</h1><div class="sub fit">{f['sub']}</div>{foot}</div>"""
    return css, body


def poster(f, sq):
    """Áp phích: nền cam phủ kín, số navy khổng lồ tràn mép, tiêu đề in hoa đậm."""
    n = len(f["num"])
    hero = (720 if n == 1 else 600 if n == 2 else 400) if sq else (720 if n == 1 else 560 if n == 2 else 330)
    css = f"""
body{{background:{ORANGE};color:{NAVY}}}
body::before{{content:"";position:absolute;inset:0;background:repeating-linear-gradient(-45deg,rgba(0,45,114,.06) 0 2px,transparent 2px 22px)}}
.num{{position:absolute;font-weight:900;font-size:{hero}px;line-height:.78;letter-spacing:-.06em;color:{NAVY};white-space:nowrap}}
.ring{{position:absolute;border-radius:50%;border:3px solid {NAVY}}}
.kicker{{display:inline-block;background:{NAVY};color:{ORANGE};font-weight:800;letter-spacing:4px;text-transform:uppercase}}
h1{{font-weight:900;line-height:1.16;text-transform:uppercase;letter-spacing:-.01em}}
.sub{{font-weight:700;line-height:1.38}}
.lg{{position:absolute}}
.sq .num{{left:-30px;top:30px}}
.sq .ring{{width:300px;height:300px;right:-90px;top:-90px}}
.sq .lg{{right:72px;top:64px}}
.sq .copy{{position:absolute;left:72px;right:72px;bottom:72px}}
.sq .kicker{{font-size:24px;padding:10px 18px}}
.sq h1{{font-size:88px;margin:24px 0 20px;max-height:3.6em}}
.sq .sub{{font-size:32px;max-height:4.4em;border-left:8px solid {NAVY};padding-left:24px}}
.ls .num{{left:-30px;bottom:-40px}}
.ls .ring{{width:220px;height:220px;right:-70px;bottom:-70px}}
.ls .lg{{right:64px;top:48px}}
.ls .copy{{position:absolute;left:{'480' if n <= 2 else '560'}px;right:64px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;align-items:flex-start}}
.ls .kicker{{font-size:18px;padding:8px 14px}}
.ls h1{{font-size:66px;margin:18px 0 16px;max-height:3.6em}}
.ls .sub{{font-size:24px;max-height:4.4em;border-left:6px solid {NAVY};padding-left:18px}}"""
    body = f"""<div class="ring"></div><div class="num">{f['num']}</div><div class="lg">{logo(NAVY, 86 if sq else 62)}</div>
<div class="copy"><div class="kicker">{f['kicker']}</div><h1 class="fit bal">{f['head']}</h1><div class="sub fit">{f['sub']}</div></div>"""
    return css, body


def versus(f, sq):
    """Đối đầu: dành cho bài so sánh "A vs B", hai nửa navy và cam cắt chéo, huy hiệu VS ở giữa."""
    src = html.unescape(f["title"])
    a, b = (re.split(r"\s+vs\.?\s+", src, flags=re.I) + ["", ""])[:2]
    a, b = esc(a.strip()), esc(re.sub(r"\s*(19|20)\d\d$", "", b.strip()))
    css = f"""
body{{background:{ORANGE};color:#fff}}
.l{{position:absolute;inset:0;background:{NAVY};clip-path:polygon(0 0,58% 0,42% 100%,0 100%)}}
.l::after{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 20% 30%,rgba(60,120,255,.35),transparent 55%)}}
.r::after{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 85% 70%,rgba(255,255,255,.3),transparent 50%)}}
.r{{position:absolute;inset:0}}
.name{{position:absolute;font-weight:900;line-height:1.16;text-transform:uppercase;letter-spacing:-.01em}}
.na{{color:#fff}}.nb{{color:{NAVY};text-align:right}}
.vs{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;background:#fff;color:{NAVY};
display:flex;align-items:center;justify-content:center;font-weight:900;letter-spacing:-.04em;box-shadow:0 0 0 14px rgba(255,255,255,.25),0 20px 50px rgba(0,0,0,.35)}}
.kicker{{position:absolute;font-weight:800;letter-spacing:4px;text-transform:uppercase;color:{ORANGE}}}
.band{{position:absolute;background:#fff;color:{NAVY};font-weight:800;line-height:1.35;border-radius:20px;box-shadow:0 18px 40px rgba(0,0,0,.25)}}
.lg{{position:absolute}}
.sq .lg{{left:72px;top:64px}}.sq .kicker{{left:72px;top:190px;font-size:24px}}
.sq .na{{left:72px;top:270px;width:420px;font-size:96px;max-height:2.5em}}
.sq .nb{{right:72px;top:660px;width:420px;font-size:96px;max-height:2.5em}}
.sq .vs{{width:170px;height:170px;font-size:70px;top:52%}}
.sq .band{{left:72px;right:72px;bottom:64px;padding:26px 34px;font-size:34px;max-height:4.4em}}
.ls .lg{{left:56px;top:44px}}.ls .kicker{{left:56px;top:140px;font-size:18px}}
.ls .na{{left:56px;top:190px;width:440px;font-size:80px;max-height:2.5em}}
.ls .nb{{right:56px;top:190px;width:440px;font-size:80px;max-height:2.5em}}
.ls .vs{{width:128px;height:128px;font-size:52px;top:46%}}
.ls .band{{left:50%;transform:translateX(-50%);bottom:44px;width:820px;text-align:center;padding:18px 28px;font-size:25px;max-height:3.6em}}"""
    cap = html.unescape(f["cap"])
    if cap[1:2].islower() and cap.split()[0] not in src:  # "Sàn, chia..." đọc liền sau số: "2 sàn, chia..."
        cap = cap[0].lower() + cap[1:]
    band = f"{f['num']} {esc(cap)}" if sq and cap else f["sub"]
    body = f"""<div class="r"></div><div class="l"></div><div class="lg">{logo('#fff', 80 if sq else 58)}</div>
<div class="kicker">{f['kicker']}</div><div class="name na fit bal">{a}</div><div class="name nb fit bal">{b}</div>
<div class="vs">VS</div><div class="band fit bal">{band}</div>"""
    return css, body


def dossier(f, sq):
    """Hồ sơ pháp lý: dành cho bài luật, nghị định. Tờ hồ sơ nghiêng có checklist và con dấu cam."""
    check = '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    items = "".join(f"<li><b>{check}</b>{x}</li>" for x in f["chips"])
    year = re.search(r"(19|20)\d\d", f["kicker"] + f["head"] + f["date"]).group(0)
    stamp = f"""<svg class="stamp" viewBox="0 0 200 200"><defs><path id="c" d="M100 100m-72 0a72 72 0 1 1 144 0a72 72 0 1 1-144 0"/></defs>
<circle cx="100" cy="100" r="94" fill="none" stroke="{ORANGE}" stroke-width="5"/><circle cx="100" cy="100" r="58" fill="none" stroke="{ORANGE}" stroke-width="2.5"/>
<text font-family="BVP" font-weight="800" font-size="17" letter-spacing="5" fill="{ORANGE}"><textPath href="#c">ADTEK · TUÂN THỦ · ADTEK · TUÂN THỦ ·</textPath></text>
<text x="100" y="114" text-anchor="middle" font-family="BVP" font-weight="900" font-size="40" fill="{ORANGE}">{year}</text></svg>"""
    css = f"""
body{{color:#fff;background:repeating-linear-gradient(135deg,rgba(255,255,255,.035) 0 2px,transparent 2px 18px),linear-gradient(160deg,#00398F,{NAVY} 45%,#001A45)}}
.kicker{{color:{ORANGE};font-weight:800;letter-spacing:4px;text-transform:uppercase}}
h1{{font-weight:900;line-height:1.16}}
.sub{{font-weight:600;line-height:1.42;color:#C9D6EE}}
.paper{{position:absolute;background:{CREAM};color:{NAVY};border-radius:10px;box-shadow:0 40px 80px rgba(0,0,0,.45);transform:rotate(-3.5deg)}}
.paper::before{{content:"";position:absolute;left:0;right:0;top:0;height:14px;background:{ORANGE};border-radius:10px 10px 0 0}}
.paper h5{{font-weight:800;letter-spacing:4px;text-transform:uppercase;color:rgba(0,45,114,.6)}}
.paper .num{{font-weight:900;line-height:1;color:{NAVY}}}
.paper .ln{{height:10px;border-radius:5px;background:rgba(0,45,114,.12);margin:12px 0}}
.paper ul{{list-style:none}}
.paper li{{display:flex;align-items:center;font-weight:800;border-bottom:1.5px dashed rgba(0,45,114,.2)}}
.paper li b{{flex:none;background:{ORANGE};border-radius:8px;display:flex}}
.stamp{{position:absolute;transform:rotate(-14deg);mix-blend-mode:multiply;opacity:.9}}
.sq .lg{{position:absolute;left:72px;top:64px}}
.sq .copy{{position:absolute;left:72px;right:72px;top:190px}}
.sq .kicker{{font-size:24px}}.sq h1{{font-size:76px;margin:16px 0 16px;max-height:2.5em}}.sq .sub{{font-size:30px;max-height:4.5em}}
.sq .paper{{left:110px;right:110px;bottom:-70px;height:520px;padding:50px 54px}}
.sq .paper h5{{font-size:19px}}.sq .paper li{{font-size:31px;gap:20px;padding:15px 0}}.sq .paper li b{{width:44px;height:44px;padding:7px}}
.sq .stamp{{width:230px;right:-40px;top:-60px}}
.ls .lg{{position:absolute;left:64px;top:46px}}
.ls .copy{{position:absolute;left:64px;width:600px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;padding-top:40px}}
.ls .kicker{{font-size:19px}}.ls h1{{font-size:64px;margin:14px 0 14px;max-height:2.5em}}.ls .sub{{font-size:24px;max-height:4.5em}}
.ls .paper{{left:730px;width:420px;top:60px;bottom:-60px;padding:42px 38px}}
.ls .paper h5{{font-size:14px}}.ls .paper li{{font-size:21px;gap:14px;padding:11px 0}}.ls .paper li b{{width:32px;height:32px;padding:5px}}
.ls .stamp{{width:170px;right:-50px;top:-50px}}"""
    body = f"""<div class="lg">{logo('#fff', 74 if sq else 56)}</div>
<div class="copy"><div class="kicker">{f['kicker']}</div><h1 class="fit bal">{f['head']}</h1><div class="sub fit">{f['sub']}</div></div>
<div class="paper"><h5>Hồ sơ tuân thủ · Số {f['no']:02d}</h5><div class="ln" style="width:70%"></div><div class="ln" style="width:45%"></div>
<ul>{items}</ul>{stamp}</div>"""
    return css, body


# Phong cách dùng chung cho mọi bài, và phong cách theo chủ đề (chỉ dùng khi bài hợp).
GENERIC = {"neon3d": neon3d, "editorial": editorial, "split": split, "dashboard": dashboard, "aurora": aurora, "poster": poster}
THEMED = {"versus": versus, "dossier": dossier}
STYLES = {**GENERIC, **THEMED}
LABELS = {"neon3d": "Tím neon 3D (mẫu đã duyệt)", "editorial": "Tạp chí nền kem", "split": "Khối tương phản cắt chéo",
          "dashboard": "Bảng số liệu", "aurora": "Kính mờ quầng sáng", "poster": "Áp phích nền cam",
          "versus": "Đối đầu A vs B (bài so sánh)", "dossier": "Hồ sơ pháp lý (bài luật)"}


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


def page(post, kind, style):
    w, h = SIZES[kind]
    css, body = STYLES[style](fields(post, kind), w == h)
    # mask-image không đọc được file:// (chặn CORS) nên nhúng logo dạng data URI
    logo_uri = "data:image/png;base64," + base64.b64encode((ASSETS / "adtek-logo-white.png").read_bytes()).decode()
    return HEAD.substitute(fontcss=font_css(), logo=logo_uri,
                           w=w, h=h, css=css, body=body, shape="sq" if w == h else "ls")


def render(jobs):
    """jobs: danh sách (post, kind, style, output). Dựng tất cả trong một lần mở trình duyệt."""
    tmp = ROOT / "previews/_covers"
    tmp.mkdir(parents=True, exist_ok=True)
    manifest = []
    for i, (post, kind, style, out) in enumerate(jobs):
        src = tmp / f"{i}-{post['slug']}-{kind}-{style}.html"
        src.write_text(page(post, kind, style), encoding="utf-8")
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        w, h = SIZES[kind]
        manifest.append({"input": str(src), "output": str(out), "width": w, "height": h})
    mf = tmp / "jobs.json"
    mf.write_text(json.dumps(manifest), encoding="utf-8")
    subprocess.run(["node", str(ROOT / "tools/render_cover.js"), str(mf)], check=True)
    for p in tmp.iterdir():
        p.unlink()
    tmp.rmdir()
    return [m["output"] for m in manifest]


def output_path(post, kind):
    return ROOT / f"content/posts/{post['slug']}-{'cover' if kind == 'blog' else 'fb'}.jpg"


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
    elif cmd == "sheet":
        post = find(data, int(args[1]))
        out = Path(opt("--out", ROOT / "previews/covers"))
        styles = [s for s in STYLES if s in GENERIC or themed_for(post) == s]
        jobs = [(post, k, s, out / f"{post['no']:02d}-{s}-{k}.jpg") for s in styles for k in SIZES]
        print("\n".join(render(jobs)))
