# Video TikTok từ bài blog

Biến bài blog adtek.agency thành video infographic dọc 1080x1920 cho kênh TikTok Adtek, giọng đọc nhân bản của anh Tin (ElevenLabs). Lịch: 3 video mỗi tuần, mỗi bài blog tách thành 3 video theo 3 góc khác nhau.

## Cách hoạt động

1. **Kịch bản** `scripts/<slug>/<số>.json`: danh sách cảnh, mỗi cảnh có `voice` (lời đọc, cũng là phụ đề) và nội dung hiển thị.
2. **Giọng đọc** `tools/voice.mjs`: gửi lời đọc từng cảnh lên ElevenLabs, nhận file mp3 và thời điểm từng chữ, lưu vào `public/voice/<id>/`.
3. **Dựng video** `tools/render.mjs`: Remotion đọc kịch bản và giọng đọc, độ dài mỗi cảnh bằng độ dài câu đọc, phụ đề tô cam đúng chữ đang đọc. Chưa có giọng thì xuất bản không tiếng, thời lượng ước tính. Âm thanh được cân về -14 LUFS (mức to chuẩn của TikTok).
4. **Nhạc nền** chèn trên TikTok lúc đăng, video xuất ra chỉ có giọng đọc.

## Thiết kế

Khung navy phẳng, logo góc trái, tiêu đề 2 dòng font Source Serif 4 (dòng trắng + dòng cam), phụ đề Be Vietnam Pro.
Biểu đồ theo chuẩn McKinsey: màu phẳng, cột vuông, không lưới, số ghi thẳng trên dữ liệu, chú thích bằng đường kẻ mảnh, chỉ một điểm nhấn cam.

## Cấu trúc một cảnh

`kicker` (dòng dẫn nhỏ), `headline` (dòng trắng), `accent` (dòng cam), `voice` (lời đọc, cũng là phụ đề), `visual` (hình minh họa, bỏ trống thì cảnh là câu chốt với tiêu đề lớn).

| visual.type | Dùng khi | Trường chính |
|---|---|---|
| `serp` | Mở đầu bằng cảnh tìm Google trên điện thoại | `query`, `answer`, `result` (bài thật), `questions`, `note` |
| `chat` | Mở đầu bằng cảnh hỏi chatbot 2 lần | `question`, `answers` (tên thương hiệu luôn bị làm mờ), `note` |
| `columns` | So sánh 2 đến 4 con số | `metric`, `unit`, `source`, `max`, `cols` [{`label`, `value`, `tone`, `step`}], `notes` |
| `hbars` | Xếp hạng nhiều yếu tố | như `columns`, dùng `rows` |
| `continue` | Giữ biểu đồ của cảnh trước, hiện thêm phần có `step: 1` | |
| `waffle` | Tỷ lệ "x trên 100" | `metric`, `unit`, `source`, `lit`, `legend` |
| `list` | Các bước, checklist (tối đa 4 ý) | `items` |
| `article` | Cảnh cuối, thẻ bài blog | `image` (ảnh bìa trong public/covers), `title`, `url` |

`tone`: `base` (nhóm đối chiếu), `main` (nhóm chính), `accent` (điểm nhấn cam, chỉ một). `notes`: `drop` (mũi tên từ cột `from` xuống cột `to`) hoặc `callout` (chữ đậm chỉ vào cột/thanh `at`).

## Lệnh

```
cd video && npm install
node tools/voice.mjs aio-la-gi          # tạo giọng bằng Eleven v4 (cần ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID; đổi model bằng ELEVENLABS_MODEL)
node tools/render.mjs aio-la-gi --stills  # chụp mỗi cảnh một ảnh để duyệt nhanh (out/)
node tools/render.mjs aio-la-gi 1 2     # xuất out/aio-la-gi-1.mp4 và caption out/aio-la-gi-1.txt
npm run studio                           # xem và chỉnh trực tiếp trên trình duyệt
```

Trong môi trường cloud đặt thêm `REMOTION_BROWSER=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`. Trên máy cá nhân không cần, Remotion tự tải trình duyệt.

## Đăng lên TikTok

1. Tải `out/<id>.mp4` lên, dán caption từ `out/<id>.txt`.
2. Bấm **Sounds**, chọn nhạc nhẹ không lời trong Commercial Music Library (tài khoản doanh nghiệp chỉ được dùng kho này).
3. Bấm **Volume**: **Original** (giọng đọc) kéo hết cỡ 100%, **Sound** (nhạc) khoảng 15%. Giọng đã ở -14 LUFS nên mức này nhạc nằm nhẹ phía sau, không lấn lời.

## Giọng đọc

- Giọng "Tin Le v1" là Professional Voice Clone giọng miền Nam. Mỗi model phải được huấn luyện riêng (ElevenLabs, My Voices, dấu cộng cạnh tên model). Model chưa huấn luyện chỉ bắt chước gần đúng, giọng bị pha Bắc.
- `voice.mjs` kiểm tra việc này trước khi tạo giọng và dừng lại nếu chưa huấn luyện. Sau khi huấn luyện xong, chạy lại với `--force` để tạo lại toàn bộ giọng cũ.

## Lưu ý khi viết kịch bản

- Mỗi video 30 đến 45 giây, 5 đến 6 cảnh. Câu mở đầu phải gây tò mò hoặc có con số gây sốc.
- Số viết theo US format (`75,000`, `0.61%`). ElevenLabs tự đọc thành chữ.
- Không đặt link trong caption (TikTok không cho bấm), dùng "link ở bio".
- Thay đổi lời đọc của cảnh nào thì chỉ cảnh đó tạo lại giọng, các cảnh khác dùng file cũ.
- Từ máy đọc sai (viết tắt, tên tiếng Anh) khai báo một lần trong `tools/pronunciation.json`, dạng `"AIO": "ây ai âu"`. Máy đọc theo cách đọc, phụ đề vẫn hiện chữ gốc. Từ điển phân biệt hoa thường và chỉ thay nguyên chữ, nên `AI` không ảnh hưởng chữ "ai" tiếng Việt. Sửa từ điển xong chạy lại `voice.mjs`, chỉ những cảnh có chữ đó tạo lại giọng.
- Remotion miễn phí cho công ty tối đa 3 người. Công ty lớn hơn cần mua Company License tại remotion.pro.
