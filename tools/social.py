"""Ảnh cho bài Facebook hằng ngày (danh sách "facebook" trong content/editorial/calendar.json).

Mỗi bài có trường design (nội dung chữ trên ảnh, phiên Designer viết) và trường images (đường dẫn ảnh đã dựng,
phiên Facebook post dùng để đăng). Ảnh lưu ở content/facebook/<id>/1.jpg, 2.jpg... (carousel nhiều ảnh), khổ 1080x1080.

Mỗi dạng bài có 2 biến thể, xoay vòng theo số lần dạng đó đã xuất hiện trước đó trong lịch, để các tuần không lặp.
Nhận diện giống ảnh bìa (tools/covers.py): phẳng, navy, cam, kem; tiêu đề và số dùng Newsreader, chữ dùng Be Vietnam Pro;
không đường kẻ, không hình tròn bao chữ hoặc logo, không gradient, không bóng đổ.

design theo dạng bài (format):
  Góc số liệu          {"num", "phrase", "context", "source"}
  Thuật ngữ 1 phút     {"term", "kind", "definition", "why", "source"}
  Carousel hướng dẫn   {"title", "promise", "steps": [{"title", "body"}], "end", "source"}
  Tin nóng             {"when", "headline", "points": [...], "source"}
  Phép tính nhanh      {"title", "rows": [[nhãn, giá trị]], "result": [nhãn, giá trị], "note", "source"}
  Hiểu lầm và sự thật  {"myth", "fact", "source"}
  Câu hỏi mở           {"question", "options": [...], "context"}

Cách dùng:
  python3 tools/social.py render <id> [--out thư-mục]   dựng ảnh một bài, ghi images vào calendar.json (khi không có --out)
  python3 tools/social.py week <ngày đầu> <ngày cuối>    dựng mọi bài có design trong khoảng ngày (YYYY-MM-DD)
  python3 tools/social.py missing                       liệt kê bài sắp đăng chưa có design hoặc chưa có ảnh
"""
import html
import sys
from datetime import date
from pathlib import Path

from covers import CREAM, NAVY, ORANGE, ROOT, document, logo, shoot

SIZE = 1080
esc = html.escape

BASE = f"""
body{{color:{NAVY}}}
.lg{{position:absolute;top:64px}}
.label{{position:absolute;left:72px;top:72px;font-weight:600;font-size:28px}}
.src{{position:absolute;left:72px;bottom:60px;font-weight:500;font-size:20px;opacity:.7}}
.site{{position:absolute;right:72px;bottom:60px;font-weight:600;font-size:20px;opacity:.7}}
h1,h2{{line-height:1.12}}
h2{{font-family:NR,serif;font-weight:600;letter-spacing:-.012em}}
p{{line-height:1.42}}
"""


def frame(theme, label, source="", foot=None):
    """Khung chung: nhãn dạng bài và logo trên cùng, nguồn và tên miền ở chân ảnh.
    foot: màu nền vùng chân ảnh khi khác nền vùng trên (ví dụ ảnh hai khối màu)."""
    fg, accent = {"cream": (NAVY, ORANGE), "navy": ("#fff", ORANGE), "orange": (NAVY, NAVY)}[theme]
    ffg = {"cream": NAVY, "navy": "#fff", "orange": NAVY}[foot or theme]
    src = f'<div class="src" style="color:{ffg}">Nguồn: {esc(source)}</div>' if source else ""
    return (f'<div class="lg" style="right:72px">{logo(fg, 70)}</div><div class="label" style="color:{accent}">{esc(label)}</div>'
            f'{src}<div class="site" style="color:{ffg}">adtek.agency</div>')


BG = {"cream": CREAM, "navy": NAVY, "orange": ORANGE}
FG = {"cream": NAVY, "navy": "#fff", "orange": NAVY}


# ---------------------------------------------------------------- dạng bài

def stat(d, v):
    """Góc số liệu: số lớn đứng trên, cụm chữ đi kèm ngay dưới."""
    theme = ["cream", "navy"][v]
    num_color = ORANGE if theme != "orange" else NAVY
    n = len(d["num"])
    size = 380 if n <= 3 else 300 if n <= 5 else 230
    css = BASE + f"""
body{{background:{BG[theme]};color:{FG[theme]}}}
.copy{{position:absolute;left:72px;right:72px;top:170px;bottom:150px;display:flex;flex-direction:column;justify-content:center}}
.num{{font-size:{size}px;line-height:.8;color:{num_color};white-space:nowrap}}
h1{{font-size:76px;margin-top:-.08em;max-height:3.4em}}
p{{font-size:32px;margin-top:26px;max-height:4.4em;opacity:.85}}"""
    body = f"""{frame(theme, "Góc số liệu", d.get("source", ""))}
<div class="copy"><div class="num">{esc(d['num'])}</div><h1 class="fit bal">{esc(d['phrase'])}</h1><p class="fit">{esc(d.get('context', ''))}</p></div>"""
    return [(css, body)]


def term(d, v):
    """Thuật ngữ 1 phút: như một mục từ điển, thuật ngữ lớn, loại từ, định nghĩa, vì sao quan trọng."""
    theme = ["cream", "navy"][v]
    css = BASE + f"""
body{{background:{BG[theme]};color:{FG[theme]}}}
.copy{{position:absolute;left:72px;right:72px;top:190px}}
h1{{font-size:132px;line-height:1;color:{ORANGE if theme == 'navy' else NAVY};max-height:2.1em}}
.kind{{font-family:NR,serif;font-style:italic;font-size:34px;margin:18px 0 34px;color:{ORANGE}}}
.def{{font-size:40px;line-height:1.35;font-weight:500;max-height:5.5em}}
.why{{position:absolute;left:72px;right:72px;bottom:130px;font-size:30px;line-height:1.42;max-height:4.4em}}
.why b{{color:{ORANGE};font-weight:600}}"""
    body = f"""{frame(theme, "Thuật ngữ 1 phút", d.get("source", ""))}
<div class="copy"><h1 class="fit">{esc(d['term'])}</h1><div class="kind">{esc(d.get('kind', ''))}</div>
<div class="def fit">{esc(d['definition'])}</div></div>
<div class="why fit"><b>Vì sao quan trọng: </b>{esc(d.get('why', ''))}</div>"""
    return [(css, body)]


def myth(d, v):
    """Hiểu lầm và sự thật: hai khối màu, hiểu lầm trước (trên hoặc trái), sự thật sau."""
    if v == 0:  # trên dưới
        css = BASE + f"""
body{{background:{CREAM}}}
.a{{position:absolute;left:0;right:0;top:0;height:470px;background:{CREAM};padding:150px 72px 0}}
.b{{position:absolute;left:0;right:0;top:470px;bottom:0;background:{NAVY};color:#fff;padding:56px 72px 0}}
.t{{font-weight:600;font-size:28px;color:{ORANGE};margin-bottom:14px}}
.a h2{{font-size:76px;max-height:3.4em;color:{NAVY}}}
.b p{{font-size:40px;font-weight:500;max-height:6.2em}}
"""
        body = f"""<div class="a"><div class="t">Hiểu lầm</div><h2 class="fit bal">“{esc(d['myth'])}”</h2></div>
<div class="b"><div class="t">Sự thật</div><p class="fit">{esc(d['fact'])}</p></div>{frame("cream", "Hiểu lầm và sự thật", d.get("source", ""), foot="navy")}"""
        return [(css, body)]
    css = BASE + f"""
body{{background:{NAVY}}}
.a{{position:absolute;left:0;top:0;bottom:0;width:470px;background:{ORANGE};padding:190px 48px 0 72px;color:{NAVY}}}
.b{{position:absolute;left:470px;right:0;top:0;bottom:0;color:#fff;padding:190px 72px 0 52px}}
.t{{font-weight:600;font-size:28px;margin-bottom:16px}}
.a .t{{color:{NAVY}}}.b .t{{color:{ORANGE}}}
.a h2{{font-size:56px;max-height:9em}}
.b p{{font-size:34px;font-weight:500;max-height:15em}}"""
    body = f"""<div class="a"><div class="t">Hiểu lầm</div><h2 class="fit bal">“{esc(d['myth'])}”</h2></div>
<div class="b"><div class="t">Sự thật</div><p class="fit">{esc(d['fact'])}</p></div>
<div class="lg" style="right:72px">{logo('#fff', 70)}</div><div class="label" style="color:{NAVY}">Hiểu lầm và sự thật</div>
<div class="src" style="left:542px;color:#fff">Nguồn: {esc(d.get('source', ''))}</div>"""
    return [(css, body)]


def question(d, v):
    """Câu hỏi mở: câu hỏi lớn, các lựa chọn đánh chữ A, B, C (không khung tròn), mời trả lời ở bình luận."""
    theme = ["orange", "navy"][v]
    letter = NAVY if theme == "orange" else ORANGE
    opts = "".join(f'<li><span>{chr(65 + i)}</span>{esc(o)}</li>' for i, o in enumerate(d.get("options", [])))
    css = BASE + f"""
body{{background:{BG[theme]};color:{FG[theme]}}}
.q{{position:absolute;left:72px;right:72px;top:180px}}
.ctx{{font-size:28px;font-weight:500;margin-bottom:22px;opacity:.85;max-height:2.9em}}
h1{{font-size:96px;max-height:3.4em}}
ul{{list-style:none;margin-top:70px}}
li{{display:flex;align-items:baseline;gap:26px;font-size:40px;font-weight:600;padding:12px 0}}
li span{{font-family:NR,serif;font-size:56px;color:{letter};width:44px}}
.cta{{position:absolute;left:72px;bottom:96px;font-size:24px;font-weight:600;opacity:.8}}
.site{{display:none}}"""
    body = f"""{frame(theme, "Câu hỏi mở")}<div class="q"><div class="ctx fit">{esc(d.get('context', ''))}</div><h1 class="fit bal">{esc(d['question'])}</h1><ul>{opts}</ul></div><div class="cta">Trả lời ở phần bình luận</div>"""
    return [(css, body)]


def news(d, v):
    """Tin nóng: mốc thời gian đứng trên tiêu đề, các ý chính đánh số."""
    theme = ["navy", "cream"][v]
    pts = "".join(f'<li><span>{i + 1}</span><div>{esc(p)}</div></li>' for i, p in enumerate(d.get("points", [])))
    css = BASE + f"""
body{{background:{BG[theme]};color:{FG[theme]}}}
.copy{{position:absolute;left:72px;right:72px;top:170px}}
.when{{font-family:NR,serif;font-weight:600;font-size:120px;line-height:.9;color:{ORANGE}}}
h1{{font-size:68px;margin-top:10px;max-height:3.4em}}
ul{{list-style:none;margin-top:70px}}
li{{display:flex;gap:24px;font-size:34px;line-height:1.38;padding:12px 0}}
li span{{font-family:NR,serif;font-weight:600;font-size:40px;line-height:1;color:{ORANGE};flex:none;width:30px}}"""
    body = f"""{frame(theme, "Tin nóng", d.get("source", ""))}
<div class="copy"><div class="when">{esc(d.get('when', ''))}</div><h1 class="fit bal">{esc(d['headline'])}</h1><ul>{pts}</ul></div>"""
    return [(css, body)]


def calc(d, v):
    """Phép tính nhanh: bảng tính như hóa đơn, dòng xen kẽ màu nền (không kẻ), dòng kết quả nổi bật."""
    theme = ["cream", "navy"][v]
    band = "rgba(0,45,114,.06)" if theme == "cream" else "rgba(255,255,255,.07)"
    rows = "".join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>' for a, b in d["rows"])
    ra, rb = d["result"]
    css = BASE + f"""
body{{background:{BG[theme]};color:{FG[theme]}}}
h1{{position:absolute;left:72px;right:72px;top:150px;font-size:58px;max-height:2.3em}}
.calc{{position:absolute;left:72px;right:72px;top:340px}}
table{{width:100%;border-collapse:collapse;font-size:32px}}
td{{padding:14px 20px}}
td:last-child{{text-align:right;font-weight:600;white-space:nowrap}}
tr:nth-child(odd) td{{background:{band}}}
.res{{margin-top:22px;background:{ORANGE};color:{NAVY};display:flex;justify-content:space-between;align-items:baseline;padding:22px 20px}}
.res span{{font-size:30px;font-weight:600}}
.res b{{font-family:NR,serif;font-weight:600;font-size:64px;line-height:1}}
.note{{margin-top:16px;font-size:22px;line-height:1.4;opacity:.75}}"""
    body = f"""{frame(theme, "Phép tính nhanh", d.get("source", ""))}<h1 class="fit bal">{esc(d['title'])}</h1>
<div class="calc"><table>{rows}</table><div class="res"><span>{esc(ra)}</span><b>{esc(rb)}</b></div><div class="note">{esc(d.get('note', ''))}</div></div>"""
    return [(css, body)]


def carousel(d, v):
    """Carousel hướng dẫn: trang bìa, mỗi bước một trang (số bước lớn trên tiêu đề), trang kết. Số trang ghi chữ ở góc."""
    steps = d["steps"]
    total = len(steps) + 2
    themes = (["cream", "navy"], ["navy", "cream"])[v]
    pages = []

    def pageno(i, theme):
        return f'<div class="pg" style="color:{FG[theme]}">{i}/{total}</div>'

    common = BASE + """.pg{position:absolute;right:72px;bottom:60px;font-weight:600;font-size:22px;opacity:.7}.site{display:none}"""
    # trang bìa
    t = themes[0]
    css = common + f"""
body{{background:{BG[t]};color:{FG[t]}}}
.num{{position:absolute;left:72px;top:190px;font-size:360px;line-height:.8;color:{ORANGE}}}
h1{{position:absolute;left:72px;right:72px;top:500px;font-size:84px;max-height:3.4em}}
.go{{position:absolute;left:72px;bottom:110px;font-size:28px;font-weight:600;color:{ORANGE}}}"""
    body = f"""{frame(t, d['title'])}<div class="num">{len(steps)}</div><h1 class="fit bal">{esc(d['promise'])}</h1>
<div class="go">Lướt sang để xem từng bước</div>{pageno(1, t)}"""
    pages.append((css, body))
    # các bước, xen kẽ hai nền
    for i, s in enumerate(steps):
        t = themes[(i + 1) % 2]
        css = common + f"""
body{{background:{BG[t]};color:{FG[t]}}}
.copy{{position:absolute;left:72px;right:72px;top:170px;bottom:140px;display:flex;flex-direction:column;justify-content:center}}
.num{{font-size:300px;line-height:.8;color:{ORANGE}}}
h1{{font-size:72px;margin-top:-.05em;max-height:2.3em}}
p{{font-size:34px;margin-top:24px;max-height:6em}}"""
        body = f"""{frame(t, d['title'])}<div class="copy"><div class="num">{i + 1}</div><h1 class="fit bal">{esc(s['title'])}</h1>
<p class="fit">{esc(s['body'])}</p></div>{pageno(i + 2, t)}"""
        pages.append((css, body))
    # trang kết
    t = "orange"
    css = common + f"""
body{{background:{ORANGE};color:{NAVY}}}
h1{{position:absolute;left:72px;right:72px;top:200px;font-size:78px;max-height:4.5em}}
.go{{position:absolute;left:72px;bottom:150px;font-size:32px;font-weight:600}}"""
    src = f'<div class="src">Nguồn: {esc(d["source"])}</div>' if d.get("source") else ""
    body = f"""<div class="lg" style="right:72px">{logo(NAVY, 70)}</div><div class="label" style="color:{NAVY}">{esc(d['title'])}</div>
<h1 class="fit bal">{esc(d['end'])}</h1><div class="go">Xem bài đầy đủ ở phần bình luận</div>{src}{pageno(total, t)}"""
    pages.append((css, body))
    return pages


FORMATS = {"Góc số liệu": stat, "Thuật ngữ 1 phút": term, "Carousel hướng dẫn": carousel, "Tin nóng": news,
           "Phép tính nhanh": calc, "Hiểu lầm và sự thật": myth, "Câu hỏi mở": question}


def variant(items, item):
    """Biến thể theo số lần dạng bài này đã xuất hiện trước đó: tuần này nền kem thì tuần sau nền navy."""
    before = [x for x in items if x["format"] == item["format"] and x["date"] < item["date"]]
    return item.get("design", {}).get("variant", len(before) % 2)


def render(data, item, out=None):
    fn = FORMATS[item["format"]]
    pages = fn(item["design"], variant(data["facebook"], item))
    folder = Path(out) if out else ROOT / "content/facebook" / item["id"]
    jobs = [(document(css, body, SIZE, SIZE), folder / f"{i + 1}.jpg", SIZE, SIZE) for i, (css, body) in enumerate(pages)]
    files = shoot(jobs)
    if not out:
        for old in folder.glob("*.jpg"):  # carousel bớt trang thì xóa ảnh thừa
            if str(old) not in files:
                old.unlink()
        item["images"] = [str(Path(f).relative_to(ROOT)) for f in files]
    return files


if __name__ == "__main__":
    from blog_post import load, save

    args = sys.argv[1:]
    data = load()
    items = data["facebook"]
    out = args[args.index("--out") + 1] if "--out" in args else None
    if args[0] == "render":
        item = next(x for x in items if x["id"] == args[1])
        print("\n".join(render(data, item, out)))
    elif args[0] == "week":
        for item in items:
            if args[1] <= item["date"] <= args[2] and item.get("design") and item["format"] in FORMATS:
                print("\n".join(render(data, item, out)))
    elif args[0] == "missing":
        today = date.today().isoformat()
        for item in items:
            if item["date"] >= today and item["format"] in FORMATS and (not item.get("design") or not item.get("images")):
                print(item["id"], item["format"], "thiếu design" if not item.get("design") else "thiếu ảnh", item["title"])
    if not out and args[0] in ("render", "week"):
        save(data)
