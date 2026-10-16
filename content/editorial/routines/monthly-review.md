# Routine: Blog Adtek: rà soát nội dung hằng tháng

- Lịch: `CRON_TZ=Asia/Ho_Chi_Minh 47 8 1 * *` (8:47 sáng ngày 1 hằng tháng, giờ Việt Nam)
- Chạy trong cùng phiên với routine thứ Sáu: phiên **Adtek - Blog post** (session_01AvYySKMdJYRoHxp3DYBUqB).

## Prompt

[Lịch tự động ngày 1: rà soát nội dung blog Adtek]
Làm theo mục "Quy trình cập nhật nội dung" trong content/editorial/README.md, repo Adtek_website (branch claude/brave-curie-2c6zbc, pull bản mới nhất trước).
1. Lấy các bài đến hạn rà soát trong calendar.json (cả posts và existing) theo hạng A/B/C/S và last_reviewed hoặc ngày đăng.
2. Với mỗi bài: đối chiếu số liệu, điều luật, tính năng nền tảng, tên sản phẩm với nguồn mới nhất; kiểm tra link hỏng nội bộ và bên ngoài; kiểm tra bài mồ côi (không có link nội bộ trỏ vào).
3. Sửa nhỏ (số liệu, link hỏng, tên tính năng): backup vào content/backups, sửa trực tiếp, thêm dòng "Cập nhật ngày ..." đầu bài, cập nhật last_reviewed. Sửa lớn (nhận định chính sai, cần viết lại): soạn bản cập nhật trong content/posts, chưa đăng, chờ anh duyệt. Link ra ngoài luôn có rel="nofollow noopener".
4. Xử lý tối đa 2 mục trong danh sách existing có action cập nhật lớn hoặc gộp bài (ưu tiên 2215 vì là trụ cột C5, rồi 3073); gộp bài thì dùng chuyển hướng 301. Đây là sửa lớn nên soạn sẵn và chờ duyệt.
5. Ghi logs/changelog.md, commit và push.
6. Gửi anh Tin báo cáo ngắn (số bài đã rà, những gì đã sửa kèm link, bản cập nhật lớn đang chờ duyệt, rủi ro cần lưu ý) qua 3 kênh: email tới hi@tinle.co bằng Gmail, tiêu đề "[Adtek Blog] Báo cáo rà soát nội dung tháng <tháng>", nội dung tiếng Việt có dấu; push notification (PushNotification, dưới 200 ký tự, nêu số bản cập nhật chờ duyệt); và tin nhắn trong phiên này.
