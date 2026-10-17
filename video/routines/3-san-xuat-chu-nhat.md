Tên: TikTok Adtek: sản xuất video (Chủ nhật)
Lịch: CRON_TZ=Asia/Ho_Chi_Minh 52 8 * * 0
Nội dung gửi vào phiên mỗi lần chạy (chép nguyên văn phần dưới đường kẻ):

---
[Lịch Chủ nhật] Sản xuất các video TikTok đã viết kịch bản hôm qua và email báo anh Tin (hi@tinle.co).

Chuẩn bị: repo tinle47/Adtek_website, nhánh claude/confident-ramanujan-t3jbi6 (fetch, checkout, pull). Đọc lại video/CLAUDE.md (đặc biệt "Khung mở đầu chữ to", "Giọng đọc là đồng hồ" và "Đa dạng dạng video"). cd video && npm install nếu thiếu.

Các bước:
1. Tìm trong Gmail thread "[Adtek TikTok] Kịch bản tuần" gửi hôm qua, đọc toàn bộ phản hồi của anh Tin (get_thread). Có chỉnh sửa thì sửa kịch bản tương ứng, vẫn giữ đúng quy tắc trong CLAUDE.md. Chưa có phản hồi thì sản xuất luôn theo kịch bản đã gửi.
2. Các video cần làm: dòng trong video/plan/lich-noi-dung-tiktok.xlsx có trạng thái "Đã viết kịch bản" và ngày đăng từ hôm nay trở đi. Video có ngày đăng hôm nay (đăng lúc 09:00) làm trước. Kịch bản nào (trừ chữ động) thiếu trường "hook" thì thêm theo quy tắc trong CLAUDE.md.
3. Tạo giọng: node tools/voice.mjs <slug>. Nếu script báo giọng "Tin Le v1" chưa được huấn luyện cho Eleven v4, chạy lại với --skip-check để dùng giọng v4 như hiện tại (anh Tin đã đồng ý). Không đổi sang model khác.
4. Kiểm tra bằng máy: REMOTION_BROWSER=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell node tools/check.mjs <slug>. FAIL phải sửa. WARN đứng hình quá 4 giây hoặc nhịp đọc quá 3.5 chữ/giây: sửa lời đọc hoặc bố cục nếu được (tạo lại giọng cho cảnh đã sửa), không được thì ghi lý do vào email.
5. Xuất video: node tools/render.mjs <slug> (cùng REMOTION_BROWSER). Kiểm tra độ dài (50 đến 65 giây) và âm lượng (-14 LUFS do render.mjs báo). Xem ảnh ghép 1 khung mỗi 2 giây của từng video để bắt lỗi hiển thị (ffmpeg fps=1/2, tile), và riêng khung đầu tiên: câu hook chữ to nằm gọn giữa màn hình, không rớt dòng xấu (sửa câu hook nếu cần).
6. Ảnh lướt: chọn 1 video nhiều số liệu nhất của tuần, chạy node tools/render.mjs <slug> --carousel, xem lại các ảnh.
7. Tải từng out/<slug>.mp4 và out/<slug>-cover.png (và các ảnh lướt) lên kho asset của trang hub (Artifact publish, url của hub, asset: true, file_paths), lấy url trả về. Thêm hoặc cập nhật mục tương ứng trong video/hub/videos.json (slug, filename "<dd-mm> <chủ đề không dấu>", date YYYY-MM-DD, service, topic có ghi dạng video, hook, duration, url, cover, caption, hashtags, note rỗng; video có ảnh lướt thêm "carousel": [url các ảnh theo thứ tự]). Đổi "status" trong kịch bản và trạng thái trong file lịch thành "Đã có video", tính lại file lịch bằng soffice như quy trình thứ Bảy.
8. Cập nhật trang hub: trong thư mục video chạy python3 tools/hub_export.py, rồi publish lại hub (url của hub, file_path video/hub/index.html, files {"videos.json": "hub/videos.json", "schedule.json": "hub/schedule.json", "scripts.json": "hub/scripts.json", "samples.json": "hub/samples.json"} tính từ thư mục video). Commit (kịch bản, giọng trong public/voice, tools/pronunciation.json, hub/*.json, file lịch), push. Sau đó gửi tin (send_message của Claude Code Remote) tới phiên Adtek - Marketing (session_01XqVohyrjLRctpapS6FbMXD) và phiên Adtek - Tiktok post (session_01XZK48jTG9DpqHxwCKxGbA6): danh sách ngày, slug, video đã lên hub (để đổi status thành "video_ready" trong calendar.json và lên lịch đăng), kèm bộ ảnh lướt thuộc video nào. Phiên này không đăng video và không gửi email nhắc đăng; việc đăng do phiên Tiktok post làm qua Zernio.
9. Gửi email tới hi@tinle.co, tiêu đề "[Adtek TikTok] Video tuần <dd/mm> đến <dd/mm> đã xong". Súc tích, không xưng anh/em, không dùng "—". Gồm link trang hub (mục Video có nút tải video, ảnh bìa, ảnh lướt và copy caption), và với mỗi video: ngày đăng, dạng video, câu hook, độ dài, kết quả kiểm tra (đứng hình dài nhất), những chỗ đã sửa theo phản hồi. Ghi bộ ảnh lướt thuộc video nào (phiên Tiktok post lo việc đăng). Nếu đã dùng giọng v4 chưa huấn luyện thì ghi một dòng lưu ý.

Gặp lỗi không tự xử lý được thì vẫn gửi email báo rõ lỗi và phần đã xong.
