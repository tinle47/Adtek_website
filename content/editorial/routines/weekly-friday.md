# Routine: Blog Adtek: viết 2 bài tuần tới

- Lịch: `CRON_TZ=Asia/Ho_Chi_Minh 52 8 * * 5` (8:52 sáng thứ Sáu, giờ Việt Nam), viết tối đa 4 bài cho các ngày đăng trong 14 ngày tới
- Gắn vào phiên **Adtek - Blog post** (session_01AvYySKMdJYRoHxp3DYBUqB) để anh Tin duyệt bài ngay trong phiên đó. Ảnh do phiên **Adtek - Designer** làm; đăng Facebook chạy ở phiên **Adtek - Facebook post** (session_0196UuuQJu6Edu8fi8VXJDzh).

## Prompt

Cập nhật 16/10/2026 (phiên Adtek - Marketing, anh Tin cho phép): 4 bài/tuần theo lịch tháng, bỏ phần Facebook.

[Lịch tự động thứ Sáu: viết bài blog Adtek]
Làm theo content/editorial/README.md và content/editorial/calendar.json trong repo Adtek_website (branch claude/brave-curie-2c6zbc, pull bản mới nhất trước). Lịch do phiên Adtek - Marketing lập mỗi tháng: không đổi date, time, tiêu đề hay từ khóa của bài; thấy cần đổi thì nêu trong tin nhắn gửi anh Tin.
1. Liên kết ngược và tối ưu SEO sau khi đăng do phiên Adtek - SEO làm (lịch thứ Hai, Ba, Năm, Sáu 21:43, content/editorial/routines/seo-after-publish.md), không làm ở đây. Chỉ kiểm tra: nếu còn bài đã qua ngày giờ đăng mà chưa có seo_optimized trong calendar.json, nêu trong tin nhắn gửi anh Tin ở bước 3c.
2. Chọn tối đa 4 bài status "planned" có ngày đăng sớm nhất trong 14 ngày tới (không có bài nào thì báo anh Tin một dòng rồi dừng). Với mỗi bài: đọc trường brief nếu có, nghiên cứu nguồn mới nhất (có thể tham khảo phần nghiên cứu trong reports/chien-luoc-noi-dung.html), viết HTML khoảng 2,000 chữ vào content/posts/<slug>.html theo đúng quy tắc trong README (dùng skill anti-ai-writing, không dùng ký tự gạch dài, số theo định dạng US, ít nhất 3 nguồn uy tín có tháng/năm, link trụ cột và links_to chỉ tới bài đã đăng hoặc đã đặt lịch đăng trước bài này, link thuật ngữ, một phần dùng được ngay là khung, checklist hoặc bảng tính, không viết mini-case hay số liệu dự án, CTA /contact/), điền slug, seo_title, meta_desc, cover (kicker, title, subtitle, chips cho ảnh bìa blog; hero là một con số có trong bài, hero_text là câu đọc liền sau con số đó), summary (2 đến 3 câu tóm tắt), confirm (danh sách điểm cần anh xác nhận, có thể rỗng) vào calendar.json. Không viết fb_caption, fb_title, fb_hashtags, fb_comment: từ bài 7, Facebook có lịch riêng, không đăng lại bài blog. Chạy python3 tools/blog_post.py draft <số bài> (tự gắn nofollow cho link ra ngoài). Ảnh bìa blog (content/posts/<slug>-cover.jpg) do phiên Adtek - Designer làm và push lên nhánh; pull để lấy ảnh, xem ảnh trước khi gửi duyệt, nếu chưa có thì báo anh Tin.
3. Nhắc anh Tin duyệt qua 3 kênh:
   a. Email: trong thư mục tools chạy python3 approval_email.py --mark <các số bài> (ghi thời điểm gửi để tính hạn D+1), lấy JSON in ra và gửi to, subject, body, htmlBody nguyên văn bằng công cụ gửi Gmail.
   b. Push notification (PushNotification, dưới 200 ký tự), ví dụ: "4 bài blog chờ duyệt trước <hạn>: <tên ngắn từng bài>. Quá hạn sẽ tự đặt lịch đăng."
   c. Tin nhắn trong phiên này với cùng nội dung, link xem trước và hạn duyệt.
4. Hẹn kiểm tra hạn D+1: gọi send_later với at = giá trị deadline trong JSON ở bước 3a (đổi sang RFC3339), name "Hạn duyệt blog bài <các số bài>", message: "[Hạn duyệt D+1] Pull branch claude/brave-curie-2c6zbc, chạy python3 tools/blog_post.py auto. Với mỗi bài trong auto_scheduled: gửi email tới hi@tinle.co (tiêu đề '[Adtek Blog] Đã tự đặt lịch bài <số>: đăng <ngày giờ>', kèm link xem trước mới tạo bằng tools/approval_email.py và cách hủy: nhắn 'hủy bài X' trước giờ đăng); gửi push notification; ghi changelog, commit, push lên claude/brave-curie-2c6zbc và đồng bộ sang claude/determined-faraday-hhy1ol. Nếu auto_scheduled rỗng thì không gửi gì."
5. Ghi logs/changelog.md, commit, push lên claude/brave-curie-2c6zbc và đồng bộ sang claude/determined-faraday-hhy1ol (git push origin claude/brave-curie-2c6zbc:claude/determined-faraday-hhy1ol).
Khi anh Tin trả lời:
- "duyệt bài X": chạy python3 tools/blog_post.py schedule X (WordPress đăng đúng ngày giờ trong lịch). Không hẹn đăng Facebook cho bài từ 7 trở đi.
- Yêu cầu sửa: chạy python3 tools/blog_post.py changes X, sửa xong gửi lại email với --mark và hẹn send_later D+1 mới.
- "hủy bài X": chạy python3 tools/blog_post.py unschedule X; nếu calendar.json có fb_trigger (chỉ bài 1 đến 6) thì xóa lịch đó bằng delete_trigger, xóa fb_scheduled và fb_trigger; báo phiên Adtek - Marketing (session_01XqVohyrjLRctpapS6FbMXD) để xếp lại lịch.

## Hẹn đăng Facebook (chỉ bài 1 đến 6, cách cũ)

Dùng khi một bài blog vừa được đặt lịch (anh Tin duyệt hoặc tự duyệt D+1). Việc đăng Facebook chạy ở phiên Adtek - Facebook post, nên gọi create_trigger (không dùng send_later) với:

- persistent_session_id: "session_0196UuuQJu6Edu8fi8VXJDzh" (phiên Adtek - Facebook post)
- run_once_at: ngày giờ đăng blog của bài (date và time trong calendar.json, giờ Việt Nam +07:00) cộng 5 phút, dạng RFC3339.
- name: "Đăng Facebook bài X"
- initiation: "human_schedule"
- prompt: "[Đăng Facebook bài X] Pull branch claude/brave-curie-2c6zbc, chạy python3 tools/fb_post.py post X (script tự kiểm tra blog đã lên sóng, token đúng Page và đã có ảnh content/posts/<slug>-fb.jpg từ phiên Adtek - Designer; nếu bài đã bị hủy thì script dừng, chỉ báo lại). Thành công: gửi anh Tin link bài Facebook qua push notification và tin nhắn trong phiên, ghi changelog, commit, push lên claude/brave-curie-2c6zbc và đồng bộ sang claude/determined-faraday-hhy1ol. Lỗi: báo anh Tin nguyên văn lỗi, không thử cách khác; nếu bình luận link bị chặn thì tạm hoãn các lịch đăng Facebook còn lại cho tới khi anh trả lời."

Sau đó ghi fb_scheduled (ngày giờ đăng Facebook) và fb_trigger (trigger_id trả về) vào calendar.json, fb_status = "scheduled". Khi hủy bài, xóa lịch bằng delete_trigger với fb_trigger (cùng tài khoản nên phiên nào cũng xóa được).
