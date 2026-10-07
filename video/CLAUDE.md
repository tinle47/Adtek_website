# Quy tắc làm video TikTok Adtek

Kênh @adtek.growth.marketing (Adtek Growth Marketing Agency). Các quy tắc dưới đây do anh Tin chốt, áp dụng cho mọi video. Chi tiết kỹ thuật xem `README.md`, lịch và nguồn số liệu xem `plan/lich-noi-dung-tiktok.xlsx`.

## Nội dung

- Kênh TikTok độc lập với website: mỗi video một chủ đề riêng, không dẫn về blog, không đặt link trong caption.
- Bám dịch vụ Adtek: Digital Marketing, Growth Marketing, App Marketing, SEO, AIO, Performance Marketing. Ưu tiên chủ đề đang trend, có nhu cầu tìm kiếm.
- Mỗi video khoảng 1 phút (50 đến 65 giây), 6 cảnh: câu hỏi mở đầu, 3 đến 4 cảnh số liệu, 1 cảnh "làm gì ngay", cảnh Follow.
- Câu đầu tiên của lời đọc là một câu hỏi khơi tò mò.
- Chỉ giữ ý mạnh, số liệu ấn tượng. Một chủ đề làm thành một video, không tách nhỏ thành nhiều video.
- Cảnh cuối dùng `follow`, lời đọc kết bằng "Follow Adtek để xem số liệu marketing mới mỗi ngày."

## Chọn biểu đồ theo kiểu dữ liệu

- 1 con số gây sốc: `bignumber`. 2 con số đối đầu: `versus`. Trước và sau của vài nhóm: `slope`. Xu hướng từ 3 mốc: `trend`. Chia phần trong tổng: `donut`. "x trên 10 người": `people`, "x trên 100": `waffle`. Rơi rụng qua từng bước: `funnel`. Xếp hạng từ 3 mục: `hbars`. So sánh 2 đến 4 nhóm: `columns`. Việc cần làm: `list`.
- Mỗi video dùng ít nhất 3 loại biểu đồ khác nhau, không dùng cùng một loại cho 2 cảnh liền nhau. Video liền kề trong lịch nên mở đầu bằng loại biểu đồ khác nhau.
- Không bóp méo dữ liệu cho đẹp: độ rộng, độ cao luôn đúng tỷ lệ; trục không bắt đầu từ 0 thì ghi rõ.

## Viết tiếng Việt tự nhiên

- Viết như người Việt nói, không dịch thẳng từ tiếng Anh. Áp dụng cho lời đọc, tiêu đề, nhãn biểu đồ, chú thích, dòng nguồn và caption.
- Đọc to lên, câu nào nghe như văn bản dịch thì viết lại. Ví dụ: "lọc bạn" → "so sánh bạn", "danh sách lọc" → "lọt vào danh sách", "hành trình mua" → "cách khách hàng mua hàng", "hệ sinh thái" → "doanh nghiệp lớn ở gần", "ổn định chính trị" → "chính trị ổn định", "người mua B2B" → "khách hàng doanh nghiệp".
- Tránh từ sáo rỗng: đóng vai trò quan trọng, bứt phá, giải pháp toàn diện, hành trình, kỷ nguyên, chìa khóa thành công, trong bối cảnh hiện nay.
- Không dùng ký tự "—". Số viết theo US format (75,000; 0.61%).

## Số liệu

- Chỉ lấy từ tổ chức phát hành gốc (Google, Meta, OpenAI, Pew, Gartner, McKinsey, Bain, AppsFlyer, Adjust, Sensor Tower, Metric, DataReportal, e-Conomy SEA, văn bản luật...). Không dùng trang tổng hợp số liệu.
- Trước khi viết kịch bản phải mở link gốc kiểm tra lại con số. Số cũ, số nước ngoài, mẫu nhỏ thì nói rõ trên video. Nội dung pháp lý nên nhờ luật sư duyệt.
- Ghi nguồn trên mỗi biểu đồ.

## Lịch và đăng

- Mỗi ngày 1 video, từ 09/10/2026. Giờ đăng gợi ý: thứ Hai đến thứ Sáu 12:00, thứ Bảy và Chủ nhật 09:00; lỡ khung thì 20:00. Sau 2 đến 3 tuần, chỉnh theo giờ người theo dõi hoạt động trong TikTok Analytics.
- Mỗi video phải có nhiều insight hay: 3 đến 4 số liệu mạnh, mỗi số liệu kèm ý nghĩa với doanh nghiệp (vì sao nên quan tâm), không nhồi số cho đủ.
- Anh Tin đăng tay, chèn nhạc từ Commercial Music Library của TikTok: Original 100%, Sound khoảng 15%.
- Slot trống trong lịch: Claude tự chọn chủ đề đang được quan tâm khi viết kịch bản thứ Bảy (tin tức, báo cáo 1 đến 2 tháng gần đây, sự kiện theo mùa). Không dùng Creator Search Insights.

## Giọng đọc

- Giọng "Tin Le v1" (Professional Voice Clone, giọng miền Nam), model Eleven v4. Nếu giọng chưa được huấn luyện cho v4, `voice.mjs` sẽ dừng; khi đó chạy lại với `--skip-check` để dùng v4 như hiện tại (anh Tin đã đồng ý). Không đổi sang model khác.
- Tốc độ đọc 1.1x (mặc định trong `voice.mjs`, đổi bằng ELEVENLABS_SPEED). Eleven v4 bỏ qua tham số speed nên giọng được tăng nhịp bằng atempo sau khi tạo. Với 1.1x, khoảng 3 chữ mỗi giây: video 50 đến 65 giây cần khoảng 150 đến 190 chữ lời đọc.
- Từ máy đọc sai thêm vào `tools/pronunciation.json`.

## Quy trình hằng tuần (Routine tự chạy, giờ Việt Nam)

- Thứ Bảy 08:47: viết kịch bản các video (mỗi ngày 1 video) từ Chủ nhật đến hết Chủ nhật tuần sau, chụp ảnh duyệt, email hi@tinle.co tiêu đề "[Adtek TikTok] Kịch bản tuần ..., chờ duyệt".
- Chủ nhật 08:52: đọc phản hồi trong thread đó, sửa theo góp ý (chưa có phản hồi thì sản xuất luôn), tạo giọng, xuất video, đưa lên trang hub https://claude.ai/artifact/72zNCsPigyqbV6P8kQtji5 (video là asset của trang, danh sách ở `hub/videos.json`), email "[Adtek TikTok] Video tuần ... đã xong" kèm link hub.
- Mỗi ngày 07:47: email "[Adtek TikTok] Nhắc đăng hôm nay ..." kèm giờ đăng gợi ý của ngày, link hub, caption copy sẵn, cấu hình nhạc.
- Trang hub có 4 mục (Video, Lịch đăng, Kịch bản, SOP). Sau mỗi thay đổi lịch hoặc kịch bản: chạy `python3 tools/hub_export.py` trong thư mục video rồi publish lại hub với files videos.json, schedule.json, scripts.json. Kịch bản mới có thêm trường "date" và "status".
- Không gửi video qua Google Drive hay đính kèm email (file quá lớn để tải lên qua công cụ); luôn dùng trang hub.
- Email gửi anh Tin: súc tích, chuyên nghiệp, không xưng anh/em, không dùng ký tự "—".
