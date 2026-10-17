Trạng thái: TẮT từ 17/10/2026 (trig_01BRGsizN3tkDdo9LqKXFqZS). Anh Tin chốt: việc đăng video chuyển cho phiên Adtek - Tiktok post (đăng tự động qua Zernio), không gửi email nhắc đăng nữa. Giữ file này để tham khảo.

Tên: TikTok Adtek: nhắc đăng video (mỗi ngày)
Lịch: CRON_TZ=Asia/Ho_Chi_Minh 47 7 * * *
Nội dung gửi vào phiên mỗi lần chạy (chép nguyên văn phần dưới đường kẻ):

---
[Lịch nhắc đăng] Hôm nay là ngày đăng video TikTok. Gửi email nhắc anh Tin (hi@tinle.co).

Các bước:
1. Repo tinle47/Adtek_website, nhánh claude/confident-ramanujan-t3jbi6 (fetch, checkout, pull). Mở video/plan/lich-noi-dung-tiktok.xlsx và video/hub/videos.json, tìm video có ngày đăng là hôm nay (giờ Việt Nam).
2. Giờ đăng gợi ý: thứ Hai đến thứ Sáu 12:00 (giờ nghỉ trưa của chủ doanh nghiệp và dân văn phòng), thứ Bảy và Chủ nhật 09:00. Nếu lỡ khung đó thì đăng 20:00.
3. Gửi email tới hi@tinle.co, tiêu đề "[Adtek TikTok] Đăng hôm nay <thứ> <dd/mm> lúc <giờ>: <chủ đề>". Súc tích, không xưng anh/em, không dùng "—". Gồm: giờ đăng gợi ý, link trang hub (xem video/HANDOFF.md; video hôm nay nằm đầu mục Video, có nút Tải video và Copy caption), caption và hashtag copy sẵn ngay trong email (không có link trong caption), cấu hình nhạc khi đăng (Sounds: nhạc nhẹ không lời trong Commercial Music Library; Volume: Original 100%, Sound khoảng 15%).
4. Nếu video hôm nay chưa có (không có url trong hub/videos.json): nếu kịch bản đã có, tạo giọng (voice.mjs, thêm --skip-check nếu giọng chưa huấn luyện cho v4), xuất video, đưa lên hub như quy trình Chủ nhật, rồi gửi email nhắc như trên. Nếu chưa có kịch bản thì email báo rõ và hỏi anh muốn bỏ qua hay xử lý thế nào. Nếu hôm nay không có video trong lịch thì không gửi email.
5. Ghi "Đã nhắc" vào cuối cột "Lưu ý khi dùng" của dòng hôm nay (không đổi trạng thái sang "Đã đăng"). Trong thư mục video chạy python3 tools/hub_export.py, publish lại hub (url của hub, file_path video/hub/index.html, files {"videos.json": "hub/videos.json", "schedule.json": "hub/schedule.json", "scripts.json": "hub/scripts.json"}), commit, push.
