# Quy trình nội dung blog

Lịch đăng, cụm chủ đề và danh sách bài nằm trong `calendar.json`.

## Nhịp đăng

- 2 bài/tuần, mỗi bài khoảng 2,000 chữ, đăng 8:00 sáng Thứ Ba và Thứ Năm.
- Mỗi bài cần có một phần chỉ Adtek viết được: mini-case ẩn danh, số liệu từ dự án, khung hoặc checklist dùng ngay.
- Tác giả Tin Le, có SEO title, meta description và ảnh bìa.

## Quy trình viết và duyệt

1. Thứ Sáu hằng tuần (lịch tự động 8:52 sáng): viết 2 bài `planned` có ngày đăng sớm nhất, đưa lên WordPress ở dạng nháp bằng `python3 tools/blog_post.py draft <số bài>`, nhắc anh Tin duyệt qua email (hi@tinle.co), push notification và tin nhắn trong phiên Claude Code.
2. Anh Tin duyệt từng bài. Chỉ sau khi được duyệt mới chạy `python3 tools/blog_post.py schedule <số bài>` để WordPress tự đăng đúng ngày giờ trong lịch.
3. Cũng trong lần chạy thứ Sáu: làm liên kết ngược cho các bài đã lên sóng trong tuần.
4. Ngày 1 hằng tháng (lịch tự động 8:47 sáng): rà soát và cập nhật nội dung, gửi báo cáo qua email, push notification và tin nhắn trong phiên.

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

Ngay sau khi bài lên sóng (liên kết ngược):

- Thêm link từ bài trụ cột của cụm về bài mới.
- Thêm link từ 2 đến 3 bài đã đăng có trong `links_to` của bài mới, hoặc có `links_to` trỏ tới bài mới.
- Không bài nào được ở trạng thái "mồ côi" (không có link nội bộ nào trỏ vào).

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
