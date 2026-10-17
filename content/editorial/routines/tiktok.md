# Routine: Video TikTok Adtek (đăng qua Zernio)

Anh Tin chọn ngày 17/10/2026: đăng tự động qua Zernio (zernio.com, gói miễn phí cho 2 tài khoản) lên @adtek.growth.marketing. Script tải video và cover lên Zernio rồi hẹn giờ; đến giờ Zernio đăng công khai, gắn nhãn "Nội dung do AI tạo" (giọng đọc nhân bản bằng ElevenLabs). Không dùng Direct Post bằng ứng dụng TikTok riêng: Content Sharing Guidelines của TikTok không duyệt công cụ chỉ đăng lên tài khoản do chính mình quản lý. Phương án dự phòng B (đẩy vào hộp nháp, anh Tin tự bấm Đăng) vẫn có trong script: lệnh `auth`, `upload`, `inbox-status`.

## Ai làm gì (anh Tin chọn 17/10/2026)

| Việc | Phiên | Nơi ghi |
|---|---|---|
| Lịch TikTok (1 video mỗi ngày, lấy lịch của Video production làm chuẩn): ngày, giờ, chủ đề | Adtek - Marketing (session_01XqVohyrjLRctpapS6FbMXD) | danh sách `tiktok` trong `content/editorial/calendar.json` |
| Kịch bản, giọng, xuất video, cover, đưa lên hub | Adtek - Video production (session_015wnXjaRHuK6RciQ3JeDviz), lịch tự động ở phiên Adtek - TikTok lịch tự động (session_01RJbeQ6L8V6bz5xR8mWeYGP) | `video/` và `video/hub/videos.json` trên nhánh `claude/confident-ramanujan-t3jbi6`, hub https://claude.ai/artifact/YAeKXQbpBZj26HyPKV5wxN |
| Hẹn đăng, theo dõi, báo link | Adtek - Tiktok post (session_01XZK48jTG9DpqHxwCKxGbA6) | trường `status`, `zernio_post_id`, `tiktok_url` của mục `tiktok` |

Mỗi mục `tiktok`: `id` (tt-YYYYMMDD), `date`, `time`, `topic`, `scripts` (slug video trên hub), `status`. Status do Marketing và Video production ghi: proposed, scripted, video_ready; phiên Tiktok post ghi tiếp: scheduled, posted, cancelled, failed. Phiên Tiktok post không đổi `date`, `time`, `topic`.

Cài đặt đăng mặc định (`TIKTOK_SETTINGS` trong script): công khai, cho bình luận, Duet, Stitch (tự tắt mục nào tài khoản đã tắt trong app), nhãn AI bật, không bật nhãn quảng cáo, cover lấy từ hub (trường `cover`; không có thì TikTok lấy khung giây thứ 1). Caption = `caption` + `hashtags` trên hub, không link (link để ở bio). Nhạc nền (anh Tin chọn phương án D 17/10/2026): gắn bài trong Commercial Music Library qua Zernio lúc hẹn đăng, giọng đọc 100, nhạc 15. Chọn bài bằng `tracks` rồi `music <id> <track_id>` trước khi `schedule`: chỉ bài không lời, clip dài hơn video, không trùng bài 2 ngày liền (lệnh tự kiểm tra 2 điều sau). Đổi nhạc cho bài đã hẹn: `music` rồi `reschedule <id>`.

## Cài đặt một lần (anh Tin)

1. Tài khoản TikTok Adtek công khai, kết nối Zernio qua TikTok Business (đã xong 17/10/2026).
2. Tạo API key mới trong Zernio, lưu vào cài đặt môi trường cloud với tên `ZERNIO_API_KEY` (Network secrets hoặc biến môi trường), xóa key cũ đã lộ trong chat. Không dán vào chat.
3. Mở phiên mới, chạy `python3 tools/tiktok_post.py check`: phải ra Adtek Growth Marketing Agency, có `PUBLIC_TO_EVERYONE`.

## Lượt hẹn đăng hằng tuần (anh Tin chọn 17/10/2026)

Chạy trong phiên **Adtek - TikTok đăng tự động** (phiên mở sau khi có `ZERNIO_API_KEY`), nhánh `claude/brave-curie-2c6zbc`. Zernio giữ lịch đăng theo đúng `date`, `time` của Marketing, nên chỉ cần một lượt mỗi tuần.

- Lịch: `CRON_TZ=Asia/Ho_Chi_Minh 43 11 * * 0` (11:43 Chủ nhật, sau lượt sản xuất 08:52 của Video production).
- Phạm vi: các mục `tiktok` có `date` từ thứ Hai tới hết Chủ nhật tuần sau, status chưa phải scheduled, posted, cancelled.
- Video production nhắn danh sách video đã lên hub sau lượt sản xuất. Lúc 11:43 mà còn video trong tuần chưa có trên hub thì hẹn lại một lượt bù bằng send_later sau 3 giờ (tối đa 2 lượt bù), rồi báo anh Tin video nào vẫn thiếu.
- Marketing đổi `date` hoặc `time` của video đã hẹn: phiên Marketing nhắn phiên đăng tự động; phiên đó `cancel <id>`, đổi status về `video_ready` và `schedule <id>` lại.

### Prompt

[TikTok: hẹn đăng tuần tới] Repo Adtek_website, nhánh claude/brave-curie-2c6zbc (fetch, pull), làm theo content/editorial/routines/tiktok.md.
1. git fetch origin claude/confident-ramanujan-t3jbi6. Với mỗi mục tiktok status scheduled đã qua giờ đăng: python3 tools/tiktok_post.py status <id> (ghi tiktok_url).
2. python3 tools/tiktok_post.py week <ngày thứ Hai sắp tới theo giờ Việt Nam>. Với mỗi video chưa hẹn có video_asset: tải video và cover bằng Artifact read (url hub, path = video_asset, cover_asset), chép vào video/out/<slug>.mp4 và video/out/<slug>-cover.png, rồi python3 tools/tiktok_post.py schedule <id>. Thêm cả video của các ngày còn lại trong tuần này nếu chưa hẹn.
3. Video thiếu kịch bản hoặc chưa có trên hub: không hẹn; nếu chưa dùng hết 2 lượt bù, gọi send_later sau 3 giờ với message "[TikTok: hẹn đăng bù] Làm lại bước 2 và 3 trong mục Lượt hẹn đăng hằng tuần của content/editorial/routines/tiktok.md (lượt bù thứ <n>)."
4. Báo anh Tin: push notification (dưới 200 ký tự) "<n> video TikTok tuần <dd/mm> đã hẹn trên Zernio. Muốn hủy hay sửa video nào thì nhắn trước giờ đăng."; tin nhắn trong phiên: bảng ngày, giờ, chủ đề, caption của từng video đã hẹn, link các video đã đăng tuần trước, video còn thiếu và lý do.
5. Lỗi Zernio hoặc TikTok: báo anh Tin nguyên văn lỗi, không thử cách khác.
6. Ghi logs/changelog.md, commit, push lên claude/brave-curie-2c6zbc.

Khi anh Tin nhắn trong phiên: "hủy <id>" thì `cancel <id>`; sửa caption thì nhắn phiên Video production sửa trên hub, rồi `cancel <id>`, đổi status về `video_ready`, `schedule <id>` lại.

## Mỗi video

1. `git fetch origin claude/confident-ramanujan-t3jbi6` (script đọc `video/hub/videos.json` từ nhánh này), rồi `python3 tools/tiktok_post.py week <hôm nay>`.
2. Video có `video_asset`: tải video và cover bằng Artifact read (url hub, path = mã asset), chép vào `video/out/<slug>.mp4` và `video/out/<slug>-cover.png`. `show <id>` liệt kê việc còn thiếu.
3. Báo trước và hẹn giờ (trong 24 giờ trước giờ đăng): `schedule <id>`. Gửi anh Tin video (SendUserFile), caption, push notification "Video TikTok <giờ>: <topic>. Không nhắn hủy thì Zernio đăng đúng giờ."
4. Anh Tin nhắn "hủy <id>": `cancel <id>` (xóa lịch trên Zernio). Sửa caption: phiên Video production sửa trên hub, rồi `cancel <id>`, đổi status về `video_ready`, `schedule <id>` lại.
5. Sau giờ đăng khoảng 30 phút: `status <id>`. Đã đăng: push notification kèm `tiktok_url`. `failed`: báo anh Tin nguyên văn `fail_reason`, không thử cách khác.
6. Ghi `logs/changelog.md`, commit, push.

Giới hạn: TikTok tối đa 15 video mỗi 24 giờ cho mỗi tài khoản; Zernio gói miễn phí 60 lượt gọi mỗi phút; bản tải lên Zernio giữ 7 ngày.

Lượt nhắc đăng tay 07:47 của phiên Video production đã tắt từ 17/10/2026; việc đăng chỉ còn lượt hẹn đăng hằng tuần ở trên.
