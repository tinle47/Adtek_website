# Video TikTok từ bài blog

Video infographic dọc 1080x1920 cho kênh TikTok Adtek (@adtek.growth.marketing), giọng đọc nhân bản của anh Tin (ElevenLabs). Lịch: mỗi ngày 1 video, mỗi video một chủ đề độc lập, xem `plan/lich-noi-dung-tiktok.xlsx` và `CLAUDE.md`.

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
| `bignumber` | Một con số gây sốc, đếm từ 0 | `value`, `display`, `prefix`, `suffix`, `label`, `context`, `source` |
| `versus` | Hai con số đối đầu, bên thắng phóng to | `metric`, `unit`, `source`, `items` [2 × {`label`, `value`, `suffix`}], `winner`, `note` |
| `slope` | Trước và sau của 1 đến 3 nhóm, đường vẽ dần | `metric`, `unit`, `source`, `from`, `to`, `series` [{`label`, `a`, `b`, `tone`}] |
| `trend` | Xu hướng từ 3 mốc trở lên, đường và vùng mờ | `metric`, `unit`, `source`, `points` [{`label`, `value`}], `min` (trục không bắt đầu từ 0 thì ghi rõ trong `note`), `note` |
| `donut` | Các phần trong một tổng (thị phần) | `metric`, `unit`, `source`, `parts` [{`label`, `value`, `tone`}], `center`, `centerLabel` |
| `people` | "x trên 10 người", từng người sáng lên | `metric`, `unit`, `source`, `lit` (0 đến 10), `legend` |
| `funnel` | Rơi rụng qua từng bước, độ rộng đúng tỷ lệ | `metric`, `unit`, `source`, `stages` [{`label`, `value`}] |
| `waffle` | Tỷ lệ "x trên 100" | `metric`, `unit`, `source`, `lit`, `legend` |
| `list` | Các bước, checklist (tối đa 4 ý) | `items` |
| `follow` | Cảnh cuối, kêu gọi theo dõi kênh Adtek | `note` (lời hứa nội dung, mặc định "Số liệu marketing có nguồn, mỗi ngày.") |
| `article` | Thẻ bài blog (không dùng cho kênh TikTok vì kênh độc lập với website) | `image`, `title`, `url` |

`tone`: `base` (nhóm đối chiếu), `main` (nhóm chính), `accent` (điểm nhấn cam, chỉ một). `notes`: `drop` (mũi tên từ cột `from` xuống cột `to`) hoặc `callout` (chữ đậm chỉ vào cột/thanh `at`).

## Lệnh

```
cd video && npm install
node tools/voice.mjs aio-la-gi          # tạo giọng bằng Eleven v4 (cần ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID; đổi model bằng ELEVENLABS_MODEL)
node tools/render.mjs aio-la-gi --stills  # chụp mỗi cảnh một ảnh để duyệt nhanh (out/)
node tools/render.mjs aio-la-gi 1 2     # xuất out/aio-la-gi-1.mp4 và caption out/aio-la-gi-1.txt
npm run studio                           # xem và chỉnh trực tiếp trên trình duyệt
node tools/shot.mjs <url> "<câu có con số>" <tên>  # chụp trang gốc, ghi vị trí câu cần tô sáng (public/shots/)
```

Cảnh `shot` dùng ảnh chụp thật của bài báo hoặc báo cáo: khung trình duyệt, trang trượt tới câu có con số, bút dạ quang cam quét qua con số, phần còn lại tối đi. Chép `width`, `height`, `highlight`, `url` từ file `public/shots/<tên>.json` vào kịch bản, thêm `source` và `note` (ví dụ: `scripts/demo-anh-chup/1.json`). Chỉ chụp trang gốc của nguồn, không sửa ảnh, không dựng giả giao diện trang báo. Mạng của môi trường cloud phải cho phép tên miền của trang cần chụp.

Trong môi trường cloud đặt thêm `REMOTION_BROWSER=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`. Trên máy cá nhân không cần, Remotion tự tải trình duyệt.

## Đăng lên TikTok

1. Tải `out/<id>.mp4` lên, dán caption từ `out/<id>.txt`.
2. Bấm **Sounds**, chọn nhạc nhẹ không lời trong Commercial Music Library (tài khoản doanh nghiệp chỉ được dùng kho này).
3. Bấm **Volume**: **Original** (giọng đọc) kéo hết cỡ 100%, **Sound** (nhạc) khoảng 15%. Giọng đã ở -14 LUFS nên mức này nhạc nằm nhẹ phía sau, không lấn lời.

## Giọng đọc

- Giọng "Tin Le v1" là Professional Voice Clone giọng miền Nam. Mỗi model phải được huấn luyện riêng (ElevenLabs, My Voices, dấu cộng cạnh tên model). Model chưa huấn luyện chỉ bắt chước gần đúng, giọng bị pha Bắc.
- `voice.mjs` kiểm tra việc này trước khi tạo giọng và dừng lại nếu chưa huấn luyện. Sau khi huấn luyện xong, chạy lại với `--force` để tạo lại toàn bộ giọng cũ.

## Lưu ý khi viết kịch bản

- Mỗi video khoảng 1 phút (50 đến 65 giây), 6 cảnh: câu hỏi mở đầu, 3 đến 4 cảnh số liệu, 1 cảnh "làm gì ngay", cảnh Follow.
- Câu đầu tiên của lời đọc là một câu hỏi khơi tò mò, ví dụ "Vốn FDI tăng 76%. Vậy tại sao nhà đầu tư vẫn chưa gọi cho bạn?". Cảnh mở đầu nên có biểu đồ để người xem dừng lại.
- Chỉ giữ ý mạnh, số liệu ấn tượng. Một chủ đề làm thành một video, không tách nhỏ thành nhiều video.
- Viết tiếng Việt tự nhiên như người Việt nói, không dịch thẳng từ tiếng Anh. Áp dụng cho cả lời đọc, tiêu đề, nhãn biểu đồ, chú thích và dòng nguồn. Đọc to lên, câu nào nghe như văn bản dịch thì viết lại. Ví dụ:
  - "lọc bạn", "danh sách lọc" (screen, shortlist) → "so sánh bạn", "lọt vào danh sách"
  - "hành trình mua" (buyer journey) → "cách khách hàng mua hàng"
  - "hệ sinh thái" (ecosystem) → "doanh nghiệp lớn ở gần", "các bên liên quan"
  - "ổn định chính trị" (political stability) → "chính trị ổn định"
  - "cá nhân hóa theo thời gian thực" (real-time personalization) → "nhắn đúng người, đúng lúc"
  - "người mua B2B" → "khách hàng doanh nghiệp"
- Tránh từ sáo rỗng: đóng vai trò quan trọng, bứt phá, giải pháp toàn diện, hành trình, kỷ nguyên, chìa khóa thành công, trong bối cảnh hiện nay.
- Số viết theo US format (`75,000`, `0.61%`). ElevenLabs tự đọc thành chữ.
- Kênh TikTok độc lập với website: mỗi video một chủ đề riêng, không dẫn về blog, không đặt link trong caption. Cảnh cuối dùng `follow`, lời đọc kết bằng "Follow Adtek để xem số liệu marketing mới mỗi ngày."
- Số liệu chỉ lấy từ tổ chức phát hành gốc (danh sách chủ đề và nguồn: `plan/lich-noi-dung-tiktok.xlsx`), ghi nguồn trên biểu đồ.
- Thay đổi lời đọc của cảnh nào thì chỉ cảnh đó tạo lại giọng, các cảnh khác dùng file cũ.
- Từ máy đọc sai (viết tắt, tên tiếng Anh) khai báo một lần trong `tools/pronunciation.json`, dạng `"AIO": "ây ai âu"`. Máy đọc theo cách đọc, phụ đề vẫn hiện chữ gốc. Từ điển phân biệt hoa thường và chỉ thay nguyên chữ, nên `AI` không ảnh hưởng chữ "ai" tiếng Việt. Sửa từ điển xong chạy lại `voice.mjs`, chỉ những cảnh có chữ đó tạo lại giọng.
- Remotion miễn phí cho công ty tối đa 3 người. Công ty lớn hơn cần mua Company License tại remotion.pro.
