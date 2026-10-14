# Routine: Blog Adtek: viết 2 bài tuần tới

- Lịch: `CRON_TZ=Asia/Ho_Chi_Minh 52 8 * * 5` (8:52 sáng thứ Sáu, giờ Việt Nam)
- Chạy trong cùng một phiên (persistent session) để anh Tin duyệt bài ngay trong phiên đó.

## Prompt

[Lịch tự động thứ Sáu: viết bài blog Adtek]
Làm theo content/editorial/README.md và content/editorial/calendar.json trong repo Adtek_website (branch claude/brave-curie-2c6zbc, pull bản mới nhất trước).
1. Liên kết ngược: với mỗi bài status "scheduled" mà ngày đăng đã qua, đổi status thành "published", điền published, rồi chèn link từ bài trụ cột của cụm và 2 đến 3 bài đã đăng liên quan về bài đó (backup nội dung cũ vào content/backups trước khi sửa). Thêm link vào các bài đã đăng có links_to trỏ tới bài này.
2. Chọn 2 bài status "planned" có ngày đăng sớm nhất. Với mỗi bài: nghiên cứu nguồn mới nhất, viết HTML khoảng 2,000 chữ vào content/posts/<slug>.html theo đúng quy tắc trong README (dùng skill anti-ai-writing, không dùng ký tự gạch dài, số theo định dạng US, ít nhất 3 nguồn uy tín có tháng/năm, link trụ cột và links_to chỉ tới bài đã đăng, link thuật ngữ, CTA /contact/), điền slug, seo_title, meta_desc, cover, summary (2 đến 3 câu tóm tắt), confirm (danh sách điểm cần anh xác nhận, có thể rỗng), fb_caption (bài đăng Facebook 150 đến 200 chữ, kể chuyện bằng một tình huống hoặc con số cụ thể có trong bài, không viết câu mời xem bài vì tools/fb_post.py tự thêm CTA ở đầu, không emoji, không link trong nội dung) và fb_comment (tiêu đề ngắn + link https://adtek.agency/<slug>/) vào calendar.json, chạy python3 tools/blog_post.py draft <số bài> (tự gắn nofollow cho link ra ngoài) và python3 tools/fb_post.py cover <số bài> (ảnh 4:5 cho Facebook). Xem ảnh bìa và ảnh Facebook trước khi tải lên.
3. Nhắc anh Tin duyệt qua 3 kênh:
   a. Email: trong thư mục tools chạy python3 approval_email.py --mark <số bài A> <số bài B> (ghi thời điểm gửi để tính hạn D+1), lấy JSON in ra và gửi to, subject, body, htmlBody nguyên văn bằng công cụ gửi Gmail. Email có hạn duyệt, ảnh bìa, ngày giờ đăng, tóm tắt, điểm cần xác nhận, bài đăng Facebook đi kèm, nút "Xem trước bài viết" (không cần đăng nhập) và "Sửa trên WordPress".
   b. Push notification (PushNotification, dưới 200 ký tự), ví dụ: "2 bài blog chờ duyệt trước <hạn>: <tên ngắn bài A>, <tên ngắn bài B>. Quá hạn sẽ tự đặt lịch đăng."
   c. Tin nhắn trong phiên này với cùng nội dung, link xem trước và hạn duyệt.
4. Hẹn kiểm tra hạn D+1: gọi send_later với at = giá trị deadline trong JSON ở bước 3a (đổi sang RFC3339), name "Hạn duyệt blog bài <A>, <B>", message: "[Hạn duyệt D+1] Pull branch claude/brave-curie-2c6zbc, chạy python3 tools/blog_post.py auto. Với các bài trong auto_scheduled: gửi email tới hi@tinle.co (tiêu đề '[Adtek Blog] Đã tự đặt lịch bài <số>: đăng <ngày giờ>', kèm link xem trước mới tạo bằng tools/approval_email.py và cách hủy: nhắn 'hủy bài X' trước giờ đăng), gửi push notification, ghi changelog, commit và push. Nếu auto_scheduled rỗng thì không gửi gì."
5. Ghi logs/changelog.md, commit và push.
Khi anh Tin trả lời: "duyệt bài X" thì chạy tools/blog_post.py schedule X; yêu cầu sửa thì chạy tools/blog_post.py changes X, sửa xong gửi lại email với --mark và hẹn send_later mới; "hủy bài X" thì chạy tools/blog_post.py unschedule X.
