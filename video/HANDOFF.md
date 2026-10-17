# Bàn giao dự án video TikTok Adtek (16/10/2026)

File này để một phiên Claude mới nhận việc và làm tiếp mà không cần đọc lịch sử chat cũ. Đọc theo thứ tự: file này, `CLAUDE.md` (quy tắc anh Tin đã chốt, bắt buộc làm đúng), `README.md` (kỹ thuật, lệnh).

## Dự án là gì

- Kênh TikTok @adtek.growth.marketing của Adtek Growth Marketing Agency, mỗi ngày 1 video infographic khoảng 1 phút (hoặc bản ngắn 30 giây khi thử nghiệm).
- Video làm bằng Remotion (thư mục `video/`), giọng đọc nhân bản của anh Tin qua ElevenLabs (giọng "Tin Le v1", model Eleven v4, tốc độ 1.1x).
- Từ 17/10/2026: phiên Adtek - Marketing (session_01XqVohyrjLRctpapS6FbMXD) quản lý lịch TikTok trong `content/editorial/calendar.json` (nhánh `claude/brave-curie-2c6zbc`); phiên Adtek - TikTok đăng tự động (session_018zu7wyE9zvuKk5Smnpczn4, lượt hẹn đăng 11:43 Chủ nhật, trig_01ETurRhshMmduNMJFWEvmNb) hẹn đăng cả tuần qua Zernio, đọc `hub/videos.json`. Phiên video (Claude ở đây) viết kịch bản, tạo giọng, xuất video, đưa lên hub, email duyệt và báo 2 phiên kia. Không còn email nhắc đăng.
- Repo `tinle47/Adtek_website`, nhánh làm việc `claude/confident-ramanujan-t3jbi6`. Chỉ đẩy lên nhánh này, không tạo PR khi chưa được yêu cầu.

## Cách xưng hô và trình bày với anh Tin

- Trong chat: tiếng Việt có dấu, xưng "em", gọi "anh"; ngắn gọn, dùng gạch đầu dòng, có ví dụ thực tế; đưa nhiều phương án kèm ưu nhược để anh chọn; anh không rành kỹ thuật nên giải thích bằng lời đơn giản.
- Không dùng ký tự "—", không dùng emoji, số theo US format (75,000; 0.61%).
- Email và nội dung xuất bản: súc tích, chuyên nghiệp, không xưng anh/em. Email chỉ gửi tới hi@tinle.co.
- Không bịa số liệu, không dựng giả giao diện báo; ảnh chụp chỉ lấy từ trang gốc.

## Nơi để mọi thứ

| Thứ | Ở đâu |
|---|---|
| Quy tắc nội dung, giọng, dạng video | `video/CLAUDE.md` |
| Kịch bản | `video/scripts/<slug>/1.json` (bản ngắn: `2.json`, id thêm `-ngan`) |
| Lịch đăng (nguồn chính) | `video/plan/lich-noi-dung-tiktok.xlsx`, sheet "Lịch đăng" (cột N là trạng thái, cột K "Lưu ý khi dùng") |
| Giọng đã tạo | `video/public/voice/<id>/` (có `manifest.json`, đã commit) |
| Video xuất ra | `video/out/` (không commit; video thật nằm trên hub) |
| Trang hub (anh Tin tải video, copy caption) | https://claude.ai/artifact/YAeKXQbpBZj26HyPKV5wxN, dữ liệu trong `video/hub/*.json` |

## Lệnh hay dùng (trong thư mục `video`)

```
export REMOTION_BROWSER=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
node tools/voice.mjs <slug> [số] --skip-check     # tạo giọng; chỉ cảnh đổi lời mới tạo lại
node tools/check.mjs <slug> [số]                   # kiểm tra chữ, đứng hình, nhịp đọc; FAIL phải sửa
node tools/render.mjs <slug> [số]                  # xuất out/<id>.mp4 và out/<id>-cover.png
node tools/render.mjs <slug> --carousel            # bộ ảnh lướt
python3 tools/hub_export.py                        # sau mỗi lần đổi lịch hoặc kịch bản
```

- Cần biến môi trường ELEVENLABS_API_KEY và ELEVENLABS_VOICE_ID (đã cài trong môi trường cloud của anh Tin). Không bao giờ in hay dán khóa API.
- Sửa file lịch xlsx bằng openpyxl xong phải tính lại công thức: `soffice --headless --calc --convert-to xlsx --outdir <thư mục tạm mới> plan/lich-noi-dung-tiktok.xlsx` rồi chép lại.
- Đưa video lên hub: Artifact publish với `url` của hub, `asset: true`, `file_paths` (tối đa 25 file), lấy url `/_blob/...` ghi vào `hub/videos.json`. Sau đó publish lại trang: `file_path` = `video/hub/index.html`, `files` = videos.json, schedule.json, scripts.json (và samples.json nếu đổi). Phiên mới phải `action: "read"` hub (và các file json bằng `paths`) trước lần publish đầu tiên, nếu không sẽ bị từ chối.

## Lịch tự động (Routine, giờ Việt Nam)

| Routine | Giờ | ID |
|---|---|---|
| Nhắc đăng video hôm nay (TẮT từ 17/10/2026, việc đăng chuyển cho phiên Tiktok post) | Mỗi ngày 07:47 | trig_01BRGsizN3tkDdo9LqKXFqZS |
| Viết kịch bản tuần tới, email chờ duyệt | Thứ Bảy 08:47 | trig_013NW4HfoFmiCaGN4WUQDxdW |
| Sản xuất video theo kịch bản đã duyệt, đưa lên hub, email | Chủ nhật 08:52 | trig_01Lz38SJwUNHvE6QNbPEjHmP |

Từ chiều 17/10/2026 (anh Tin chốt): chỉ phiên Adtek - Video production (session_015wnXjaRHuK6RciQ3JeDviz) sản xuất video; việc đăng chỉ do phiên Adtek - TikTok post (session_018zu7wyE9zvuKk5Smnpczn4, lượt hẹn đăng 11:43 Chủ nhật) làm. Hai routine thứ Bảy và Chủ nhật trỏ vào phiên Video production (phiên này đã khởi động lại sau khi thêm biến nên có khóa ElevenLabs). Routine cũ trỏ vào phiên "Adtek - TikTok lịch tự động" (session_01RJbeQ6L8V6bz5xR8mWeYGP: trig_01M1bsFaGkqY3WP8Pd4k9GVe, trig_01PMqm6rHeR3J5WdBYcNmLa7) và 3 routine nháp (trig_01Q8D4SMZZuQQdiihw8kXrDN, trig_01Mf3NeyFEiVyVoXEnckCYWW, trig_013uBjHGAqWFpFDU7VztYtgg) đã tắt, không xóa. Lần sau chuyển phiên: tạo routine mới trỏ vào phiên mới (create_trigger với persistent_session_id) rồi tắt routine cũ. Nội dung từng routine chép nguyên văn từ `video/routines/*.md`. Nội dung routine chỉ sửa được từ chính phiên nhận routine (update_trigger từ phiên khác bị từ chối); tắt, bật thì phiên nào cũng làm được.

Khóa ElevenLabs của tài khoản mới không có quyền đọc thông tin tài khoản: `GET /v1/user` trả 401 là bình thường. `GET /v1/voices/<voice_id>` (endpoint `voice.mjs` dùng) trả 200, giọng "Tin Le v1".

## Tình trạng hiện tại (17/10/2026)

- Đã đăng tới 18/10 (video 18/10 do phiên Tiktok post đăng sớm lúc 15:38 ngày 17/10).
- Hub mới https://claude.ai/artifact/YAeKXQbpBZj26HyPKV5wxN (tài khoản mới sở hữu). Video sắp đăng 18 đến 22/10 và 27/10 đã xuất lại từ giọng có sẵn và tải lên hub mới. Video đã đăng (07 đến 17/10) ghi "Đã đăng", file gốc nằm ở hub cũ của tài khoản cũ, không chuyển. Mục "Mẫu dạng video mới" để trống vì asset nằm ở hub cũ.
- Kịch bản 18, 23, 24, 25/10 do routine thứ Bảy của tài khoản cũ viết sáng 17/10 (có giọng, trạng thái "Đã viết kịch bản"). Ảnh duyệt đã chụp lại và đưa lên hub mới. Video 18/10 đã xuất sẵn lên hub; routine Chủ nhật 18/10 vẫn xử lý cả 4 video theo quy trình (giọng đã có nên không tốn credit nếu không đổi lời).
- Email kịch bản tuần 18 đến 25/10 được gửi từ Gmail của tài khoản cũ, nên Gmail của tài khoản mới (tin.le@adtek.agency) không có thread đó. Từ 18/10 mọi email đi từ tin.le@adtek.agency tới hi@tinle.co.
- Video "Khách muốn nhắn tin trước khi mua" đã dời từ 09/10 (chưa đăng) sang 22/10, nguồn đã kiểm tra lại 13/10.

## Quyết định mới nhất của anh Tin (13/10/2026)

1. **Khung mở đầu chữ to (đã duyệt, áp dụng cho mọi video trừ chữ động):** trường `hook` trong kịch bản, xem mục "Khung mở đầu chữ to" trong `CLAUDE.md`. Lý do: số liệu TikTok của anh Tin cho thấy hơn 50% người xem lướt đi trong 2 giây đầu (chỉ còn 44 đến 50% ở giây thứ 2, khoảng 10% ở giây thứ 10), lượt xem gần như 100% từ For You.
2. **Thử bản ngắn 30 giây trên 14/10 (livestream) và 15/10 (thị trường app):** đã đăng bản ngắn. **Việc đang chờ:** xin anh Tin ảnh TikTok Analytics của 2 video này (tỷ lệ xem hết, tỷ lệ còn ở giây thứ 2) để so với video dài, rồi đề xuất có làm tiếp bản ngắn hay không. Mục tiêu giây thứ 2: trên 60%.
3. Mèo Adtek nói theo giọng: có mẫu nhưng **chưa bật**. Không làm thêm bản giấy cắt dán hay bộ animate.

## Lưu ý kỹ thuật dễ vấp

- `voice.mjs` lưu giọng theo số thứ tự cảnh: chèn hoặc xóa cảnh ở giữa sẽ làm các cảnh sau tạo lại giọng (tốn credit).
- Khung mở đầu (`src/design/opener.tsx`): câu chính từ 15 ký tự tự xuống 2 hàng; luôn xem khung đầu, ngắt dòng xấu thì đổi chữ. Hình của cảnh 1 chỉ bám lời đọc sau câu hook.
- `check.mjs` hay báo WARN "dưới giao diện TikTok" cho dòng nguồn nhỏ và WARN đứng hình 4 đến 9 giây ở vài cảnh cũ: không chặn xuất, nhưng ghi lý do trong email tuần.
- ffmpeg đi kèm Remotion không có muxer s16le: muốn đọc âm thanh thô thì giải mã ra WAV.
- Mạng: WebFetch đôi khi lỗi DNS, dùng `curl -sSL` qua proxy thay thế. Tải PDF lớn có thể bị ngắt, thử lại vài lần.

## Chuyển sang tài khoản Claude khác (đã xong 17/10/2026)

- GitHub, Gmail, môi trường cloud, khóa ElevenLabs: đã nối ở tài khoản mới.
- Hub: tạo mới (link ở trên), đã thay link trong `CLAUDE.md`, `HANDOFF.md`, `tools/hub_export.py`.
- 3 lịch tự động: đã tạo lại (bảng ở trên).
- Anh Tin tắt 3 routine ở tài khoản cũ (`trig_015moonCQ7qxhn7oX9AAw6Qd`, `trig_01RniaH3JPJRrWA2SBv1K6iJ`, `trig_01XR5BNQVfwxuhe6Ak7BBTci`) tại https://claude.ai/code/routines của tài khoản cũ, để tránh 2 phiên cùng sản xuất và gửi email trùng.

Công cụ cần trong container: node 22, python3 + openpyxl, ffmpeg, ffprobe, soffice (LibreOffice Calc), pdftotext, Chromium của Playwright ở `/opt/pw-browsers`. Môi trường cloud mặc định đã có đủ; phiên mới chỉ cần `cd video && npm install`.
