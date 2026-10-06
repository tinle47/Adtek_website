# Video TikTok từ bài blog

Biến bài blog adtek.agency thành video infographic dọc 1080x1920 cho kênh TikTok Adtek, giọng đọc nhân bản của anh Tin (ElevenLabs). Lịch: 3 video mỗi tuần, mỗi bài blog tách thành 3 video theo 3 góc khác nhau.

## Cách hoạt động

1. **Kịch bản** `scripts/<slug>/<số>.json`: danh sách cảnh, mỗi cảnh có `voice` (lời đọc, cũng là phụ đề) và nội dung hiển thị.
2. **Giọng đọc** `tools/voice.mjs`: gửi lời đọc từng cảnh lên ElevenLabs, nhận file mp3 và thời điểm từng chữ, lưu vào `public/voice/<id>/`.
3. **Dựng video** `tools/render.mjs`: Remotion đọc kịch bản và giọng đọc, độ dài mỗi cảnh bằng độ dài câu đọc, phụ đề tô cam đúng chữ đang đọc. Chưa có giọng thì xuất bản không tiếng, thời lượng ước tính.

## Các loại cảnh

| type | Dùng khi | Trường |
|---|---|---|
| `hook` | 2 giây mở đầu | `kicker`, `title`, `highlight` (cụm từ tô cam) |
| `stat` | Một con số lớn | `value` (ví dụ `61%`, `+35%`, `<1%`), `label`, `source` |
| `compare` | Hai con số đối chiếu | `title`, `left` / `right` {`value`, `label`}, `source` |
| `bars` | Xếp hạng 2 đến 4 mục | `title`, `items` [{`label`, `value`, `display`}], `source` |
| `list` | Các bước, checklist (tối đa 4 ý) | `title`, `items` |
| `statement` | Một câu chốt | `text`, `highlight` |
| `cta` | Cảnh cuối | `title`, `action` |

## Lệnh

```
cd video && npm install
node tools/voice.mjs aio-la-gi          # tạo giọng (cần ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID)
node tools/render.mjs aio-la-gi --stills  # chụp mỗi cảnh một ảnh để duyệt nhanh
node tools/render.mjs aio-la-gi 1 2     # xuất out/aio-la-gi-1.mp4 và caption out/aio-la-gi-1.txt
npm run studio                           # xem và chỉnh trực tiếp trên trình duyệt
```

Trong môi trường cloud đặt thêm `REMOTION_BROWSER=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`. Trên máy cá nhân không cần, Remotion tự tải trình duyệt.

## Lưu ý khi viết kịch bản

- Mỗi video 30 đến 45 giây, 5 đến 6 cảnh. Câu mở đầu phải gây tò mò hoặc có con số gây sốc.
- Số viết theo US format (`75,000`, `0.61%`). ElevenLabs tự đọc thành chữ.
- Không đặt link trong caption (TikTok không cho bấm), dùng "link ở bio".
- Thay đổi lời đọc của cảnh nào thì chỉ cảnh đó tạo lại giọng, các cảnh khác dùng file cũ.
- Remotion miễn phí cho công ty tối đa 3 người. Công ty lớn hơn cần mua Company License tại remotion.pro.
