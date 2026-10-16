# Routine: Adtek Marketing: nghiên cứu thị trường và lập kế hoạch nội dung tháng mới

- Lịch: `CRON_TZ=Asia/Ho_Chi_Minh 47 6 26-29 * *`. Prompt tự kiểm tra ngày, chỉ chạy tiếp khi hôm nay cách ngày 1 tháng sau đúng 3 ngày (ngày cuối tháng trừ 2: 29 với tháng 31 ngày, 28 với tháng 30 ngày, 26 hoặc 27 với tháng 2). Anh Tin chọn ngày 16/10/2026: mỗi tháng nghiên cứu một lần, trước ngày 1 tháng mới 3 ngày, chỉ lập lịch cho tháng kế tiếp.
- Chạy 6:47 sáng để xong trước lịch viết blog thứ Sáu 8:52 của phiên Adtek - Blog post.
- Gắn vào phiên **Adtek - Marketing** (session_01XqVohyrjLRctpapS6FbMXD).
- Trang kết quả: https://claude.ai/artifact/BHoYZVz5Nk9Wc3zfg2AHgL (file `reports/chien-luoc-noi-dung.html`).
- Nhánh: `claude/brave-curie-2c6zbc` (chung với các phiên khác), đồng bộ sang `claude/determined-faraday-hhy1ol` và `claude/tender-ptolemy-o4l8v0`.

## Phạm vi một tháng

Kế hoạch tháng M gồm các tuần có thứ Hai nằm trong tháng M (ví dụ tháng 11/2026: 2/11 đến 6/12). Quy tắc này bảo đảm phiên Blog post luôn có lịch trước thứ Sáu viết bài cho tuần đầu tiên của tháng.

## Nhịp đăng (anh Tin chọn 16/10/2026)

| Kênh | Nhịp | Giờ |
|---|---|---|
| Blog | 4 bài/tuần: thứ Hai, Ba, Năm, Sáu | 08:05 đến 08:55, phút chọn ngẫu nhiên |
| Facebook | 1 bài mỗi ngày, định dạng riêng cho Facebook, không đăng lại bài blog | 12:13 ngày thường, 20:13 thứ Bảy và Chủ nhật |
| TikTok | 3 video/tuần từ 1 bài blog (công cụ trong `video/`) | 19:13 thứ Ba, Năm, Bảy |

Định dạng Facebook xoay theo ngày: thứ Hai góc số liệu, thứ Ba thuật ngữ 1 phút, thứ Tư carousel hướng dẫn, thứ Năm tin nóng (có tin lớn thì thay), thứ Sáu phép tính nhanh (con số ví dụ ghi rõ là ví dụ), thứ Bảy hiểu lầm và sự thật hoặc câu hỏi mở, Chủ nhật video ngắn (Reels, dùng lại video TikTok; chưa có video thì đổi sang câu hỏi mở). Caption Facebook giữ giọng riêng của Page Adtek, không áp dụng `van-phong.md` (anh Tin chọn phương án A ngày 17/10/2026). Bài liên quan tới một bài blog đã lên sóng thì Page bình luận link bài đó, không giới hạn số bài có link mỗi tuần (anh Tin chọn phương án A ngày 16/10/2026).

## Các bước

1. Pull nhánh `claude/brave-curie-2c6zbc`.
2. Nghiên cứu: chạy song song 2 agent (ngành tăng trưởng tại Việt Nam; xu hướng công nghệ digital marketing), chỉ tìm thay đổi kể từ lần cập nhật trước ghi trong nhật ký nghiên cứu của trang. Mỗi số liệu có nguồn, tháng/năm, link; ghi rõ số chưa xác minh hoặc lệch giữa các nguồn.
3. Cập nhật phần nghiên cứu trong `reports/chien-luoc-noi-dung.html` (bức tranh thị trường, bảng ngành, bảng công nghệ), thêm một dòng vào nhật ký nghiên cứu.
4. Lập kế hoạch tháng mới cho cả 3 kênh:
   - Chủ đề tháng nối với thông điệp xuyên suốt.
   - Tiêu đề và brief bài blog viết theo `content/editorial/van-phong.md` (văn phong anh Tin, 17/10/2026): hứa một kết quả cụ thể, vào thẳng việc, ưu tiên bài có ví dụ làm từng bước.
   - Blog: chọn bài từ `calendar.json` (status planned hoặc backlog) và bài mới từ nghiên cứu, ưu tiên tin có tính thời sự và ngành tăng trưởng; mỗi bài có số bài, tiêu đề, cụm, từ khóa, ngày giờ.
   - Facebook: 1 bài mỗi ngày theo định dạng xoay vòng, mỗi bài có tiêu đề câu hỏi, brief, số liệu kèm nguồn, bài blog để bình luận link (chỉ khi bài đó đã lên sóng trước ngày đăng). Không lên bài mini-case hay số liệu dự án (anh Tin bỏ ngày 16/10/2026).
   - TikTok: 3 video/tuần từ 1 bài blog đã lên sóng trước ngày đăng video, mỗi video một góc.
   - Không đổi bài blog hay bài Facebook đã viết (status khác planned). Ghi `reports/lich-dang-<yyyy-mm>.json` và thay 3 bảng lịch trong trang (mỗi kênh một bảng).
5. Đăng lại trang: Artifact publish file `reports/chien-luoc-noi-dung.html` với url ở trên.
6. Đồng bộ: ghi lịch vào `content/editorial/calendar.json` (posts: date, time, title, keyword, cluster, links_to, month, status planned cho bài trong tháng, backlog cho bài chờ; `month_plans`; danh sách `facebook` và `tiktok` với status planned), rồi gửi send_message cho từng phiên (Blog post session_01AvYySKMdJYRoHxp3DYBUqB, Facebook post session_0196UuuQJu6Edu8fi8VXJDzh, Designer session_01Wp8F7EosGPrY7v6XwBpRSM, SEO session_013GwSn1yAegYgnHucCuLbNr, phiên TikTok khi có) nêu chủ đề tháng và lịch tuần đầu.
7. Ghi `logs/changelog.md`, commit, push lên `claude/brave-curie-2c6zbc` và đồng bộ sang 2 nhánh ở trên.
8. Báo anh Tin: push notification (dưới 200 ký tự, nêu chủ đề tháng và số bài từng kênh), tin nhắn trong phiên (xu hướng mới, thay đổi so với tháng trước, việc cần anh cung cấp), email Gmail tới hi@tinle.co tiêu đề "[Adtek Marketing] Kế hoạch nội dung tháng <tháng>" kèm link trang, tiếng Việt có dấu.

## Đồng bộ

ĐÃ CHO PHÉP (anh Tin, 16/10/2026): phiên Marketing tự ghi lịch vào nhánh `claude/brave-curie-2c6zbc` và tự đồng bộ các phiên với nhau.
