# Quy trình nội dung blog

Lịch đăng, cụm chủ đề và danh sách bài nằm trong `calendar.json`.

## Nhịp đăng

- Lịch do phiên **Adtek - Marketing** (session_01XqVohyrjLRctpapS6FbMXD) lập mỗi tháng, 3 ngày trước ngày 1 tháng mới (`routines/monthly-planning.md`, kế hoạch và nghiên cứu trong `reports/`). Các phiên Blog post, Facebook post, Designer, SEO chỉ viết và đăng theo lịch, không tự đổi `date`, `time`, không chạy `retime` (anh Tin chọn 16/10/2026).
- Blog: 4 bài/tuần từ tuần 19/10/2026 (anh Tin chọn triển khai từ 17/10), mỗi bài khoảng 2,000 chữ, đăng thứ Hai, Ba, Năm, Sáu, 08:05 đến 08:55. Bài `backlog` là bài chờ, chưa có lịch. Bài 1 đến 4 giữ giờ cũ.
- Facebook: 1 bài mỗi ngày từ 17/10/2026, định dạng riêng cho Facebook, không đăng lại bài blog (danh sách `facebook` trong `calendar.json`). Bài mở bài blog của bài 2 đến 6 đã hủy (`fb_status` cancelled), chỉ bài 1 đã đăng.
- Đăng Facebook hằng ngày (phiên Adtek - Facebook post): công cụ `tools/fb_daily.py` (due, week, show, notify, publish, approve, cancel, auto, delete), 3 lịch trong `routines/facebook-daily.md`: báo trước 8:43 và 16:43 (tuần đầu đến 25/10: anh Tin không nhắn hủy thì đăng), đăng 12:13 và 20:13, viết caption tuần tới 9:07 thứ Tư (từ tuần 26/10, duyệt D+1). Page chỉ bình luận link bài blog `link_post` khi bài đó đã lên sóng; nếu chưa, caption bỏ câu "Xem full bài viết ở bình luận bên dưới."
- TikTok: 3 video/tuần (danh sách `tiktok`), do phiên TikTok anh Tin sẽ tạo.
- Văn phong: viết theo `content/editorial/van-phong.md` (rút từ bài mẫu của anh Tin, 17/10/2026): ngôi "tôi" và "bạn", vào thẳng việc, khái niệm kèm tên tiếng Anh và phép tính nhỏ, so sánh đời thường, một ví dụ làm từng bước, công thức kèm danh sách "Không nên".
- Mỗi bài cần có một phần dùng được ngay: khung, checklist hoặc bảng tính. Không viết mini-case hay số liệu dự án (anh Tin bỏ ngày 16/10/2026).
- Tác giả Tin Le, có SEO title, meta description và ảnh bìa. Ảnh bìa blog (bố cục 1200x630, xuất file 2400x1260 cho màn Retina, `python3 tools/blog_post.py cover X`) và ảnh Facebook (1:1, `python3 tools/fb_post.py cover X`) dựng từ bộ mẫu `tools/covers.py`: 7 phong cách thiết kế phẳng, chỉ dùng màu navy, cam, kem của Adtek, không đường kẻ hay gạch chân, không hình tròn bao quanh logo hoặc chữ, không gradient, quầng sáng, kính mờ, bóng đổ (anh Tin yêu cầu 16/10/2026: không giống ảnh AI): tạp chí nền kem, khối cam navy cắt chéo, chữ A Adtek cỡ lớn, hai tầng màu có số cam lớn, áp phích nền cam; đối đầu A vs B cho bài so sánh, hồ sơ pháp lý cho bài luật. Mẫu tím neon 3D cũ chỉ dùng khi ghi tay `cover.style`. Chữ (theo mẫu McKinsey anh Tin gửi 16/10/2026): tiêu đề Inter Tight 600 viết thường như câu, một từ khóa tô màu nhấn bằng cách bọc trong dấu sao (`*từ khóa*`) ở các trường chữ; mô tả Inter Tight 400; con số và cụm chữ đọc liền sau số dùng Newsreader 600 (chữ có chân); không dùng chữ in hoa giãn khoảng cho tiêu đề. Không đặt chữ trên nền cam (anh Tin 17/10/2026): cam chỉ dùng cho con số, từ khóa tô màu và mảng không có chữ (ví dụ chữ A lớn); nhãn nhỏ (kicker, chip, tên dạng bài) cùng màu chữ xung quanh, không tô cam; nền sáng dùng kem, không dùng trắng. Con số lớn (`cover.hero`) luôn đứng sát cụm chữ đi kèm (`cover.hero_text`) và đứng trước theo thứ tự đọc: bên trái hoặc phía trên cụm chữ, không đặt số một nơi, chữ một nẻo. Lần dựng đầu, hệ thống tự chọn phong cách theo nội dung (phương án A anh Tin chọn 16/10/2026): bài có "vs" trong `cover.title` dùng mẫu đối đầu, bài luật dùng mẫu hồ sơ (nếu 2 bài liền trước chưa dùng), còn lại xoay vòng 5 mẫu chung và tránh 3 bài liền trước; phong cách được ghi vào `cover.style` để dựng lại vẫn giữ nguyên, muốn đổi thì sửa tay trường này. Dữ liệu ảnh: `cover.kicker`, `title`, `subtitle`, `chips` (blog) và `hero`, `hero_text`, `fb_kicker` (Facebook, một số mẫu blog cũng dùng số `hero`). Chữ và logo trên ảnh blog nằm trong vùng x 140 đến 1060, y 70 đến 560 vì theme cắt ảnh: thẻ 370x250 mất hai bên, trang /blog/ 870x362 mất khoảng 65px trên và dưới. Xem thử mọi phong cách cho một bài: `python3 tools/covers.py sheet X`. Bài cũ (mục `existing`, có `slug`, `date`, `cover` kèm `style`): `python3 tools/covers.py existing <wp_id>`. Đổi ảnh bìa bài đã đưa lên WordPress: `python3 tools/blog_post.py recover X [--delete-old]`. Bài đăng trước lịch (không có trong `calendar.json`, ví dụ 6076, 6078): `python3 tools/blog_post.py feature <ID bài> <file ảnh> [--delete-old]`. Ảnh do phiên "Adtek - Designer" dựng và commit; phiên "Adtek - Blog post" chỉ tải lên (`recover` dùng đúng file có sẵn).

## Quy trình viết và duyệt

1. Thứ Sáu hằng tuần (lịch tự động 8:52 sáng): viết tối đa 4 bài `planned` có ngày đăng sớm nhất trong 14 ngày tới, đưa lên WordPress ở dạng nháp bằng `python3 tools/blog_post.py draft <số bài>`, nhắc anh Tin duyệt qua email (hi@tinle.co), push notification và tin nhắn trong phiên Claude Code.
2. Anh Tin duyệt từng bài:
   - "duyệt bài X": chạy `python3 tools/blog_post.py schedule X`, WordPress tự đăng đúng ngày giờ trong lịch.
   - Yêu cầu sửa: chạy `python3 tools/blog_post.py changes X`, sửa xong gửi email duyệt lại (hạn 24 giờ tính lại từ lần gửi mới).
   - "hủy bài X" (kể cả khi đã đặt lịch): chạy `python3 tools/blog_post.py unschedule X`.
   - Hạn duyệt D+1: email gửi bằng `tools/approval_email.py --mark` ghi thời điểm gửi. Đúng 24 giờ sau, lịch hẹn một lần (send_later) chạy `python3 tools/blog_post.py auto`: bài chưa có phản hồi được tự đặt lịch đăng theo kế hoạch (approval = auto), rồi báo anh Tin qua email và push notification. Bài đã duyệt hoặc đang chờ sửa thì bỏ qua.
   - Cách cũ, chỉ còn để tham khảo (bài 1 đã đăng; bài 2 đến 6 đã hủy từ 16/10/2026). Bài đăng Facebook: mỗi bài blog có `fb_caption` (khoảng 150 đến 200 chữ, kể chuyện bằng một tình huống hoặc con số cụ thể trong bài, dẫn người đọc mở link ở bình luận) và `fb_comment` (tiêu đề ngắn + link bài). Không dùng emoji, không gạch dài, không đặt link trong nội dung chính. Caption không tự viết câu mời xem bài: `tools/fb_post.py` tự đặt câu CTA chung "Xem full bài viết ở bình luận bên dưới." lên đầu caption (email duyệt hiển thị đúng bản đăng thật). Duyệt cùng bài blog trong email.
   - Đăng Facebook qua Graph API (`tools/fb_post.py`; network secret của môi trường gắn header `Authorization: Bearer <Page access token>` cho `graph.facebook.com`; script tự dừng nếu token không thuộc Page 101888089257566): bài đăng lên Page Adtek Growth Agency dạng ảnh vuông 1:1 `content/posts/<slug>-fb.jpg` (do phiên **Adtek - Designer** làm và push lên nhánh `claude/brave-curie-2c6zbc`; phiên Facebook chỉ đăng ảnh có sẵn, thiếu ảnh thì dừng và báo anh Tin, dựng bằng `python3 tools/fb_post.py cover X` theo bộ mẫu `tools/covers.py`, cùng phong cách với ảnh bìa blog của bài; một con số lớn lấy từ nội dung bài (`cover.hero`) đọc liền với câu bên cạnh (`cover.hero_text`, ví dụ "30" + "Ngày chuẩn bị 11.11"), nhãn nhỏ `cover.fb_kicker`, mô tả `cover.subtitle`) + CTA + `fb_caption`, không có link; Page tự bình luận `fb_comment` ngay dưới bài. Khi bài blog được đặt lịch (duyệt hoặc tự duyệt D+1), hẹn send_later vào 5 phút sau giờ đăng blog để chạy `python3 tools/fb_post.py post X`. Script chỉ đăng khi bài blog đã lên sóng (hủy bài thì bài Facebook cũng không đăng) và không đăng trùng.
   - Caption Facebook theo template (tools/fb_post.py tự ghép): dòng 1 `fb_title` (câu hỏi gợi tò mò, viết in hoa), dòng 2 "Xem full bài viết ở bình luận bên dưới.", rồi `fb_caption`, rồi 5 hashtag (`#Adtek #GrowthMarketing` mặc định + 3 hashtag riêng trong `fb_hashtags`, không dấu, viết liền), cuối cùng "Website: adtek.agency" và "Email: contact@adtek.agency".
3. Thứ Hai, Ba, Năm, Sáu 21:43 (lịch tự động của phiên **Adtek - SEO**): tối ưu SEO và làm liên kết ngược cho bài vừa lên sóng, xem mục "Tối ưu SEO sau khi đăng".
4. Ngày 1 hằng tháng (lịch tự động 8:47 sáng): rà soát và cập nhật nội dung, gửi báo cáo qua email, push notification và tin nhắn trong phiên.

## Ảnh Facebook hằng ngày

Bài Facebook riêng (danh sách `facebook` trong `calendar.json`) dùng ảnh 1080x1080 do phiên **Adtek - Designer** dựng bằng `tools/social.py`, cùng nhận diện với ảnh bìa (phẳng, navy, cam, kem; Inter Tight cho tiêu đề và chữ, Newsreader cho số và cụm chữ đi liền sau số, `*từ khóa*` để tô màu nhấn; không đường kẻ, không hình tròn bao chữ hoặc logo, không gradient, không bóng đổ).

- Nội dung chữ trên ảnh nằm trong trường `design` của từng bài (phiên Designer viết, chỉ dùng số liệu có trong `brief`, nguồn hoặc bài blog). Cấu trúc theo dạng bài ghi ở đầu `tools/social.py`.
- Ảnh lưu ở `content/facebook/<id>/1.jpg`, `2.jpg`... (carousel nhiều ảnh theo thứ tự). Trường `images` ghi danh sách đường dẫn tương đối theo đúng thứ tự đăng; phiên Facebook post đăng đúng các file này, thiếu `images` thì dừng và báo.
- Mỗi dạng bài có 2 biến thể, tự xoay vòng theo số lần dạng đó đã xuất hiện; ghi `design.variant` (0 hoặc 1) để ép một biến thể.
- Dạng bài: Góc số liệu (số lớn đứng trên cụm chữ), Thuật ngữ 1 phút (như mục từ điển), Carousel hướng dẫn (trang bìa, mỗi bước một trang, trang kết; số trang ghi chữ ở góc), Tin nóng (mốc thời gian trên tiêu đề, các ý đánh số), Phép tính nhanh (bảng tính, dòng kết quả nền cam), Hiểu lầm và sự thật (hai khối màu), Câu hỏi mở (lựa chọn A, B, C). Video ngắn (Reels) không dựng ảnh.
- Lệnh: `python3 tools/social.py render <id>`, `python3 tools/social.py week <ngày đầu> <ngày cuối>`, `python3 tools/social.py missing` (bài sắp đăng chưa có design hoặc ảnh).
- Duyệt ảnh (anh Tin chọn phương án A ngày 16/10/2026): ảnh được duyệt cùng bài, không có bước duyệt riêng. Bài quá hạn duyệt thì tự duyệt và đăng kèm ảnh hiện có; ảnh xem trước phiên Designer gửi không chặn việc đăng. Ảnh lỗi sau khi đăng: phiên Facebook post gỡ bài, phiên Designer sửa rồi đăng lại.
- Nhịp: ảnh tuần sau xong trước thứ Sáu tuần trước để kịp gửi duyệt; sửa `design` thì dựng lại và báo phiên Facebook post.

## Cụm chủ đề (topic cluster)

Mỗi cụm có một bài trụ cột (pillar) bao quát, các bài con đi sâu từng khía cạnh.

| Cụm | Tên | Bài trụ cột |
|---|---|---|
| C1 | Thương mại điện tử và Social Commerce | Bài 3 (TikTok Shop và Shopee 2026) |
| C2 | Quảng cáo Performance và Creative | Bài 2 (Quảng cáo Meta 2026) |
| C3 | Dữ liệu, CRM và đo lường | Bài 5 (MER, CAC, LTV) |
| C4 | SEO và AI Search | Bài đã đăng 6076 (AIO là gì) |
| C5 | Chiến lược tăng trưởng | Bài đã đăng 2215 (Growth Marketing, cần cập nhật lớn) |
| C6 | Playbook theo ngành | Không có trụ cột, mỗi bài trỏ về trụ cột của phương pháp liên quan |

## Quy tắc liên kết

Mỗi bài mới khi đăng phải có:

1. 1 link lên bài trụ cột của cụm.
2. Ít nhất 2 link sang bài cùng cụm (tính cả bài cũ), theo cột `links_to` trong `calendar.json`.
3. Ít nhất 1 link sang cụm khác nếu nội dung liên quan.
4. Link thuật ngữ trong từ điển Adtek ở lần nhắc đầu tiên (ví dụ CDP, CRM, Brand Strategy).
5. Anchor text là từ khóa của bài đích, không dùng "xem thêm" hay "tại đây".
6. Ít nhất 3 nguồn bên ngoài uy tín (văn bản luật, cơ quan nhà nước, báo cáo nghiên cứu, tài liệu chính thức của nền tảng), ghi rõ tháng/năm của số liệu. Link ra ngoài luôn có `rel="nofollow noopener"` và mở tab mới (`tools/blog_post.py draft` tự gắn).
7. 1 lời mời liên hệ (`/contact/`) hoặc tài nguyên miễn phí của Adtek.

Ngay sau khi bài lên sóng (liên kết ngược, phiên Adtek - SEO làm trong lịch 21:43 các ngày đăng blog):

- Thêm link từ bài trụ cột của cụm về bài mới.
- Thêm link từ 2 đến 3 bài đã đăng có trong `links_to` của bài mới, hoặc có `links_to` trỏ tới bài mới.
- Không bài nào được ở trạng thái "mồ côi" (không có link nội bộ nào trỏ vào).

## Tối ưu SEO sau khi đăng

Phiên **Adtek - SEO** (session_013GwSn1yAegYgnHucCuLbNr) chạy lúc 21:43 thứ Hai, Ba, Năm, Sáu (prompt: `routines/seo-after-publish.md`), xử lý mọi bài đã lên sóng mà chưa có `seo_optimized` trong `calendar.json`, nên bài dời ngày hoặc bị sót được bắt ở lần chạy kế tiếp. Anh Tin cho phép tự sửa bài đang live rồi báo sau (16/10/2026); mọi lần sửa nội dung đều backup vào `content/backups`.

Công cụ `tools/seo_post.py`:

| Lệnh | Việc |
|---|---|
| `due` | Bài đã lên sóng chưa tối ưu SEO, tự đổi `scheduled` thành `published` |
| `fix X` | Focus keyphrase Yoast = `keyword`, alt ảnh đại diện và ảnh trong bài, nofollow link ngoài |
| `links X` | Bài nên trỏ link về bài X (trụ cột, `links_to`, bài có `links_to` chứa X) và bài nào đã có link |
| `check X` | 29 mục kiểm tra trên bản live, in mục lỗi kèm cách sửa |
| `meta X` | Ghi `seo_title`, `meta_desc` trong `calendar.json` lên Yoast |
| `get ID file`, `put ID file "lý do"` | Tải nội dung gốc để sửa, ghi lại kèm backup (bài trong lịch thì đồng bộ luôn `content/posts/<slug>.html`) |
| `done X` | Ghi `seo_optimized` |
| `gsc.py submit`, `gsc.py notify X`, `gsc.py pending` | Gửi lại sitemap, báo Google bài X qua Indexing API, kiểm tra bài chưa index |

Các mục `check`:

- Kỹ thuật: HTTP 200 đúng URL, không noindex, canonical trỏ về chính nó, có trong post-sitemap.xml, schema Article, og:image, đúng 1 H1.
- SEO title 30 đến 60 ký tự, có từ khóa và từ khóa nằm ở đầu; meta description 120 đến 156 ký tự, có từ khóa; slug chứa từ khóa (chỉ ghi nhận, không đổi slug bài đã đăng).
- Từ khóa: focus keyphrase Yoast, trong 120 chữ đầu, trong ít nhất 1 H2, đúng cụm xuất hiện từ 3 lần (tối đa khoảng 1 lần mỗi 150 chữ).
- Ảnh: alt ảnh đại diện, alt mọi ảnh trong bài.
- Liên kết ra: link ngoài có nofollow noopener và mở tab mới, ít nhất 3 nguồn ngoài, ít nhất 3 link nội bộ, có link lên trụ cột và tới các bài trong `links_to` đã đăng, không anchor kiểu "xem thêm", "tại đây", không link nội bộ hỏng.
- Liên kết vào: trụ cột đã trỏ về, ít nhất 3 bài trỏ về (2 nếu cụm không có trụ cột).
- Độ dài từ 1,500 chữ.

Google Search Console (`tools/gsc.py`, anh Tin chọn ngày 16/10/2026): sau mỗi lần tối ưu, gửi lại `sitemap_index.xml` (`submit`); mỗi lần chạy kiểm tra các bài đăng từ 2 đến 30 ngày trước mà chưa được index (`pending`, ghi `index_status`, `index_checked` vào `calendar.json`). Google không có API cho nút "Yêu cầu lập chỉ mục". Anh Tin chọn phương án B (16/10/2026): báo Google mỗi bài mới qua Indexing API (`notify`), dù Google chỉ chính thức hỗ trợ API này cho trang tuyển dụng và livestream nên có thể bị lờ đi hoặc thu hồi quyền; service account là Owner của property, project bật Web Search Indexing API, hạn mức 200 URL/ngày. API từ chối hoặc bài vẫn chưa index sau 2 ngày thì gửi anh Tin link để bấm tay. Đăng nhập bằng service account: khóa JSON đặt trong biến môi trường `GSC_SERVICE_ACCOUNT` (nguyên văn hoặc base64), email service account được thêm vào property https://adtek.agency/ (loại URL-prefix) với quyền Owner (cần cho Indexing API). Đã kết nối và kiểm tra ngày 16/10/2026. Biến môi trường chỉ có trong container khởi động sau khi thêm biến; phiên chạy từ trước thì dùng phiên phụ (xem `routines/seo-after-publish.md`).

Giới hạn: mạng của môi trường chặn site bên ngoài nên không kiểm tra được link ngoài còn sống (lịch rà soát ngày 1 hằng tháng xử lý). Xóa cache thủ công cần plugin `adtek-acf-rest.php` 1.1.0 (đang chờ upload); WordPress vẫn tự xóa cache của bài khi lưu.

## Quy trình cập nhật nội dung

Mỗi bài có hạng làm mới trong `calendar.json`:

| Hạng | Chu kỳ rà soát | Loại nội dung |
|---|---|---|
| A | 3 tháng | Luật, tính năng nền tảng quảng cáo, số liệu thị trường |
| B | 6 tháng | Hướng dẫn, quy trình |
| C | 12 tháng | Khái niệm nền tảng |
| S | 6 tuần trước mùa năm sau | Bài theo mùa (11.11, Tết, ngân sách năm) |

Rà soát định kỳ, ngày 1 hằng tháng:

1. Lấy các bài đến hạn theo `last_reviewed` (hoặc `published` nếu chưa rà lần nào) cộng chu kỳ của hạng.
2. Kiểm tra từng nhận định có mốc thời gian: số liệu, điều luật, tính năng, giá, tên sản phẩm. Đối chiếu với nguồn mới nhất.
3. Kiểm tra link hỏng (nội bộ và bên ngoài).
4. Phân loại và xử lý:
   - Sửa nhỏ (số liệu mới, link hỏng, tên tính năng đổi): sửa trực tiếp.
   - Sửa lớn (nhận định chính không còn đúng, cần viết lại một phần): soạn bản cập nhật, chờ duyệt rồi mới đăng.
5. Sau khi sửa: giữ nguyên URL, thêm dòng "Cập nhật ngày ..." đầu bài kèm tóm tắt thay đổi, cập nhật `last_reviewed`, ghi `logs/changelog.md`.

Rà soát theo sự kiện: khi có luật mới, nền tảng đổi tính năng lớn hoặc số liệu thị trường mới công bố, cập nhật ngay các bài liên quan, không chờ đến kỳ.

- Ảnh chia sẻ mặc định của website (og:image cho trang chủ VI, EN và trang không có ảnh đại diện): `content/brand/og-default.jpg` (1200x630) và `og-default@2x.jpg` (2400x1260), dựng bằng `python3 tools/covers.py og [navy|cream|panel]`. Chữ và logo trong vùng x 100 đến 1100, y 60 đến 570. Nội dung chỉ gồm logo, "Growth marketing agency", "Brand Commerce, Lead Generation, SEO", adtek.agency; không thêm số liệu hay khẩu hiệu. Phiên Designer dựng, phiên SEO tải lên và gắn vào Yoast.
