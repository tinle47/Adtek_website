# Routine: Facebook Adtek hằng ngày

Chạy trong phiên **Adtek - Facebook post** (session_0196UuuQJu6Edu8fi8VXJDzh). Lịch bài do phiên **Adtek - Marketing** lập trong danh sách `facebook` của `calendar.json`; phiên Facebook post không tự đổi `date`, `time`. Ảnh do phiên **Adtek - Designer** (session_01Wp8F7EosGPrY7v6XwBpRSM) làm, đặt ở `content/facebook/<id>/` (ảnh đơn hoặc carousel `1.jpg`, `2.jpg`...; video `video.mp4`) hoặc ghi danh sách file vào trường `images`. Công cụ: `tools/fb_daily.py`.

Quy tắc caption: viết theo `brief` và `source`, chỉ dùng số liệu có trong brief (không thêm số liệu chưa kiểm chứng), đúng định dạng ở `format`, 120 đến 200 chữ, dùng skill anti-ai-writing, không emoji, không ký tự gạch dài, không link, số theo định dạng US, ví dụ giả định phải ghi rõ là ví dụ. `hashtags` là 3 hashtag riêng, không dấu, viết liền. Script tự ghép template: tiêu đề in hoa, câu "Xem full bài viết ở bình luận bên dưới." (chỉ khi bài blog `link_post` đã lên sóng, Page sẽ bình luận link), caption, 5 hashtag, Website, Email. Bình luận link: mọi bài có `link_post` mà bài blog đã lên sóng đều bình luận link, không giới hạn số bài mỗi tuần (anh Tin chọn phương án A ngày 16/10/2026).

Khi anh Tin trả lời trong phiên: "duyệt <id>" thì chạy `python3 tools/fb_daily.py approve <id>`; "hủy <id>" thì `python3 tools/fb_daily.py cancel <id>`; yêu cầu sửa thì sửa `caption` hoặc `hashtags` trong `calendar.json`, gửi lại email (notify không kèm cờ) và giữ approval hiện có. Gỡ bài đã đăng: `python3 tools/fb_daily.py delete <id>`.

## 1. Báo trước bài sắp đăng

- Lịch: `CRON_TZ=Asia/Ho_Chi_Minh 43 8,16 * * *` (8:43 và 16:43 mỗi ngày), trig_011G6TDdHPbm7yqo6ZqqGrgA

### Prompt

[Facebook: báo trước bài sắp đăng] Pull branch claude/brave-curie-2c6zbc, làm theo content/editorial/routines/facebook-daily.md (quy tắc caption ở đầu file).
1. Chạy python3 tools/fb_daily.py week <ngày hôm nay theo giờ Việt Nam>, lấy các bài có giờ đăng trong 12 giờ tới mà status khác posted, cancelled.
2. Bài chưa có caption hoặc hashtags: viết theo quy tắc caption, ghi vào calendar.json.
3. Bài chưa có ảnh: nhắn phiên Adtek - Designer (session_01Wp8F7EosGPrY7v6XwBpRSM) bằng send_message, kèm id, giờ đăng, format, title, brief và quy ước content/facebook/<id>/.
4. Bài có approval rỗng: chạy python3 tools/fb_daily.py notify <id...> --mark, gửi to, subject, body, htmlBody, attachments nguyên văn bằng công cụ gửi Gmail; push notification (dưới 200 ký tự) "Bài Facebook <giờ>: <tiêu đề>. Không nhắn hủy thì đăng đúng giờ." (thêm "đang chờ ảnh" nếu thiếu ảnh); tin nhắn trong phiên với caption đăng thật. Bài đã báo với notified_media = 0 mà nay đã có ảnh: gửi lại email bằng notify <id> (không kèm cờ).
5. Bài có approval pending: chạy python3 tools/fb_daily.py auto.
6. Ghi logs/changelog.md, commit, push lên claude/brave-curie-2c6zbc và đồng bộ sang claude/determined-faraday-hhy1ol. Không có bài nào trong 12 giờ tới thì không gửi gì.

## 2. Đăng bài đến giờ

- Lịch: `CRON_TZ=Asia/Ho_Chi_Minh 13 12,20 * * *` (12:13 và 20:13 mỗi ngày), trig_01BM7F7Xa9Aumx4BjSNK3vH1

### Prompt

[Facebook: đăng bài đến giờ] Pull branch claude/brave-curie-2c6zbc, làm theo content/editorial/routines/facebook-daily.md.
1. Chạy python3 tools/fb_daily.py auto, rồi python3 tools/fb_daily.py due.
2. Với mỗi bài trong due: nếu problems rỗng và approval là approved hoặc auto thì chạy python3 tools/fb_daily.py publish <id>. Thành công: push notification "Đã đăng Facebook <giờ>: <tiêu đề> <url>" và tin nhắn trong phiên kèm link.
3. Bài thiếu ảnh, thiếu caption hoặc chưa duyệt: không đăng; push notification và tin nhắn nêu rõ thiếu gì; thiếu ảnh thì nhắn phiên Adtek - Designer. Lỗi khi đăng hoặc bình luận link bị chặn: báo anh Tin nguyên văn lỗi, không thử cách khác.
4. Ghi logs/changelog.md, commit, push lên claude/brave-curie-2c6zbc và đồng bộ sang claude/determined-faraday-hhy1ol. due rỗng thì không gửi gì.

## 3. Viết caption tuần tới (từ tuần 26/10/2026)

- Lịch: `CRON_TZ=Asia/Ho_Chi_Minh 7 9 * * 3` (9:07 thứ Tư), trig_01Q9TrdfsUDXYTE9vAGoosNe

### Prompt

[Facebook: viết caption tuần tới] Pull branch claude/brave-curie-2c6zbc, làm theo content/editorial/routines/facebook-daily.md.
1. Chạy python3 tools/fb_daily.py week <ngày thứ Hai tuần kế tiếp>, viết caption và hashtags cho các bài chưa có theo quy tắc caption, ghi vào calendar.json.
2. Nhắn phiên Adtek - Designer (session_01Wp8F7EosGPrY7v6XwBpRSM) danh sách 7 bài (id, giờ đăng, format, title, brief) để làm ảnh trước thứ Sáu, theo quy ước content/facebook/<id>/.
3. Chạy python3 tools/fb_daily.py notify <7 id> --pending, gửi email nguyên văn bằng Gmail (to, subject, body, htmlBody, attachments); push notification "7 bài Facebook tuần tới chờ duyệt trước <hạn>. Quá hạn sẽ tự duyệt."; tin nhắn trong phiên với caption từng bài.
4. Gọi send_later với at = deadline trong JSON (RFC3339), name "Hạn duyệt Facebook tuần <ngày thứ Hai>", message: "[Hạn duyệt Facebook D+1] Pull branch claude/brave-curie-2c6zbc, chạy python3 tools/fb_daily.py auto. Nếu auto_approved không rỗng: push notification và tin nhắn liệt kê bài tự duyệt; ghi changelog, commit, push lên claude/brave-curie-2c6zbc và đồng bộ sang claude/determined-faraday-hhy1ol."
5. Ghi logs/changelog.md, commit, push lên claude/brave-curie-2c6zbc và đồng bộ sang claude/determined-faraday-hhy1ol.
