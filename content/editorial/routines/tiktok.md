# Routine: Video TikTok Adtek (phương án B, hộp nháp)

Anh Tin chọn ngày 17/10/2026: script đẩy video vào hộp nháp (inbox) của tài khoản TikTok Adtek, anh Tin bấm thông báo trong app, dán caption, bật nhãn "Nội dung do AI tạo" (giọng đọc nhân bản bằng ElevenLabs), rồi bấm Đăng. Không dùng Direct Post: Content Sharing Guidelines của TikTok không duyệt công cụ chỉ đăng lên tài khoản do chính mình quản lý. Song song đang so sánh công cụ trung gian (phương án C) để chuyển sang tự động 100%.

Lịch video: danh sách `tiktok` trong `calendar.json` (3 video/tuần, phiên Adtek - Marketing lập). Kịch bản `video/scripts/<slug bài blog>/<part>.json`, giọng `video/tools/voice.mjs`, dựng `video/tools/render.mjs` (xem `video/README.md`). Công cụ đẩy video: `tools/tiktok_post.py`.

## Cài đặt một lần (anh Tin)

1. Tạo ứng dụng trên developers.tiktok.com, thêm sản phẩm Login Kit và Content Posting API, xin scope `user.info.basic` và `video.upload`. Redirect URI trong Login Kit: `https://adtek.agency/`.
2. Gửi ứng dụng cho TikTok duyệt (App review). Trong lúc chờ, thêm tài khoản TikTok Adtek vào danh sách Target Users (sandbox) để thử.
3. Trên máy anh Tin: đặt `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET` rồi chạy `python3 tools/tiktok_post.py auth`, mở link, bấm Cho phép, dán lại địa chỉ trang adtek.agency vừa mở ra. Script in refresh token (hạn 365 ngày) trên máy anh Tin.
4. Lưu `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, `TIKTOK_REFRESH_TOKEN` vào cài đặt môi trường cloud (Network secrets hoặc biến môi trường). Không dán vào chat.
5. Mở phiên mới, chạy `python3 tools/tiktok_post.py check`: phải ra đúng tên tài khoản TikTok Adtek.

## Mỗi video

1. Trước ngày đăng: kịch bản, giọng, dựng video (`show <id>` liệt kê việc còn thiếu). Thư mục `video/out/` không nằm trong git, phiên đẩy video phải dựng lại nếu chưa có file.
2. Đến giờ: `python3 tools/tiktok_post.py due`, mỗi video không còn problems thì `upload <id>`. Gửi anh Tin push notification "Video TikTok <id> đã vào hộp nháp" và tin nhắn trong phiên chứa nguyên caption để dán.
3. Sau khi anh Tin đăng: `status <id>` (TikTok trả PUBLISH_COMPLETE thì status = posted) hoặc `posted <id>` khi anh Tin báo đã đăng.
4. Kết quả có `refresh_token_rotated: true`: báo anh Tin cập nhật `TIKTOK_REFRESH_TOKEN` (bản mới đã lưu tạm ở `~/.config/adtek/tiktok_refresh_token`, chỉ còn trong phiên hiện tại).

Giới hạn TikTok: tối đa 5 video chờ trong hộp nháp mỗi 24 giờ, 6 lượt gọi mỗi phút. Caption không có link (để link ở bio).

Lịch tự động chưa tạo: chờ có khóa TikTok (bước 4) và kịch bản video đầu tiên.
