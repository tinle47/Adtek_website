"""Tài liệu hướng dẫn thương hiệu Adtek: PDF khổ ngang 1920x1080, bố cục theo tài liệu mẫu TASECO Land anh Tin gửi (16/10/2026).

Nội dung lấy từ website (trang chủ, Hỏi đáp: content/pages/home.json, faq.json), quy tắc văn phong (content/editorial/van-phong.md)
và bộ quy tắc thiết kế đã duyệt (tools/covers.py, content/editorial/README.md). Phần chưa có nguồn (tính cách, khẩu hiệu tiếng Việt,
thông điệp) ghi rõ "Đề xuất, chờ duyệt". Phần ứng dụng dùng ảnh thật đã dựng (ảnh bìa blog, ảnh Facebook, bìa báo cáo).

Logo: chỉ có bản ảnh 440x369 (logo dọc, chữ A màu chuyển navy sang hồng, chữ ADTEK màu mực). tools/assets/adtek-logo-color-hd.png
là bản phóng 6 lần, làm mịn mép; các bản một màu dựng từ kênh trong suốt của file này.

Cách dùng:
  python3 tools/brand_guide.py      ghi content/brand/adtek-brand-guidelines.pdf và ảnh xem trước previews/brand-guide/NN.jpg
"""
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from covers import ASSETS, CREAM, NAVY, ORANGE, ROOT, esc, font_css, hl  # noqa: E402

W, H = 1920, 1080
INK = "#101624"  # màu chữ ADTEK trong logo
GRAD = ("#1B4075", "#676E9B", "#E1B3CF")  # màu chuyển của chữ A trong logo (lấy mẫu từ file logo)
BUILD = ROOT / "previews/_brand"
OUT = ROOT / "content/brand/adtek-brand-guidelines.pdf"
PREVIEW = ROOT / "previews/brand-guide"
REPORTS = ["thuong-mai-dien-tu-viet-nam-9-thang-2026", "10-nganh-tang-truong-viet-nam-2026",
           "tim-kiem-quang-cao-thoi-ai-2026", "cam-nang-phap-ly-marketing-2026"]
DOC = "Hướng dẫn thương hiệu Adtek"


# ---------------------------------------------------------------- ảnh logo các màu

def build_assets():
    """Logo và dấu A các màu (PNG tô sẵn màu: PDF in mask CSS hay để lại viền mảnh), ảnh báo cáo lấy từ nhánh claude/report-covers."""
    BUILD.mkdir(parents=True, exist_ok=True)
    color = Image.open(ASSETS / "adtek-logo-color-hd.png")
    color = color.resize((1320, round(1320 * color.height / color.width)), Image.LANCZOS)
    alpha = color.getchannel("A")
    out = {"logo-color": color}
    for name, rgb in {"logo-white": "#ffffff", "logo-navy": NAVY, "logo-ink": INK, "logo-orange": ORANGE}.items():
        im = Image.new("RGBA", color.size, rgb)
        im.putalpha(alpha)
        out[name] = im
    mark = Image.open(ASSETS / "adtek-mark-white-hd.png")
    mark = mark.resize((1140, round(1140 * mark.height / mark.width)), Image.LANCZOS)
    for name, rgb in {"mark-white": "#ffffff", "mark-orange": ORANGE, "mark-navy": NAVY}.items():
        im = Image.new("RGBA", mark.size, rgb)
        im.putalpha(mark.getchannel("A"))
        out[name] = im
    mc = Image.open(ASSETS / "adtek-mark-color-hd.png")
    out["mark-color"] = mc.resize((1140, round(1140 * mc.height / mc.width)), Image.LANCZOS)
    split = round(color.height * 253 / 371)  # hàng ngăn chữ A và chữ ADTEK trong logo gốc 440x371
    word = color.crop((0, split, color.width, color.height))
    out["wordmark"] = word.crop(word.getbbox())
    uris = {}
    for name, im in out.items():
        p = BUILD / f"{name}.png"
        im.save(p, optimize=True)
        uris[name] = p.as_uri()
    for slug in REPORTS:
        p = BUILD / f"report-{slug}.jpg"
        local = ROOT / f"content/reports/{slug}-cover.jpg"
        if local.exists():
            shutil.copy(local, p)
        else:
            blob = subprocess.run(["git", "show", f"origin/claude/report-covers:content/reports/{slug}-cover.jpg"],
                                  cwd=ROOT, capture_output=True, check=True).stdout
            p.write_bytes(blob)
        uris[f"report-{slug}"] = p.as_uri()
    return uris


def img(uri, style="", cls=""):
    return f'<img src="{uri}" class="{cls}" style="{style}">'


def file_uri(rel):
    return (ROOT / rel).as_uri()


# ---------------------------------------------------------------- khung trang

CSS = f"""
@page{{size:{W}px {H}px;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:IT,sans-serif;color:{NAVY};-webkit-font-smoothing:antialiased}}
.page{{width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{CREAM};break-after:page}}
.page.dark{{background:{NAVY};color:#fff}}
.hdr{{position:absolute;left:96px;right:96px;top:44px;display:flex;justify-content:space-between;font-size:15px;font-weight:500;opacity:.6}}
.hdr .pn{{font-family:NR;font-weight:600;font-size:17px}}
.ttl{{position:absolute;left:96px;top:104px;display:flex;align-items:baseline;gap:22px}}
.ttl .n{{font-family:NR;font-weight:600;font-size:46px;color:{ORANGE};letter-spacing:-.02em}}
.ttl h2{{font-size:46px;font-weight:600;letter-spacing:-.02em}}
.desc{{position:absolute;left:96px;top:232px;width:390px;font-size:19px;line-height:1.55}}
.desc p{{opacity:.8;margin-bottom:16px}}
.desc .note{{opacity:1;font-weight:600;font-size:15px;margin-top:28px}}
.main{{position:absolute;left:600px;right:96px;top:232px;bottom:90px}}
.hl{{color:{ORANGE}}}
.num{{font-family:NR;font-weight:600;color:{ORANGE};letter-spacing:-.02em;font-variant-numeric:lining-nums}}
.lbl{{font-size:15px;font-weight:600;opacity:.6;margin-bottom:14px}}
.dark .lbl{{opacity:.7}}
p{{font-weight:400}}
img{{display:block}}
.grid{{display:grid;gap:32px}}
.card{{background:#fff}}
.card.navy{{background:{NAVY};color:#fff}}
"""


def header(section, n):
    return f'<div class="hdr"><span>{DOC}</span><span>{esc(section)}&nbsp;&nbsp;&nbsp;<span class="pn">{n:02d}</span></span></div>'


def content_page(n, section, num, title, desc, main, note=""):
    d = "".join(f"<p>{x}</p>" for x in desc)
    if note:
        d += f'<div class="note">{note}</div>'
    return f"""<section class="page">{header(section, n)}
<div class="ttl"><span class="n">{num}</span><h2>{title}</h2></div>
<div class="desc">{d}</div><div class="main">{main}</div></section>"""


PROPOSAL = "Đề xuất, chờ duyệt"


# ---------------------------------------------------------------- nội dung

def cover(a):
    return f"""<section class="page dark">
<div style="position:absolute;right:-260px;bottom:-330px;width:1300px">{img(a['mark-orange'], 'width:100%')}</div>
<div style="position:absolute;left:120px;top:110px">{img(a['logo-white'], 'height:150px')}</div>
<h1 style="position:absolute;left:120px;top:520px;font-size:120px;font-weight:600;letter-spacing:-.03em;line-height:1.02;width:900px">
Hướng dẫn <span class="hl">thương hiệu</span></h1>
<div style="position:absolute;left:120px;bottom:110px;font-size:24px;opacity:.75">Tháng 10, 2026</div></section>"""


def divider(a, num, title, items):
    rows = "".join(f'<div style="display:flex;gap:28px;align-items:baseline;margin-bottom:14px"><span class="num" style="font-size:24px;width:52px">{k}</span>'
                   f'<span style="font-size:24px;opacity:.85;width:520px">{esc(t)}</span><span class="num" style="font-size:24px">{p:02d}</span></div>'
                   for k, t, p in items)
    return f"""<section class="page dark">
<div style="position:absolute;right:-180px;bottom:-260px;width:1000px">{img(a['mark-orange'], 'width:100%')}</div>
<h2 style="position:absolute;left:120px;top:120px;font-size:84px;font-weight:600;letter-spacing:-.025em">{title}</h2>
<div style="position:absolute;left:120px;top:290px">{rows}</div>
<div class="num" style="position:absolute;left:112px;bottom:60px;font-size:260px;line-height:1">{num}</div></section>"""


def toc(a, sections):
    cols = []
    for num, title, items in sections:
        rows = "".join(f'<div style="display:flex;justify-content:space-between;font-size:21px;margin:10px 0"><span style="opacity:.85">{esc(t)}</span>'
                       f'<span class="num" style="font-size:21px">{p:02d}</span></div>' for _, t, p in items)
        cols.append(f'<div><div style="display:flex;gap:16px;align-items:baseline;margin-bottom:14px"><span class="num" style="font-size:30px">{num[0]}.</span>'
                    f'<span style="font-size:26px;font-weight:600">{esc(title)}</span></div>{rows}</div>')
    return f"""<section class="page">{header('Nội dung', 2)}
<div class="ttl"><h2>Nội dung</h2></div>
<div style="position:absolute;left:600px;right:96px;top:232px;display:grid;grid-template-columns:1fr 1fr;column-gap:120px;row-gap:56px">{''.join(cols)}</div></section>"""


def purpose(n):
    main = """<div style="font-size:76px;font-weight:600;letter-spacing:-.025em;line-height:1.12;margin-top:40px;width:1100px">
Đồng hành cùng doanh nghiệp Việt trong hành trình chuyển đổi số và <span class="hl">tăng trưởng</span> bền vững.</div>"""
    return content_page(n, "Thương hiệu Adtek", "1.1", "Mục đích thương hiệu",
                        ["Lý do Adtek được thành lập và giá trị Adtek mang lại cho khách hàng.",
                         "Câu sứ mệnh đang dùng trên website (trang chủ, Hỏi đáp)."], main)


def positioning(n):
    stats = [("2022", "Năm thành lập, tại TP. Hồ Chí Minh"), ("100+", "Khách hàng đã đồng hành"),
             ("200+", "Dự án đã triển khai"), ("10+", "Năm kinh nghiệm của đội ngũ")]
    st = "".join(f'<div><div class="num" style="font-size:84px;line-height:1">{v}</div><div style="font-size:21px;margin-top:10px;opacity:.85;width:230px">{t}</div></div>'
                 for v, t in stats)
    main = f"""<div class="lbl">Định vị</div>
<div style="font-size:92px;font-weight:600;letter-spacing:-.03em;line-height:1">Adtek</div>
<div style="font-size:64px;font-weight:600;letter-spacing:-.025em;margin-top:8px"><span class="hl">Growth</span> Marketing Agency</div>
<div style="font-size:30px;line-height:1.4;margin-top:28px;width:1050px;opacity:.85">Hỗ trợ khách hàng tăng trưởng vượt bậc thông qua chuyển đổi số và chiến lược dựa trên phân tích dữ liệu.</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:40px;margin-top:84px">{st}</div>"""
    return content_page(n, "Thương hiệu Adtek", "1.2", "Định vị thương hiệu",
                        ["Vị trí Adtek muốn có trong tâm trí khách hàng mục tiêu.",
                         "Câu định vị và các con số lấy từ trang chủ và trang Hỏi đáp. Cập nhật con số khi website cập nhật."], main)


def personality(n):
    traits = [("Dựa trên *dữ liệu*", "Mọi đề xuất bắt đầu từ số liệu và được đo bằng chỉ số kinh doanh: doanh thu, chi phí trên mỗi khách hàng, giá trị vòng đời khách hàng."),
              ("Đồng hành *đến cùng*", "Không chỉ xây chiến lược, Adtek trực tiếp triển khai như một phần mở rộng của đội ngũ khách hàng, chịu trách nhiệm ở từng giai đoạn."),
              ("*Thực chiến*", "Đội ngũ bước ra từ Vingroup, Lazada và Shopee. Adtek nói bằng kinh nghiệm làm nghề, ví dụ cụ thể và phép tính rõ ràng."),
              ("Đam mê *tăng trưởng*", "Adteker là những con người đam mê tăng trưởng: tò mò với dữ liệu, thử nhanh, học từ kết quả.")]
    cells = "".join(f'<div><div style="font-size:40px;font-weight:600;letter-spacing:-.02em;margin-bottom:16px">{hl(t)}</div>'
                    f'<p style="font-size:21px;line-height:1.5;opacity:.85">{esc(d)}</p></div>' for t, d in traits)
    main = f'<div class="grid" style="grid-template-columns:1fr 1fr;column-gap:96px;row-gap:72px;margin-top:20px">{cells}</div>'
    return content_page(n, "Thương hiệu Adtek", "1.3", "Tính cách thương hiệu",
                        ["Bốn đặc điểm khắc họa Adtek, thể hiện qua lời nói, chữ viết và hình ảnh.",
                         "Rút từ nội dung website: cách tiếp cận dựa trên dữ liệu, đồng hành từ chiến lược đến triển khai, đội ngũ và câu \"Adteker những con người đam mê tăng trưởng\"."],
                        main, PROPOSAL)


def slogan(n):
    opts = [("Tăng trưởng *đo được*.", "Nói đúng khác biệt so với agency truyền thống: kết quả đo bằng chỉ số kinh doanh."),
            ("Từ chiến lược đến *tăng trưởng*.", "Nhấn cách làm trọn gói: lập chiến lược và trực tiếp triển khai."),
            ("Đam mê *tăng trưởng*.", "Lấy từ câu đang dùng về đội ngũ, gần gũi, dễ nhớ.")]
    rows = "".join(f'<div style="display:flex;gap:28px;align-items:baseline;margin-bottom:30px"><span class="num" style="font-size:34px;width:40px">{i}</span>'
                   f'<div><div style="font-size:38px;font-weight:600;letter-spacing:-.02em">{hl(t)}</div>'
                   f'<p style="font-size:20px;opacity:.8;margin-top:6px">{esc(d)}</p></div></div>' for i, (t, d) in enumerate(opts, 1))
    main = f"""<div class="lbl">Đang dùng</div>
<div style="font-size:100px;font-weight:600;letter-spacing:-.03em;line-height:1"><span class="hl">Growth</span> Marketing Agency</div>
<div class="lbl" style="margin-top:96px">Khẩu hiệu tiếng Việt: {PROPOSAL.lower()}, chọn một</div>{rows}"""
    return content_page(n, "Ngôn ngữ thương hiệu", "2.1", "Khẩu hiệu thương hiệu",
                        ["Câu ngắn đi cùng logo, thể hiện định vị của Adtek.",
                         "\"Growth Marketing Agency\" đang dùng trên website, ảnh bìa Fanpage và ảnh chia sẻ. Adtek chưa có khẩu hiệu tiếng Việt; ba phương án bên cạnh để chọn."], main)


def story(n):
    paras = [
        "Adtek là growth marketing agency tại TP. Hồ Chí Minh, thành lập ngày 5/5/2022. Đội ngũ sáng lập bước ra từ các tập đoàn công nghệ và bán lẻ hàng đầu Việt Nam như Vingroup, Lazada và Shopee, với hơn 10 năm kinh nghiệm trong digital marketing và thương mại điện tử.",
        "Chúng tôi lập Adtek để đồng hành cùng doanh nghiệp Việt trong hành trình chuyển đổi số và tăng trưởng bền vững.",
        "Agency truyền thống thường tập trung vào từng chiến dịch hoặc từng kênh. Adtek nhìn vào toàn bộ bộ máy kinh doanh: thị trường, sản phẩm, kênh bán, vận hành và dữ liệu khách hàng, để tìm đòn bẩy tăng trưởng và đo kết quả bằng doanh thu, chi phí trên mỗi khách hàng và giá trị vòng đời khách hàng.",
        "Chúng tôi không chỉ xây chiến lược mà trực tiếp triển khai như một phần mở rộng của đội ngũ khách hàng: Brand Commerce, Lead Generation, Creative Strategy, SEO, App User Acquisition, vận hành sàn thương mại điện tử, truyền thông tích hợp (IMC), KOL/KOC và livestream, tư vấn tăng trưởng và CRM.",
        "Đến nay Adtek đã đồng hành cùng hơn 100 khách hàng với hơn 200 dự án trong các ngành bất động sản, thời trang, thương mại điện tử, mỹ phẩm, dược phẩm, giáo dục và điện tử.",
    ]
    body = "".join(f'<p style="font-size:21px;line-height:1.55;margin-bottom:22px;break-inside:avoid">{esc(p)}</p>' for p in paras)
    main = f"""<div style="columns:2;column-gap:72px;opacity:.9">{body}</div>
<div style="position:absolute;left:0;bottom:0;font-size:40px;font-weight:600;letter-spacing:-.02em">Adtek, <span class="hl">Growth</span> Marketing Agency.</div>"""
    return content_page(n, "Ngôn ngữ thương hiệu", "2.2", "Câu chuyện thương hiệu",
                        ["Câu chuyện Adtek kể với khách hàng, đối tác và ứng viên, gồm cả giá trị lý tính và cảm tính.",
                         "Mọi chi tiết lấy từ trang chủ và trang Hỏi đáp. Không thêm khách hàng, dự án hay số liệu chưa công bố."], main)


def messages(n):
    groups = [("Khách hàng", ["Tăng trưởng đo được bằng doanh thu, chi phí trên mỗi khách hàng và giá trị vòng đời.",
                              "Một đội ngũ chịu trách nhiệm từ chiến lược đến triển khai.",
                              "Kinh nghiệm thực chiến từ Vingroup, Lazada và Shopee."]),
              ("Cộng đồng marketer", ["Chia sẻ miễn phí blog kiến thức, từ điển thuật ngữ, thư viện báo cáo và bản đồ thương mại điện tử Việt Nam.",
                                      "Viết như người làm nghề chỉ việc: có số liệu, có nguồn, có ví dụ làm theo được."]),
              ("Đội ngũ và ứng viên", ["Adteker, những con người đam mê tăng trưởng.",
                                       "Adtek luôn tìm người yêu thích tăng trưởng và dữ liệu."]),
              ("Đối tác", ["Hợp tác dựa trên kết quả đo được và minh bạch số liệu.",
                           "Cùng khách hàng đi từ chiến lược đến triển khai trên nhiều kênh."])]
    cells = "".join(f'<div><div style="font-size:30px;font-weight:600;margin-bottom:18px">{g}</div>'
                    + "".join(f'<p style="font-size:20px;line-height:1.5;opacity:.85;margin-bottom:12px;padding-left:22px;text-indent:-22px">&bull;&nbsp;&nbsp;{esc(x)}</p>' for x in xs)
                    + "</div>" for g, xs in groups)
    main = f'<div class="grid" style="grid-template-columns:1fr 1fr;column-gap:96px;row-gap:60px">{cells}</div>'
    return content_page(n, "Ngôn ngữ thương hiệu", "2.3", "Thông điệp thương hiệu",
                        ["Thông điệp chính cho từng nhóm người Adtek giao tiếp.",
                         "Ba nhóm đầu rút từ website. Nhóm đối tác là đề xuất mới."], main, PROPOSAL)


def voice(n):
    do = ["Vào thẳng việc: nói rõ nội dung làm gì và không làm gì.",
          "Có quan điểm, nói rõ điều kiện: \"có khi..., không khi...\".",
          "Khái niệm đi kèm tên tiếng Anh và một phép tính nhỏ.",
          "Dẫn nguồn ngay trong câu, ghi tháng hoặc quý và năm.",
          "Câu ngắn, mỗi câu một ý, đoạn tối đa 3 đến 4 câu."]
    dont = ["Mở bằng bối cảnh chung chung: \"Trong thời đại số...\".",
            "Cụm sáo rỗng: chìa khóa thành công, giải pháp toàn diện, bứt phá, khẳng định vị thế.",
            "Bịa khách hàng, dự án hay số liệu của Adtek.",
            "Ký tự gạch dài, in đậm tràn lan, biểu tượng cảm xúc."]
    li = lambda xs: "".join(f'<p style="font-size:20px;line-height:1.45;margin-bottom:14px;opacity:.9">{esc(x)}</p>' for x in xs)  # noqa: E731
    main = f"""<div class="grid" style="grid-template-columns:1fr 1fr;column-gap:72px">
<div><div style="font-size:30px;font-weight:600;margin-bottom:22px">Nên</div>{li(do)}</div>
<div><div style="font-size:30px;font-weight:600;margin-bottom:22px">Không nên</div>{li(dont)}</div></div>
<div class="grid" style="grid-template-columns:1fr 1fr;column-gap:72px;margin-top:44px">
<div class="card" style="padding:32px"><div class="lbl">Ví dụ nên viết</div><p style="font-size:21px;line-height:1.5">Quý 2/2026, doanh thu quảng cáo Shopee tăng hơn 70%, GMV chỉ tăng 28.4% (Sea Limited). Sàn thu tiền quảng cáo nhanh gấp đôi tốc độ đơn hàng tăng.</p></div>
<div class="card" style="padding:32px"><div class="lbl">Ví dụ không nên viết</div><p style="font-size:21px;line-height:1.5;opacity:.75">Trong thời đại số, thương mại điện tử đang bùng nổ mạnh mẽ, đóng vai trò quan trọng và là chìa khóa thành công cho mọi doanh nghiệp.</p></div></div>"""
    return content_page(n, "Ngôn ngữ thương hiệu", "2.4", "Giọng văn",
                        ["Cách Adtek viết trên website, blog, mạng xã hội, báo cáo và email.",
                         "Tài liệu công ty xưng \"chúng tôi\"; bài blog xưng \"tôi\" theo tác giả. Quy tắc đầy đủ: content/editorial/van-phong.md."], main)


def logo_page(n, a):
    main = f"""<div class="grid" style="grid-template-columns:1.25fr 1fr;height:100%">
<div class="card" style="position:relative;display:flex;align-items:center;justify-content:center">
<div class="lbl" style="position:absolute;left:36px;top:30px">Logo chính</div>{img(a['logo-color'], 'height:360px')}</div>
<div class="grid" style="grid-template-rows:1fr 1fr">
<div class="card navy" style="display:flex;align-items:center;justify-content:center">{img(a['logo-white'], 'height:190px')}</div>
<div class="card" style="display:flex;align-items:center;justify-content:center;gap:56px">{img(a['mark-color'], 'height:150px')}
<div style="font-size:18px;line-height:1.45;width:250px;opacity:.85"><b style="font-weight:600">Biểu tượng chữ A</b><br>Dùng riêng khi chỗ quá nhỏ cho logo đầy đủ: ảnh đại diện, favicon, họa tiết.</div></div></div></div>"""
    return content_page(n, "Nhận diện thương hiệu", "3.1", "Logo thương hiệu",
                        ["Logo Adtek gồm biểu tượng chữ A màu chuyển và chữ ADTEK, xếp theo chiều dọc.",
                         "Logo được thiết kế riêng cho Adtek. Không vẽ lại, sửa đổi hay sắp xếp lại các thành phần.",
                         "Adtek hiện chỉ có phiên bản dọc. Khi cần phiên bản ngang, thiết kế và duyệt riêng, không tự ghép."], main)


def clearspace(n, a):
    lh = 300
    x = round(lh * 76 / 371)  # x = chiều cao chữ ADTEK trong logo
    lw = round(lh * 440 / 371)
    box = f"""<div style="position:relative;width:{lw + 2 * x}px;height:{lh + 2 * x}px;background:rgba(255,144,20,.18)">
<div style="position:absolute;left:{x}px;top:{x}px;background:{CREAM}">{img(a['logo-color'], f'height:{lh}px')}</div>
<div style="position:absolute;left:0;top:0;width:{x}px;height:{x}px;display:flex;align-items:center;justify-content:center;font-family:NR;font-weight:600;font-size:26px;color:{ORANGE}">x</div>
<div style="position:absolute;right:0;bottom:0;width:{x}px;height:{x}px;display:flex;align-items:center;justify-content:center;font-family:NR;font-weight:600;font-size:26px;color:{ORANGE}">x</div></div>"""
    sizes = [("Logo đầy đủ, in ấn", "20mm", "chiều rộng"), ("Logo đầy đủ, màn hình", "80px", "chiều rộng"),
             ("Biểu tượng chữ A", "24px", "chiều rộng, favicon và ảnh đại diện nhỏ")]
    rows = "".join(f'<div style="display:flex;gap:28px;align-items:center;margin-bottom:34px"><div style="width:180px"><span class="num" style="font-size:56px">{v}</span></div>'
                   f'<div><div style="font-size:22px;font-weight:600">{t}</div><div style="font-size:18px;opacity:.75;margin-top:4px">{s}</div></div></div>'
                   for t, v, s in sizes)
    main = f"""<div class="grid" style="grid-template-columns:auto 1fr;column-gap:110px;align-items:start">
<div><div class="lbl">Vùng an toàn</div>{box}<p style="font-size:18px;opacity:.8;margin-top:22px;width:{lw + 2 * x}px">x bằng chiều cao chữ ADTEK. Không đặt chữ, hình hay mép giấy trong vùng tô màu.</p></div>
<div><div class="lbl">Kích thước tối thiểu</div>{rows}</div></div>"""
    return content_page(n, "Nhận diện thương hiệu", "3.2", "Vùng an toàn và kích thước tối thiểu",
                        ["Khoảng trống quanh logo giúp logo dễ nhận ra và không bị chen lấn.",
                         "Không dùng logo nhỏ hơn kích thước tối thiểu trên ấn phẩm in hoặc màn hình."], main)


def on_colors(n, a):
    tiles = [(CREAM, a["logo-color"], "Nền kem, logo màu"), ("#ffffff", a["logo-color"], "Nền trắng, logo màu"),
             (NAVY, a["logo-white"], "Nền navy, logo trắng"), (CREAM, a["logo-navy"], "Nền kem, logo navy một màu"),
             ("#ffffff", a["logo-ink"], "Đen trắng: logo màu mực"), (INK, a["logo-white"], "Đen trắng: logo trắng trên nền mực")]
    cells = "".join(f'<div><div style="background:{bg};height:250px;display:flex;align-items:center;justify-content:center{";outline:1px solid rgba(0,45,114,.12);outline-offset:-1px" if bg == "#ffffff" else ""}">{img(u, "height:140px")}</div>'
                    f'<div style="font-size:18px;margin-top:12px;opacity:.85">{t}</div></div>' for bg, u, t in tiles)
    main = f'<div class="grid" style="grid-template-columns:repeat(3,1fr);column-gap:32px;row-gap:40px">{cells}</div>'
    return content_page(n, "Nhận diện thương hiệu", "3.3", "Logo trên nền màu",
                        ["Ưu tiên logo màu trên nền kem hoặc trắng. Trên nền navy hay nền tối, dùng logo trắng.",
                         "Bản một màu (navy, mực, trắng) dùng khi in một màu, khắc, dập nổi hoặc nền không cho phép logo màu.",
                         "Không đặt logo trên nền cam (xem 3.4)."], main)


def misuse(n, a):
    L = a["logo-color"]
    ex = [(img(a["logo-orange"], "height:120px"), "Không đổi màu logo"),
          (img(L, "height:120px;filter:drop-shadow(0 6px 10px rgba(0,0,0,.45))"), "Không thêm bóng đổ, hiệu ứng"),
          (img(L, "height:120px;width:230px"), "Không bóp méo tỉ lệ"),
          (img(L, "height:120px;transform:rotate(-14deg)"), "Không xoay logo"),
          (f'<div style="display:flex;align-items:center;gap:14px">{img(a["mark-color"], "height:80px")}{img(a["wordmark"], "height:30px")}</div>', "Không tự sắp xếp lại thành phần"),
          (f'<div style="text-align:center">{img(a["mark-color"], "height:84px;margin:0 auto")}<div style="font-family:Arial;font-weight:700;font-size:32px;letter-spacing:.08em;color:{INK};margin-top:4px">ADTEK</div></div>', "Không thay phông chữ ADTEK"),
          (f'<div style="width:150px;height:84px;overflow:hidden">{img(L, "height:120px")}</div>', "Không cắt bớt logo"),
          (f'<div style="background:{ORANGE};padding:24px 34px">{img(a["logo-white"], "height:92px")}</div>', "Không đặt logo trên nền cam"),
          (f'<div style="border:3px solid {NAVY};border-radius:50%;padding:22px">{img(L, "height:86px")}</div>', "Không thêm viền, khung tròn")]
    cells = "".join(f'<div><div class="card" style="height:210px;display:flex;align-items:center;justify-content:center;overflow:hidden">{h}</div>'
                    f'<div style="font-size:18px;margin-top:12px"><span style="color:{ORANGE};font-weight:700">&times;</span>&nbsp;&nbsp;{t}</div></div>' for h, t in ex)
    main = f'<div class="grid" style="grid-template-columns:repeat(3,1fr);column-gap:32px;row-gap:30px">{cells}</div>'
    return content_page(n, "Nhận diện thương hiệu", "3.4", "Trường hợp sử dụng sai",
                        ["Giữ nguyên vẹn logo trong mọi trường hợp. Không làm sai lệch hay thay đổi bất kỳ thành phần nào.",
                         "Khi không chắc cách dùng, dùng logo màu trên nền kem hoặc logo trắng trên nền navy."], main)


def cmyk(hexv):
    r, g, b = (int(hexv[i:i + 2], 16) / 255 for i in (1, 3, 5))
    k = 1 - max(r, g, b)
    if k >= 1:
        return 0, 0, 0, 100
    return tuple(round(v * 100) for v in ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k))


def rgb(hexv):
    return ", ".join(str(int(hexv[i:i + 2], 16)) for i in (1, 3, 5))


def palette(n):
    def spec(name, hexv, h, role, swatch=None):
        c = cmyk(hexv)
        edge = ";outline:1px solid rgba(0,45,114,.14);outline-offset:-1px" if hexv.lower() in ("#ffffff", CREAM.lower()) else ""
        return f"""<div><div style="height:{h}px;background:{swatch or hexv}{edge}"></div>
<div style="font-size:28px;font-weight:600;margin-top:18px">{name}</div><div style="font-size:17px;opacity:.75;margin-top:4px">{role}</div>
<div style="font-size:16px;line-height:1.6;margin-top:10px;opacity:.9">HEX {hexv.upper()}<br>RGB {rgb(hexv)}<br>CMYK {c[0]} {c[1]} {c[2]} {c[3]}</div></div>"""
    grad = f"linear-gradient(115deg,{GRAD[0]},{GRAD[1]} 55%,{GRAD[2]})"
    main = f"""<div class="lbl">Màu chính</div><div class="grid" style="grid-template-columns:1.5fr 1fr 1fr;column-gap:28px">
{spec("Navy", NAVY, 250, "Màu chủ đạo: nền, chữ")}{spec("Cam", ORANGE, 250, "Nhấn: con số, từ khóa, mảng không chữ")}{spec("Kem", CREAM, 250, "Nền sáng, thay cho trắng")}</div>
<div class="lbl" style="margin-top:40px">Màu phụ</div><div class="grid" style="grid-template-columns:1fr 1fr 1.3fr;column-gap:28px">
{spec("Trắng", "#ffffff", 60, "Chữ trên nền navy, giấy in")}{spec("Mực", INK, 60, "Màu chữ ADTEK trong logo")}
<div><div style="height:60px;background:{grad}"></div><div style="font-size:28px;font-weight:600;margin-top:18px">Màu chuyển của logo</div>
<div style="font-size:17px;opacity:.75;margin-top:4px">Chỉ dùng trong logo, không dùng cho nền hay chữ</div>
<div style="font-size:16px;line-height:1.6;margin-top:10px;opacity:.9">{GRAD[0]} &rarr; {GRAD[1]} &rarr; {GRAD[2]}</div></div></div>"""
    return content_page(n, "Thành tố thương hiệu", "4.1", "Bảng màu",
                        ["Ba màu chính: navy, cam, kem. Tỉ lệ gợi ý trên một thiết kế: navy và kem khoảng 90%, cam khoảng 10%.",
                         "Cam chỉ dùng cho con số, từ khóa tô màu và mảng hình không có chữ. Không đặt chữ trên nền cam.",
                         "Mã CMYK quy đổi tham khảo, cần in thử để chốt."], main)


def type_brand(n):
    sample = "Aa Ăă Ââ Đđ Êê Ôô Ơơ Ưư Ạạ Ấấ Ầầ Ẩẩ Ẫẫ Ậậ Ếế Ềề Ểể Ễễ Ệệ"
    main = f"""<div class="grid" style="grid-template-columns:1.2fr 1fr;column-gap:80px">
<div><div class="lbl">Tiêu đề và nội dung</div>
<div style="font-size:96px;font-weight:600;letter-spacing:-.03em;line-height:1">Inter Tight</div>
<div style="font-size:30px;line-height:1.35;margin-top:24px">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>0123456789</div>
<div style="font-size:22px;margin-top:18px;opacity:.85">{sample}</div>
<div style="display:grid;grid-template-columns:auto 1fr;column-gap:36px;row-gap:12px;margin-top:34px;font-size:22px;align-items:baseline">
<span style="font-weight:600">SemiBold 600</span><span style="opacity:.8">Tiêu đề, nhãn, logo chữ phụ</span>
<span style="font-weight:500">Medium 500</span><span style="opacity:.8">Danh sách, nhãn phụ</span>
<span style="font-weight:400">Regular 400</span><span style="opacity:.8">Nội dung, mô tả</span></div></div>
<div><div class="lbl">Con số và cụm chữ đi liền sau số</div>
<div style="font-family:NR;font-weight:600;font-size:96px;letter-spacing:-.02em;line-height:1">Newsreader</div>
<div style="display:flex;gap:20px;align-items:baseline;margin-top:40px"><span class="num" style="font-size:150px;line-height:.9">30</span>
<span style="font-family:NR;font-weight:600;font-size:36px;line-height:1.1">ngày chuẩn bị<br>cho 11.11</span></div>
<p style="font-size:20px;line-height:1.5;opacity:.8;margin-top:30px">Newsreader SemiBold 600, chữ có chân, chỉ dùng cho con số lớn và cụm chữ đọc liền sau số. Số đứng bên trái hoặc phía trên, sát cụm chữ.</p></div></div>"""
    return content_page(n, "Thành tố thương hiệu", "4.2", "Phông chữ thương hiệu",
                        ["Hai phông chữ cho mọi thiết kế của Adtek: ảnh bìa blog, ảnh mạng xã hội, báo cáo, website.",
                         "Cả hai là phông mã nguồn mở (SIL Open Font License), hỗ trợ đầy đủ tiếng Việt."], main)


def type_system(n):
    main = f"""<div class="grid" style="grid-template-columns:1.2fr 1fr;column-gap:80px">
<div><div class="lbl">Phông hệ thống</div>
<div style="font-family:BVP;font-size:96px;font-weight:600;letter-spacing:-.02em;line-height:1">Be Vietnam Pro</div>
<div style="font-family:BVP;font-size:30px;line-height:1.35;margin-top:24px">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>0123456789</div>
<div style="font-family:BVP;display:grid;grid-template-columns:auto 1fr;column-gap:36px;row-gap:12px;margin-top:34px;font-size:22px">
<span style="font-weight:700">Bold 700</span><span style="opacity:.8">Tiêu đề slide, tiêu đề văn bản</span>
<span style="font-weight:500">Medium 500</span><span style="opacity:.8">Nhãn, bảng</span>
<span style="font-weight:400">Regular 400</span><span style="opacity:.8">Nội dung</span></div></div>
<div><div class="lbl">Phông thay thế</div>
<div style="font-family:Arial;font-size:96px;font-weight:700;line-height:1">Arial</div>
<p style="font-size:20px;line-height:1.5;opacity:.85;margin-top:30px">Dùng khi máy hoặc phần mềm không có Be Vietnam Pro, ví dụ email gửi khách, tệp chia sẻ cho đối tác.</p></div></div>"""
    return content_page(n, "Thành tố thương hiệu", "4.3", "Phông chữ hệ thống",
                        ["Phông cho tài liệu soạn trên phần mềm văn phòng: slide đề xuất, Word, Google Docs, chữ ký email.",
                         "Be Vietnam Pro miễn phí trên Google Fonts, cài một lần trên máy là dùng được."], main)


def type_rules(n):
    rules = [("Viết thường như câu", "Chỉ viết hoa chữ đầu câu và tên riêng. Không dùng tiêu đề in hoa giãn khoảng."),
             ("Một từ khóa màu cam", "Mỗi tiêu đề tô cam đúng một từ hoặc cụm từ khóa."),
             ("Số đứng trước chữ", "Con số lớn đứng bên trái hoặc phía trên, sát cụm chữ giải thích nó."),
             ("Nhãn nhỏ cùng màu chữ", "Nhãn, chú thích dùng màu chữ xung quanh, mờ hơn; không tô cam."),
             ("Không chữ trên nền cam", "Trên nền cam chữ khó đọc; chữ đặt trên navy, kem hoặc trắng.")]
    rows = "".join(f'<div style="margin-bottom:24px"><div style="font-size:24px;font-weight:600">{t}</div><p style="font-size:19px;opacity:.8;margin-top:4px">{d}</p></div>' for t, d in rules)
    sample = f"""<div style="background:{NAVY};color:#fff;padding:56px;height:100%">
<div style="font-size:20px;font-weight:600;opacity:.75">Mega sale 2026</div>
<div style="font-size:64px;font-weight:600;letter-spacing:-.025em;line-height:1.08;margin-top:14px">Kế hoạch <span class="hl">11.11</span> cho nhà bán trên sàn</div>
<div style="display:flex;gap:18px;align-items:baseline;margin-top:44px"><span class="num" style="font-size:120px;line-height:.9">30</span>
<span style="font-family:NR;font-weight:600;font-size:34px;line-height:1.1">ngày chuẩn bị<br>trước ngày sale</span></div>
<p style="font-size:22px;line-height:1.5;opacity:.85;margin-top:38px;width:620px">Tính giá hòa vốn sau phí sàn, chọn sản phẩm chủ lực và lên lịch livestream.</p></div>"""
    main = f'<div class="grid" style="grid-template-columns:1fr 1.15fr;column-gap:72px;height:100%"><div>{rows}</div>{sample}</div>'
    return content_page(n, "Thành tố thương hiệu", "4.4", "Quy tắc chữ",
                        ["Cách sắp xếp chữ để mọi thiết kế của Adtek đọc nhanh và giống nhau.",
                         "Ví dụ bên phải: nhãn, tiêu đề có một từ khóa cam, con số sát cụm chữ, mô tả."], main)


def devices(n, a):
    hs = [36, 50, 68, 92, 124, 168, 232, 316]
    bars = "".join(f'<div style="position:absolute;bottom:0;left:{12 + 46 * i}px;width:34px;height:{h * .62:.0f}px;background:{ORANGE if i >= 5 else "rgba(244,238,227,.14)"}"></div>' for i, h in enumerate(hs))
    pattern = "".join(f'<div style="position:absolute;left:{x}px;top:{y}px">{img(a["mark-orange"] if (x, y) == (290, 150) else a["mark-white"], "height:40px;opacity:" + ("1" if (x, y) == (290, 150) else ".09"))}</div>'
                      for y in range(10, 330, 70) for x in range(10 + (0 if y % 140 == 10 else 35), 540, 70))
    tiles = [(f'<div style="position:absolute;right:-90px;bottom:-110px">{img(a["mark-orange"], "height:330px")}</div>', NAVY, "Chữ A cỡ lớn",
              "Dấu A cam tràn mép, cắt bớt. Dùng cho ảnh bìa, trang ngăn cách, slide mở đầu."),
             (bars, NAVY, "Cột tăng trưởng", "Các cột cao dần, cột cuối chuyển cam. Gợi ý tăng trưởng, dùng cho ảnh bìa và báo cáo."),
             (f'<div style="position:absolute;left:44px;top:44px;bottom:44px;width:42%;background:{CREAM};display:flex;align-items:center;justify-content:center"><span class="num" style="font-size:120px">8</span></div><div style="position:absolute;left:52%;top:70px;color:#fff;font-size:30px;font-weight:600;line-height:1.15;width:220px">điểm rà tài khoản Meta Ads</div>',
              NAVY, "Hai khối kem và navy", "Chia đôi nền, con số cam trên khối kem. Dùng cho bài có số liệu nổi bật."),
             (pattern, NAVY, "Lưới chữ A", "Dấu A chìm lặp lại, một dấu A cam nổi bật. Dùng làm nền phụ, không đặt chữ đè lên.")]
    cells = "".join(f'<div><div style="position:relative;height:290px;background:{bg};overflow:hidden">{h}</div>'
                    f'<div style="font-size:24px;font-weight:600;margin-top:16px">{t}</div><p style="font-size:18px;opacity:.8;margin-top:4px">{d}</p></div>'
                    for h, bg, t, d in tiles)
    main = f'<div class="grid" style="grid-template-columns:1fr 1fr;column-gap:40px;row-gap:24px;margin-top:-30px">{cells}</div>'
    return content_page(n, "Thành tố thương hiệu", "4.5", "Thiết bị đồ họa",
                        ["Các hình đồ họa riêng của Adtek, dựng từ dấu A và bảng màu.",
                         "Chỉ dùng hình phẳng: mảng màu đặc, không màu chuyển, không bóng, không viền."], main)


def style_rules(n, a):
    good = [file_uri("content/posts/meta-andromeda-cover.jpg"), file_uri("content/posts/ke-hoach-11-11-cover.jpg")]
    bad = [(f'<div style="height:100%;background:linear-gradient(135deg,#6a11cb,#2575fc);display:flex;align-items:center;justify-content:center"><span style="color:#fff;font-size:26px;font-weight:700;text-shadow:0 0 18px #fff;text-align:center">MÀU CHUYỂN,<br>QUẦNG SÁNG</span></div>', "Màu chuyển, quầng sáng, chữ in hoa"),
           (f'<div style="height:100%;background:{NAVY};display:flex;align-items:center;justify-content:center"><div style="border:4px solid {ORANGE};border-radius:50%;width:200px;height:200px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:28px;font-weight:600">Vòng tròn</div></div>', "Hình tròn bao quanh chữ hoặc logo"),
           (f'<div style="height:100%;background:{ORANGE};display:flex;align-items:center;justify-content:center;padding:30px"><span style="color:{NAVY};font-size:36px;font-weight:600">Chữ trên nền cam</span></div>', "Chữ đặt trên nền cam"),
           (f'<div style="height:100%;background:#fff;display:flex;align-items:center;justify-content:center"><span style="color:{NAVY};font-size:36px;font-weight:600;text-decoration:underline;text-decoration-color:{ORANGE};text-decoration-thickness:5px;text-underline-offset:10px">Gạch chân nhấn</span></div>', "Đường kẻ, gạch chân, nền trắng")]
    g = "".join(f'<div style="height:262px;outline:1px solid rgba(0,45,114,.14);outline-offset:-1px">{img(u, "width:100%;height:100%;object-fit:cover")}</div>' for u in good)
    b = "".join(f'<div><div style="height:180px;overflow:hidden">{h}</div><div style="font-size:17px;margin-top:10px"><span style="color:{ORANGE};font-weight:700">&times;</span>&nbsp;&nbsp;{t}</div></div>' for h, t in bad)
    main = f"""<div class="lbl">Nên: phẳng, ít màu, chữ rõ</div><div class="grid" style="grid-template-columns:1fr 1fr;column-gap:32px">{g}</div>
<div class="lbl" style="margin-top:36px">Không nên</div><div class="grid" style="grid-template-columns:repeat(4,1fr);column-gap:24px">{b}</div>"""
    return content_page(n, "Thành tố thương hiệu", "4.6", "Phong cách thiết kế",
                        ["Thiết kế phẳng, chỉ dùng màu thương hiệu, để nội dung là phần nổi bật nhất và không giống ảnh tạo bằng AI.",
                         "Ngoại lệ duy nhất: ảnh bìa Fanpage giữ phong cách mẫu cũ (màu chuyển) theo quyết định ngày 16/10/2026."], main)


def business_card(n, a):
    w, h = 630, 360
    front = f'<div style="width:{w}px;height:{h}px;background:{NAVY};position:relative;overflow:hidden"><div style="position:absolute;right:-70px;bottom:-110px">{img(a["mark-orange"], "height:330px")}</div><div style="position:absolute;left:56px;top:56px">{img(a["logo-white"], "height:96px")}</div><div style="position:absolute;left:56px;bottom:46px;color:#fff;font-size:17px;opacity:.75">adtek.agency</div></div>'
    back = f"""<div style="width:{w}px;height:{h}px;background:{CREAM};position:relative;padding:56px;outline:1px solid rgba(0,45,114,.14);outline-offset:-1px">
<div style="font-size:34px;font-weight:600;letter-spacing:-.02em">Họ và tên</div><div style="font-size:19px;opacity:.75;margin-top:6px">Chức danh</div>
<div style="position:absolute;left:56px;bottom:50px;font-size:17px;line-height:1.65">+84 9323 494 34<br>ten@adtek.agency<br>123/30B Nguyễn Hoàng, phường Bình Trưng, TP. Hồ Chí Minh</div>
<div style="position:absolute;right:56px;top:56px">{img(a["mark-color"], "height:56px")}</div></div>"""
    main = f"""<div class="grid" style="grid-template-columns:auto auto;column-gap:48px;justify-content:start;margin-top:40px">
<div><div class="lbl">Mặt trước</div>{front}</div><div><div class="lbl">Mặt sau</div>{back}</div></div>
<p style="font-size:19px;opacity:.8;margin-top:40px">Khổ 90 x 55 mm. Mặt trước in navy và cam, mặt sau in nền kem. Chữ Inter Tight.</p>"""
    return content_page(n, "Ứng dụng thương hiệu", "5.1", "Danh thiếp",
                        ["Mặt trước nhận diện thương hiệu, mặt sau thông tin cá nhân.",
                         "Thông tin liên hệ chung lấy từ website; tên, chức danh, email thay theo từng người."], main)


def letterhead(n, a):
    lines = "".join(f'<div style="height:9px;background:rgba(0,45,114,.12);margin-bottom:13px;width:{w}%"></div>' for w in (100, 96, 100, 88, 100, 92, 60))
    lines2 = "".join(f'<div style="height:9px;background:rgba(0,45,114,.12);margin-bottom:13px;width:{w}%"></div>' for w in (100, 94, 100, 70))
    page = f"""<div style="width:520px;height:735px;background:#fff;position:relative;padding:58px 54px;outline:1px solid rgba(0,45,114,.12);outline-offset:-1px">
<div style="display:flex;justify-content:space-between;align-items:flex-start">{img(a["logo-color"], "height:70px")}<div style="text-align:right;font-size:11px;line-height:1.6;opacity:.75">adtek.agency<br>contact@adtek.agency<br>+84 9323 494 34</div></div>
<div style="margin-top:70px;font-size:13px;opacity:.7">TP. Hồ Chí Minh, ngày ... tháng ... năm 2026</div>
<div style="margin-top:26px;font-size:15px;font-weight:600">Kính gửi Quý khách hàng</div>
<div style="margin-top:22px">{lines}</div><div style="margin-top:20px">{lines2}</div>
<div style="position:absolute;left:54px;right:54px;bottom:40px;display:flex;justify-content:space-between;font-size:10px;opacity:.7">
<span>Adtek, 123/30B Nguyễn Hoàng, phường Bình Trưng, TP. Hồ Chí Minh</span><span>adtek.agency</span></div></div>"""
    env = f'<div style="width:560px;height:270px;background:#fff;position:relative;outline:1px solid rgba(0,45,114,.12);outline-offset:-1px"><div style="position:absolute;left:40px;top:36px">{img(a["logo-color"], "height:64px")}</div><div style="position:absolute;left:40px;bottom:32px;font-size:12px;opacity:.75;line-height:1.6">123/30B Nguyễn Hoàng, phường Bình Trưng, TP. Hồ Chí Minh<br>adtek.agency</div></div>'
    main = f"""<div class="grid" style="grid-template-columns:auto auto;column-gap:56px;justify-content:start">
<div><div class="lbl">Tiêu đề thư A4</div>{page}</div><div><div class="lbl">Phong bì DL</div>{env}
<p style="font-size:19px;opacity:.8;margin-top:28px;width:560px">In trên giấy trắng. Logo màu góc trên bên trái, thông tin liên hệ góc trên bên phải và chân trang. Nội dung Be Vietnam Pro hoặc Arial 11 đến 12pt.</p></div></div>"""
    return content_page(n, "Ứng dụng thương hiệu", "5.2", "Tiêu đề thư",
                        ["Mẫu giấy tiêu đề cho thư, báo giá và văn bản gửi khách hàng, đối tác.",
                         "Tên pháp nhân và mã số thuế bổ sung theo giấy phép kinh doanh."], main)


def slides(n, a):
    w, h = 600, 338
    s1 = f"""<div style="width:{w}px;height:{h}px;background:{NAVY};position:relative;overflow:hidden;font-family:BVP;color:#fff">
<div style="position:absolute;right:-60px;bottom:-90px">{img(a["mark-orange"], "height:300px")}</div><div style="position:absolute;left:36px;top:32px">{img(a["logo-white"], "height:46px")}</div>
<div style="position:absolute;left:36px;top:130px;font-size:30px;font-weight:700;line-height:1.15;width:380px">Đề xuất chiến lược <span class="hl">tăng trưởng</span> 2027</div>
<div style="position:absolute;left:36px;bottom:30px;font-size:12px;opacity:.75">Tên khách hàng · Tháng 10, 2026</div></div>"""
    bars = "".join(f'<div style="width:38px;height:{v}px;background:{ORANGE if i == 4 else NAVY}"></div>' for i, v in enumerate((50, 70, 84, 110, 150)))
    s2 = f"""<div style="width:{w}px;height:{h}px;background:{CREAM};position:relative;font-family:BVP;color:{NAVY};outline:1px solid rgba(0,45,114,.14);outline-offset:-1px">
<div style="position:absolute;left:32px;top:26px;right:32px;font-size:19px;font-weight:700;line-height:1.25">Doanh thu online tăng nhanh hơn chi phí quảng cáo khi tối ưu trang đích</div>
<div style="position:absolute;left:32px;bottom:40px;display:flex;gap:16px;align-items:flex-end">{bars}</div>
<div style="position:absolute;left:330px;top:120px;width:236px;font-size:12px;line-height:1.5;opacity:.85">Tiêu đề là một câu kết luận. Biểu đồ thay cho bảng. Số liệu minh họa.</div>
<div style="position:absolute;right:24px;bottom:18px">{img(a["logo-color"], "height:30px")}</div></div>"""
    main = f"""<div class="grid" style="grid-template-columns:auto auto;column-gap:40px;justify-content:start;margin-top:30px">
<div><div class="lbl">Slide mở đầu</div>{s1}</div><div><div class="lbl">Slide nội dung</div>{s2}</div></div>
<div class="grid" style="grid-template-columns:repeat(3,1fr);column-gap:40px;margin-top:56px;font-size:19px;line-height:1.5">
<div><b style="font-weight:600">Khổ 16:9</b><p style="opacity:.8">Nền kem cho trang nội dung, navy cho trang mở đầu và trang ngăn cách.</p></div>
<div><b style="font-weight:600">Tiêu đề hành động</b><p style="opacity:.8">Mỗi slide có tiêu đề là một câu kết luận, đọc riêng tiêu đề vẫn hiểu câu chuyện.</p></div>
<div><b style="font-weight:600">Logo góc phải dưới</b><p style="opacity:.8">Logo màu nhỏ góc phải dưới trang nội dung; phông Be Vietnam Pro.</p></div></div>"""
    return content_page(n, "Ứng dụng thương hiệu", "5.3", "Trang mẫu trình bày",
                        ["Mẫu slide cho đề xuất, báo cáo kết quả và thuyết trình với khách hàng.",
                         "Bộ mẫu đầy đủ theo chuẩn deck đề xuất của Adtek."], main)


def signature(n, a):
    sig = f"""<div style="background:#fff;width:980px;padding:44px 52px;outline:1px solid rgba(0,45,114,.12);outline-offset:-1px;font-family:Arial,sans-serif">
<div style="font-size:15px;color:#555;line-height:1.7">Chào anh/chị,<br>Adtek gửi anh/chị đề xuất chiến lược như đã trao đổi. Anh/chị xem giúp và phản hồi trước thứ Sáu.<br>Trân trọng,</div>
<div style="display:flex;gap:28px;align-items:center;margin-top:34px">{img(a["logo-color"], "height:92px")}
<div style="font-size:14px;line-height:1.6;color:{NAVY}"><div style="font-size:18px;font-weight:700">Họ và tên</div><div style="opacity:.75">Chức danh · Adtek</div>
<div style="margin-top:6px">+84 9323 494 34 · ten@adtek.agency</div><div><span style="color:{NAVY};font-weight:700">adtek.agency</span> · 123/30B Nguyễn Hoàng, phường Bình Trưng, TP. Hồ Chí Minh</div></div></div></div>"""
    main = f"""<div style="margin-top:20px">{sig}</div>
<div class="grid" style="grid-template-columns:repeat(3,1fr);column-gap:40px;margin-top:56px;font-size:19px;line-height:1.5">
<div><b style="font-weight:600">Phông Arial</b><p style="opacity:.8">Email hiển thị đúng trên mọi máy; tên Arial Bold 14 đến 18px.</p></div>
<div><b style="font-weight:600">Logo màu cao 80 đến 100px</b><p style="opacity:.8">Ảnh PNG nền trong suốt, có liên kết về adtek.agency.</p></div>
<div><b style="font-weight:600">Không thêm</b><p style="opacity:.8">Câu trích dẫn, biểu tượng cảm xúc, ảnh động, màu chữ khác navy.</p></div></div>"""
    return content_page(n, "Ứng dụng thương hiệu", "5.4", "Chữ ký email",
                        ["Chữ ký thống nhất cho mọi email gửi khách hàng, đối tác và ứng viên.",
                         "Email chung: contact@adtek.agency. Giờ làm việc thứ Hai đến thứ Sáu, 9:00 đến 18:00."], main)


def social(n, a):
    fb = ["ke-hoach-11-11", "meta-andromeda", "tiktok-shop-vs-shopee", "luat-bao-ve-du-lieu-ca-nhan-marketing", "chi-so-growth-marketing", "luat-thuong-mai-dien-tu-livestream"]
    grid = "".join(img(file_uri(f"content/posts/{s}-fb.jpg"), "width:100%;outline:1px solid rgba(0,45,114,.14);outline-offset:-1px") for s in fb)
    main = f"""<div class="grid" style="grid-template-columns:1fr 1.5fr;column-gap:48px">
<div><div class="lbl">Bài đăng Facebook 1:1</div><div class="grid" style="grid-template-columns:repeat(3,1fr);gap:12px">{grid}</div></div>
<div><div class="lbl">Ảnh bìa Fanpage</div>{img(file_uri("content/brand/fb-cover.jpg"), "width:100%")}
<div style="display:flex;gap:28px;align-items:center;margin-top:28px"><div style="flex:none;width:120px;height:120px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden">{img(a["logo-color"], "height:84px")}</div>
<p style="font-size:19px;line-height:1.5;opacity:.85">Ảnh đại diện: logo màu trên nền trắng. Ảnh bìa 1640 x 624, chữ trong vùng giữa vì điện thoại cắt hai bên và ảnh đại diện che phía dưới.</p></div></div></div>
<p style="font-size:19px;opacity:.8;margin-top:30px;width:1100px">Mỗi bài một phong cách, tự chọn theo nội dung và không lặp bài liền trước. Ảnh dựng tự động bằng tools/covers.py và tools/social.py.</p>"""
    return content_page(n, "Ứng dụng thương hiệu", "5.5", "Mạng xã hội",
                        ["Ảnh bài đăng, ảnh bìa và ảnh đại diện trên Facebook.",
                         "Bài đăng theo bộ quy tắc phẳng; ảnh bìa Fanpage là ngoại lệ giữ phong cách mẫu cũ."], main)


def web(n, a):
    covers = ["tiktok-shop-vs-shopee", "luat-bao-ve-du-lieu-ca-nhan-marketing", "chi-so-growth-marketing", "luat-thuong-mai-dien-tu-livestream"]
    g = "".join(img(file_uri(f"content/posts/{s}-cover.jpg"), "width:100%;outline:1px solid rgba(0,45,114,.14);outline-offset:-1px") for s in covers)
    main = f"""<div class="grid" style="grid-template-columns:1.6fr 1fr;column-gap:48px">
<div><div class="lbl">Ảnh bìa bài blog, 1200 x 630 (xuất 2400 x 1260)</div><div class="grid" style="grid-template-columns:1fr 1fr;gap:16px">{g}</div></div>
<div><div class="lbl">Ảnh chia sẻ mặc định của website</div>{img(file_uri("content/brand/og-default.jpg"), "width:100%")}
<p style="font-size:19px;line-height:1.5;opacity:.85;margin-top:24px">Hiện khi chia sẻ trang chủ và các trang không có ảnh đại diện lên Facebook, Zalo, LinkedIn.</p>
<p style="font-size:19px;line-height:1.5;opacity:.85;margin-top:16px">Chữ và logo ảnh bìa blog nằm trong vùng x 140 đến 1060, y 70 đến 560 vì website cắt ảnh ở trang danh sách.</p></div></div>"""
    return content_page(n, "Ứng dụng thương hiệu", "5.6", "Website và blog",
                        ["Ảnh bìa bài viết và ảnh chia sẻ link của adtek.agency.",
                         "Bảy phong cách ảnh bìa xoay vòng, cùng bảng màu và phông chữ."], main)


def reports(n, a):
    g = "".join(img(a[f"report-{s}"], "width:100%;outline:1px solid rgba(0,45,114,.14);outline-offset:-1px") for s in REPORTS)
    main = f"""<div class="grid" style="grid-template-columns:1fr 1fr;gap:24px;width:1000px">{g}</div>"""
    return content_page(n, "Ứng dụng thương hiệu", "5.7", "Báo cáo và tài liệu",
                        ["Ảnh đại diện và bìa PDF cho thư viện báo cáo miễn phí của Adtek.",
                         "Bốn biến thể màu xoay vòng: nền navy hoặc kem, khối kem, cam hoặc navy chứa con số chính.",
                         "Bìa có nhãn \"Báo cáo Adtek\", tiêu đề một từ khóa cam và con số nổi bật nhất của báo cáo."], main)


def closing(a):
    return f"""<section class="page dark">
<div style="position:absolute;right:-260px;bottom:-330px;width:1300px">{img(a['mark-orange'], 'width:100%')}</div>
<div style="position:absolute;left:120px;top:110px">{img(a['logo-white'], 'height:120px')}</div>
<h2 style="position:absolute;left:120px;top:440px;font-size:80px;font-weight:600;letter-spacing:-.025em;line-height:1.1;width:1000px">
Cảm ơn bạn đã cùng xây dựng thương hiệu <span class="hl">Adtek</span>.</h2>
<div style="position:absolute;left:120px;bottom:110px;font-size:22px;line-height:1.7;opacity:.8">adtek.agency&nbsp;&nbsp;·&nbsp;&nbsp;contact@adtek.agency&nbsp;&nbsp;·&nbsp;&nbsp;+84 9323 494 34</div></section>"""


# ---------------------------------------------------------------- dựng tài liệu

def build():
    a = build_assets()
    plan = [
        ("1.0", "Thương hiệu Adtek", [("1.1", "Mục đích thương hiệu", purpose), ("1.2", "Định vị thương hiệu", positioning),
                                      ("1.3", "Tính cách thương hiệu", personality)]),
        ("2.0", "Ngôn ngữ thương hiệu", [("2.1", "Khẩu hiệu thương hiệu", slogan), ("2.2", "Câu chuyện thương hiệu", story),
                                         ("2.3", "Thông điệp thương hiệu", messages), ("2.4", "Giọng văn", voice)]),
        ("3.0", "Nhận diện thương hiệu", [("3.1", "Logo thương hiệu", logo_page), ("3.2", "Vùng an toàn và kích thước tối thiểu", clearspace),
                                          ("3.3", "Logo trên nền màu", on_colors), ("3.4", "Trường hợp sử dụng sai", misuse)]),
        ("4.0", "Thành tố thương hiệu", [("4.1", "Bảng màu", palette), ("4.2", "Phông chữ thương hiệu", type_brand),
                                         ("4.3", "Phông chữ hệ thống", type_system), ("4.4", "Quy tắc chữ", type_rules),
                                         ("4.5", "Thiết bị đồ họa", devices), ("4.6", "Phong cách thiết kế", style_rules)]),
        ("5.0", "Ứng dụng thương hiệu", [("5.1", "Danh thiếp", business_card), ("5.2", "Tiêu đề thư", letterhead),
                                         ("5.3", "Trang mẫu trình bày", slides), ("5.4", "Chữ ký email", signature),
                                         ("5.5", "Mạng xã hội", social), ("5.6", "Website và blog", web),
                                         ("5.7", "Báo cáo và tài liệu", reports)]),
    ]
    # đánh số trang: bìa 1, mục lục 2, mỗi phần một trang ngăn cách rồi các trang nội dung
    n = 3
    sections = []
    for num, title, subs in plan:
        div_page = n
        n += 1
        items = []
        for k, t, fn in subs:
            items.append((k, t, n, fn))
            n += 1
        sections.append((num, title, div_page, items))
    toc_data = [(num, title, [(k, t, p) for k, t, p, _ in items]) for num, title, _, items in sections]
    pages = [cover(a), toc(a, toc_data)]
    for num, title, _, items in sections:
        pages.append(divider(a, num, title, [(k, t, p) for k, t, p, _ in items]))
        for _, _, p, fn in items:
            pages.append(fn(p, a) if fn.__code__.co_argcount == 2 else fn(p))
    pages.append(closing(a))
    html_text = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>{DOC}</title><style>{font_css()}{CSS}</style></head>
<body>{''.join(pages)}</body></html>"""
    src = BUILD / "guide.html"
    src.write_text(html_text, encoding="utf-8")
    if PREVIEW.exists():
        shutil.rmtree(PREVIEW)
    PREVIEW.mkdir(parents=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["node", str(ROOT / "tools/render_pages.js"), str(src), str(OUT), str(W), str(H), str(PREVIEW)], check=True)
    shutil.rmtree(BUILD)
    print(OUT, len(pages), "trang")


if __name__ == "__main__":
    build()
