# Quy tắc làm video TikTok Adtek

Kênh @adtek.growth.marketing (Adtek Growth Marketing Agency). Các quy tắc dưới đây do anh Tin chốt, áp dụng cho mọi video. Chi tiết kỹ thuật xem `README.md`, lịch và nguồn số liệu xem `plan/lich-noi-dung-tiktok.xlsx`.

## Nội dung

- Kênh TikTok độc lập với website: mỗi video một chủ đề riêng, không dẫn về blog, không đặt link trong caption.
- Bám dịch vụ Adtek: Digital Marketing, Growth Marketing, App Marketing, SEO, AIO, Performance Marketing. Ưu tiên chủ đề đang trend, có nhu cầu tìm kiếm.
- Mỗi video khoảng 1 phút (50 đến 65 giây). Dạng infographic chuẩn có 6 cảnh: câu hỏi mở đầu, 3 đến 4 cảnh số liệu, 1 cảnh "làm gì ngay", cảnh Follow. Các dạng khác theo cấu trúc riêng ở mục "Đa dạng dạng video".
- Câu đầu tiên của lời đọc là một câu hỏi khơi tò mò.
- Chỉ giữ ý mạnh, số liệu ấn tượng. Một chủ đề làm thành một video, không tách nhỏ thành nhiều video.
- Không trùng video đã đăng: trước khi viết, đọc mọi kịch bản có status "Đã đăng" (kể cả bản archived) và các video đã có lịch. Không lặp lại góc nhìn chính hay số liệu đã dùng. Ví dụ: video AIO đã đăng nói tóm tắt AI của Google làm giảm lượt bấm (Pew 15% xuống 8%), nên chủ đề "đứng top 1 Google vẫn mất khách" bị bỏ vì trùng ý.
- Cảnh "Làm gì ngay" thể hiện chuyên môn của Adtek nên phải nghiên cứu kỹ, không viết chung chung, không tự bịa. Mỗi việc phải:
  - Cụ thể tới mức làm được ngay: tên tính năng, công cụ, con số hoặc vị trí cài đặt. Ví dụ: "Không chặn OAI-SearchBot trong robots.txt", không viết "tối ưu cho AI".
  - Có căn cứ từ nguồn chính thức (tài liệu của Google, Meta, OpenAI, Zalo, TikTok) hoặc nghiên cứu gốc (Baymard, Klaviyo...). Kiểm tra nguồn như với số liệu.
  - Trả lời đúng vấn đề mà các cảnh số liệu trước đó nêu ra.
  - Dùng `items` dạng `{ "text": việc cần làm, "detail": căn cứ hoặc cách làm }` và ghi `source` ở cuối danh sách. Ghi nguồn của từng việc vào email duyệt kịch bản.
- Giữ chân người xem (anh Tin chốt hướng A và C, 08/10/2026):
  - Khung đầu tiên phải có ngay câu hook và con số: `Video.tsx` tự hiện cảnh đầu ở trạng thái cuối của hiệu ứng, không đếm từ 0.
  - Mỗi kịch bản có trường `cover` (3 đến 5 chữ, ví dụ "8/10 khách" + "muốn nhắn tin trước khi mua"). Video đố số liệu: ảnh bìa, khung đầu, caption và tiêu đề cảnh 1 chỉ được đặt câu hỏi và hiện lựa chọn (`cover.options`), tuyệt đối không lộ đáp án; lộ đáp án là mất lý do để bình luận và xem đến cuối; `render.mjs` xuất `out/<id>-cover.png` để làm ảnh bìa; tải ảnh này lên kho asset của hub và ghi url vào trường `cover` trong `hub/videos.json` (hub có nút Tải ảnh bìa).
  - Âm thanh chuyển cảnh và tiếng "bật" khi số hiện được thêm tự động (`public/sfx`).
  - Đổi kiểu video (xem thêm mục "Đa dạng dạng video"), trong đó có **đố số liệu** (`quiz`: hỏi ở cảnh đầu với 3 lựa chọn, 2 cảnh gợi ý, cảnh lật đáp án `reveal: true`) và **phá hiểu lầm** (`myth`: câu nhiều người tin, đóng dấu "SAI" hoặc "CHƯA ĐÚNG", rồi số liệu chứng minh). Kiểu video hướng dẫn (quay màn hình) cần anh Tin quay, chỉ đề xuất trong email.
  - Cảnh cuối có `ask`: câu hỏi cụ thể để người xem bình luận (ví dụ "Shop bạn trả lời tin nhắn trong bao lâu? Comment số phút"), không chỉ "Follow". Caption cũng kết bằng câu hỏi đó.
- Cảnh cuối dùng `follow`, lời đọc kết bằng "Follow Adtek để xem số liệu marketing mới mỗi ngày."
- Chỉ làm video bằng Remotion. Không làm thêm bản giấy cắt dán hay phong cách minh họa bằng bộ animate (anh Tin chốt 10/10/2026: chỉ đăng thử 1 bản cho video 11/10, các lần sau không làm). Chỉ làm lại khi anh Tin yêu cầu.
- Giọng đọc là đồng hồ (anh Tin duyệt hướng A từ bộ animate, 10/10/2026): hình hiện theo lúc giọng nhắc tới, nên khi viết lời đọc:
  - Đọc con số đúng như trên biểu đồ và theo thứ tự hiển thị (thanh 69, 60, 51 thì đọc 69%, 60%, 51%).
  - Mỗi việc trong "Làm gì ngay" được đọc lại ít nhất 2 chữ liền nhau của dòng chữ trên màn hình; dòng chi tiết cũng vậy nếu muốn nó hiện sau.
  - Cảnh phá hiểu lầm đọc chữ trên con dấu ("Sai.") để con dấu đóng đúng lúc. Cảnh lật đáp án mở đầu bằng "Đáp án là ...".
  - Không để màn hình đứng yên quá 4 giây: câu dài thì chia ý, mỗi ý một con số hoặc một dòng hiện thêm.
  - Trước khi xuất, chạy `node tools/check.mjs <slug>`: FAIL phải sửa; WARN đứng hình hoặc nhịp đọc (trên 3.5 chữ/giây) thì sửa lời đọc hoặc bố cục nếu được, không được thì ghi lý do trong email.

## Đa dạng dạng video (anh Tin chốt 10/10/2026: mọi dạng đều phù hợp, làm đa dạng để người xem không nhàm chán)

- 7 dạng video, chọn theo dữ liệu và góc nhìn của chủ đề:
  1. **Infographic chuẩn**: 6 cảnh, mỗi cảnh một biểu đồ.
  2. **Đố số liệu** (`quiz`): hỏi đầu video, 2 cảnh gợi ý, lật đáp án.
  3. **Phá hiểu lầm** (`myth`): câu nhiều người tin, đóng dấu "SAI", rồi số liệu.
  4. **Chữ động** (`words`): 8 đến 12 nhịp, mỗi nhịp 2 đến 3 dòng chữ to (mỗi dòng tối đa 18 ký tự), không biểu đồ; hợp chủ đề quan điểm, lời khuyên, sự kiện theo mùa. Mỗi nhịp có số liệu vẫn ghi nguồn.
  5. **Đếm ngược top 5** (`countdown`): cảnh mở đầu `teaser: true` (5 ô "?"), đọc "Hạng 5" tới "Hạng 1", hạng 1 sau một câu nhử. Chỉ dùng bảng xếp hạng chính thức có thứ tự rõ ràng.
  6. **Bản đồ** (`map`): số liệu theo từng nước Đông Nam Á từ cùng một nguồn, Việt Nam tô cam.
  7. **Biểu đồ đua** (`race`): ít nhất 5 mốc thời gian từ cùng một nguồn, không trộn nguồn, không tự nội suy số thiếu. Ưu tiên chuỗi số có vượt mặt thật; không có thì nói rõ là "thu hẹp khoảng cách".
- Mỗi tuần (7 video) dùng ít nhất 5 dạng khác nhau, không dạng nào lặp lại 2 ngày liền, infographic chuẩn tối đa 2 video. Dạng cần dữ liệu đặc biệt (bản đồ, biểu đồ đua, đếm ngược) chỉ làm khi có số liệu gốc phù hợp; không có thì đổi dạng khác và ghi lý do trong email duyệt.
- Mọi dạng vẫn giữ: câu đầu là câu hỏi, số liệu gốc đã kiểm tra, lời đọc 150 đến 190 chữ, cảnh cuối `follow` có `ask`, ảnh bìa (`cover`) không lộ đáp án hay hạng 1.
- Ảnh lướt (TikTok photo mode): mỗi tuần xuất 1 bộ từ video nhiều số liệu nhất của tuần (`render.mjs <slug> --carousel`), đưa lên hub kèm video đó (trường `carousel` trong `hub/videos.json`). Đăng thêm lúc 20:00, cách ngày đăng video gốc ít nhất 3 ngày.
- Khổ vuông 1:1 và khổ ngang 16:9 (`--format`): chỉ xuất khi anh Tin cần đăng Facebook, Instagram, YouTube.
- Mẫu từng dạng: `scripts/3-dieu-truoc-sale-11-11` (chữ động), `scripts/top5-tu-khoa-tang-manh-2025` (đếm ngược), `scripts/kinh-te-so-viet-nam-dung-thu-may` (bản đồ), `scripts/tiktok-shop-duoi-sat-shopee` (biểu đồ đua), `scripts/khach-so-gia-cho-sale` (đố số liệu), `scripts/thue-kol-khach-co-tin` (phá hiểu lầm).

## Chọn biểu đồ theo kiểu dữ liệu

- 1 con số gây sốc: `bignumber`. 2 con số đối đầu: `versus`. Trước và sau của vài nhóm: `slope`. Xu hướng từ 3 mốc: `trend`. Chia phần trong tổng: `donut`. "x trên 10 người": `people`, "x trên 100": `waffle`. Rơi rụng qua từng bước: `funnel`. Xếp hạng từ 3 mục: `hbars`. So sánh 2 đến 4 nhóm: `columns`. Việc cần làm: `list`.
- Video infographic dùng ít nhất 3 loại biểu đồ khác nhau, không dùng cùng một loại cho 2 cảnh liền nhau. Video liền kề trong lịch nên mở đầu bằng loại biểu đồ khác nhau.
- Ảnh chụp bài báo, báo cáo (`shot`, chụp bằng `tools/shot.mjs`): dùng cho con số mạnh nhất của video, nhất là số từ cơ quan nhà nước, báo chí hoặc báo cáo gốc. Tối đa 1 cảnh mỗi video, các cảnh còn lại vẫn là biểu đồ. Chỉ chụp trang gốc, không sửa ảnh, không dựng giả giao diện trang báo.
- Không bóp méo dữ liệu cho đẹp: độ rộng, độ cao luôn đúng tỷ lệ; trục không bắt đầu từ 0 thì ghi rõ.

## Viết tiếng Việt tự nhiên

- Viết như người Việt nói, không dịch thẳng từ tiếng Anh. Áp dụng cho lời đọc, tiêu đề, nhãn biểu đồ, chú thích, dòng nguồn và caption.
- Đọc to lên, câu nào nghe như văn bản dịch thì viết lại. Ví dụ: "lọc bạn" → "so sánh bạn", "danh sách lọc" → "lọt vào danh sách", "hành trình mua" → "cách khách hàng mua hàng", "hệ sinh thái" → "doanh nghiệp lớn ở gần", "ổn định chính trị" → "chính trị ổn định", "người mua B2B" → "khách hàng doanh nghiệp".
- Tránh từ sáo rỗng: đóng vai trò quan trọng, bứt phá, giải pháp toàn diện, hành trình, kỷ nguyên, chìa khóa thành công, trong bối cảnh hiện nay.
- Không dùng ký tự "—". Số viết theo US format (75,000; 0.61%).

## Số liệu

- Ưu tiên theo thị trường: số liệu Việt Nam trước; không có mới dùng Đông Nam Á; không có nữa mới dùng toàn cầu hoặc Mỹ, và phải ghi rõ trên video ("số liệu Mỹ", "số liệu quốc tế"). Nguồn Việt Nam nên tìm: Cục Thống kê, Bộ Công Thương, Vietnam Report, Decision Lab, Q&Me, Milieu Insight, Kantar, NielsenIQ Việt Nam, Metric, phần Việt Nam trong e-Conomy SEA. Ví dụ: video khách hỏi AI dùng 78.4% người tiêu dùng Gen Y, Gen Z đã dùng AI khi mua sắm (Vietnam Report) thay cho 900 triệu người dùng ChatGPT toàn cầu.
- Chỉ lấy từ tổ chức phát hành gốc (Google, Meta, OpenAI, Pew, Gartner, McKinsey, Bain, AppsFlyer, Adjust, Sensor Tower, Metric, DataReportal, e-Conomy SEA, văn bản luật...). Không dùng trang tổng hợp số liệu.
- Trước khi viết kịch bản phải mở link gốc kiểm tra lại con số (mạng đã mở từ 08/10/2026, không còn lý do chỉ đối chiếu qua báo). Trang tổng hợp hay trích sai hoặc dùng số cũ: ví dụ Baymard ghi trung bình 14.88 ô nhập ở trang thanh toán, nhiều trang trích lại thành 11.3. Số cũ, số nước ngoài, mẫu nhỏ thì nói rõ trên video. Nội dung pháp lý nên nhờ luật sư duyệt.
- Ghi nguồn trên mỗi biểu đồ.

## Lịch và đăng

- Mỗi ngày 1 video, từ 07/10/2026. Giờ đăng gợi ý: thứ Hai đến thứ Sáu 12:00, thứ Bảy và Chủ nhật 09:00; lỡ khung thì 20:00. Sau 2 đến 3 tuần, chỉnh theo giờ người theo dõi hoạt động trong TikTok Analytics.
- Mỗi video phải có nhiều insight hay: 3 đến 4 số liệu mạnh, mỗi số liệu kèm ý nghĩa với doanh nghiệp (vì sao nên quan tâm), không nhồi số cho đủ.
- Hashtag: luôn mở đầu bằng `#adtekagency #growthmarketing` (render.mjs tự thêm nếu thiếu), sau đó 3 đến 4 hashtag hợp với nội dung video. Không dùng `#adtek`.
- Anh Tin đăng tay, chèn nhạc từ Commercial Music Library của TikTok: Original 100%, Sound khoảng 15%.
- Slot trống trong lịch: Claude tự chọn chủ đề đang được quan tâm khi viết kịch bản thứ Bảy (tin tức, báo cáo 1 đến 2 tháng gần đây, sự kiện theo mùa). Không dùng Creator Search Insights.

## Giọng đọc

- Giọng "Tin Le v1" (Professional Voice Clone, giọng miền Nam), model Eleven v4. Nếu giọng chưa được huấn luyện cho v4, `voice.mjs` sẽ dừng; khi đó chạy lại với `--skip-check` để dùng v4 như hiện tại (anh Tin đã đồng ý). Không đổi sang model khác.
- Tốc độ đọc 1.1x (mặc định trong `voice.mjs`, đổi bằng ELEVENLABS_SPEED). Eleven v4 bỏ qua tham số speed nên giọng được tăng nhịp bằng atempo sau khi tạo. Với 1.1x, khoảng 3 chữ mỗi giây: video 50 đến 65 giây cần khoảng 150 đến 190 chữ lời đọc.
- Từ máy đọc sai thêm vào `tools/pronunciation.json`.

## Quy trình hằng tuần (Routine tự chạy, giờ Việt Nam)

- Thứ Bảy 08:47: viết kịch bản các video (mỗi ngày 1 video) từ Chủ nhật đến hết Chủ nhật tuần sau, chụp ảnh duyệt, email hi@tinle.co tiêu đề "[Adtek TikTok] Kịch bản tuần ..., chờ duyệt".
- Chủ nhật 08:52: đọc phản hồi trong thread đó, sửa theo góp ý (chưa có phản hồi thì sản xuất luôn), tạo giọng, chạy `tools/check.mjs`, xuất video, đưa lên trang hub https://claude.ai/artifact/72zNCsPigyqbV6P8kQtji5 (video là asset của trang, danh sách ở `hub/videos.json`), email "[Adtek TikTok] Video tuần ... đã xong" kèm link hub.
- Mỗi ngày 07:47: email "[Adtek TikTok] Nhắc đăng hôm nay ..." kèm giờ đăng gợi ý của ngày, link hub, caption copy sẵn, cấu hình nhạc.
- Trang hub có 4 mục (Video, Lịch đăng, Kịch bản, SOP). Sau mỗi thay đổi lịch hoặc kịch bản: chạy `python3 tools/hub_export.py` trong thư mục video rồi publish lại hub với files videos.json, schedule.json, scripts.json. Kịch bản mới có thêm trường "date" và "status".
- Không gửi video qua Google Drive hay đính kèm email (file quá lớn để tải lên qua công cụ); luôn dùng trang hub.
- Email gửi anh Tin: súc tích, chuyên nghiệp, không xưng anh/em, không dùng ký tự "—".
