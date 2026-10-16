# Bàn giao dự án video TikTok Adtek (16/10/2026)

File này để một phiên Claude mới nhận việc và làm tiếp mà không cần đọc lịch sử chat cũ. Đọc theo thứ tự: file này, `CLAUDE.md` (quy tắc anh Tin đã chốt, bắt buộc làm đúng), `README.md` (kỹ thuật, lệnh).

## Dự án là gì

- Kênh TikTok @adtek.growth.marketing của Adtek Growth Marketing Agency, mỗi ngày 1 video infographic khoảng 1 phút (hoặc bản ngắn 30 giây khi thử nghiệm).
- Video làm bằng Remotion (thư mục `video/`), giọng đọc nhân bản của anh Tin qua ElevenLabs (giọng "Tin Le v1", model Eleven v4, tốc độ 1.1x).
- Anh Tin đăng tay lên TikTok. Claude viết kịch bản, tạo giọng, xuất video, đưa lên trang hub và gửi email nhắc.
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
| Trang hub (anh Tin tải video, copy caption) | https://claude.ai/artifact/72zNCsPigyqbV6P8kQtji5, dữ liệu trong `video/hub/*.json` |

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
| Nhắc đăng video hôm nay (email kèm caption, cấu hình nhạc) | Mỗi ngày 07:47 | trig_01CQnosVhYjPGFhPaiztwZZ8 |
| Viết kịch bản tuần tới, email chờ duyệt | Thứ Bảy 08:47 | trig_01NTBXYMDspRxo8qvc2T6nRe |
| Sản xuất video theo kịch bản đã duyệt, đưa lên hub, email | Chủ nhật 08:52 | trig_019hnqJBnVkP1i1DYK3Yh8Ch |

Cả 3 routine hiện bắn vào phiên cũ (session_01Dpu4oyZ8FYSVLE8FrdnGTC). Khi chuyển phiên, phải trỏ lại về phiên mới hoặc đổi sang "mỗi lần chạy tạo phiên mới" (xem mục cuối). Nội dung từng routine xem bằng `get_trigger`.

## Tình trạng hiện tại (16/10/2026)

- Đã đăng tới 13/10. Đã gửi email nhắc tới 16/10 (cột K ghi "Đã nhắc").
- Video đã xong, đã có trên hub: 16/10, 17/10, 19/10, 20/10, 21/10, 22/10, 27/10.
- Chưa có video: 18/10 (ý tưởng "Mua data khách hàng để chạy quảng cáo: rủi ro tới đâu?", chưa có kịch bản) và các slot trống 23 đến 26/10, 28/10 trở đi. Routine thứ Bảy 17/10 sẽ viết kịch bản cho 18 đến 25/10, routine Chủ nhật 18/10 sản xuất. Lưu ý 18/10 đăng lúc 09:00 Chủ nhật, cùng ngày với lúc sản xuất (08:52), nên cần ưu tiên xuất video 18/10 trước.
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
