# Routine: Video TikTok Adtek (đăng qua Zernio)

Anh Tin chọn ngày 17/10/2026: đăng tự động qua Zernio (zernio.com, gói miễn phí cho 2 tài khoản) lên @adtek.growth.marketing. Script tải video và cover lên Zernio rồi hẹn giờ; đến giờ Zernio đăng công khai, gắn nhãn "Nội dung do AI tạo" (giọng đọc nhân bản bằng ElevenLabs). Không dùng Direct Post bằng ứng dụng TikTok riêng: Content Sharing Guidelines của TikTok không duyệt công cụ chỉ đăng lên tài khoản do chính mình quản lý. Phương án dự phòng B (đẩy vào hộp nháp, anh Tin tự bấm Đăng) vẫn có trong script: lệnh `auth`, `upload`, `inbox-status`.

## Ai làm gì (anh Tin chọn 17/10/2026)

| Việc | Phiên | Nơi ghi |
|---|---|---|
| Lịch TikTok (1 video mỗi ngày, lấy lịch của Video production làm chuẩn): ngày, giờ, chủ đề | Adtek - Marketing (session_01XqVohyrjLRctpapS6FbMXD) | danh sách `tiktok` trong `content/editorial/calendar.json` |
| Kịch bản, giọng, xuất video, cover, đưa lên hub | Adtek - Video production (session_015wnXjaRHuK6RciQ3JeDviz), lịch tự động ở phiên Adtek - TikTok lịch tự động (session_01RJbeQ6L8V6bz5xR8mWeYGP) | `video/` và `video/hub/videos.json` trên nhánh `claude/confident-ramanujan-t3jbi6`, hub https://claude.ai/artifact/YAeKXQbpBZj26HyPKV5wxN |
| Hẹn đăng, theo dõi, báo link | Adtek - Tiktok post (session_01XZK48jTG9DpqHxwCKxGbA6) | trường `status`, `zernio_post_id`, `tiktok_url` của mục `tiktok` |

Mỗi mục `tiktok`: `id` (tt-YYYYMMDD), `date`, `time`, `topic`, `scripts` (slug video trên hub), `status`. Status do Marketing và Video production ghi: proposed, scripted, video_ready; phiên Tiktok post ghi tiếp: scheduled, posted, cancelled, failed. Phiên Tiktok post không đổi `date`, `time`, `topic`.

Cài đặt đăng mặc định (`TIKTOK_SETTINGS` trong script): công khai, cho bình luận, Duet, Stitch (tự tắt mục nào tài khoản đã tắt trong app), nhãn AI bật, không bật nhãn quảng cáo, cover lấy từ hub (trường `cover`; không có thì TikTok lấy khung giây thứ 1). Caption = `caption` + `hashtags` trên hub, không link (link để ở bio). Chưa thêm nhạc nền qua API.

## Cài đặt một lần (anh Tin)

1. Tài khoản TikTok Adtek công khai, kết nối Zernio qua TikTok Business (đã xong 17/10/2026).
2. Tạo API key mới trong Zernio, lưu vào cài đặt môi trường cloud với tên `ZERNIO_API_KEY` (Network secrets hoặc biến môi trường), xóa key cũ đã lộ trong chat. Không dán vào chat.
3. Mở phiên mới, chạy `python3 tools/tiktok_post.py check`: phải ra Adtek Growth Marketing Agency, có `PUBLIC_TO_EVERYONE`.

## Mỗi video

1. `git fetch origin claude/confident-ramanujan-t3jbi6` (script đọc `video/hub/videos.json` từ nhánh này), rồi `python3 tools/tiktok_post.py week <hôm nay>`.
2. Video có `video_asset`: tải video và cover bằng Artifact read (url hub, path = mã asset), chép vào `video/out/<slug>.mp4` và `video/out/<slug>-cover.png`. `show <id>` liệt kê việc còn thiếu.
3. Báo trước và hẹn giờ (trong 24 giờ trước giờ đăng): `schedule <id>`. Gửi anh Tin video (SendUserFile), caption, push notification "Video TikTok <giờ>: <topic>. Không nhắn hủy thì Zernio đăng đúng giờ."
4. Anh Tin nhắn "hủy <id>": `cancel <id>` (xóa lịch trên Zernio). Sửa caption: phiên Video production sửa trên hub, rồi `cancel <id>`, đổi status về `video_ready`, `schedule <id>` lại.
5. Sau giờ đăng khoảng 30 phút: `status <id>`. Đã đăng: push notification kèm `tiktok_url`. `failed`: báo anh Tin nguyên văn `fail_reason`, không thử cách khác.
6. Ghi `logs/changelog.md`, commit, push.

Giới hạn: TikTok tối đa 15 video mỗi 24 giờ cho mỗi tài khoản; Zernio gói miễn phí 60 lượt gọi mỗi phút; bản tải lên Zernio giữ 7 ngày.

Lịch tự động chưa tạo: chờ `ZERNIO_API_KEY` trong môi trường và anh Tin quyết định thay lượt "nhắc đăng tay 07:47" của phiên Video production bằng đăng tự động.
