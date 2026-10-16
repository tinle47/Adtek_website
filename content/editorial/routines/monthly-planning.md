# Routine: Adtek Marketing: nghiên cứu thị trường và lập kế hoạch nội dung tháng mới

- Lịch: `CRON_TZ=Asia/Ho_Chi_Minh 47 6 26-29 * *`. Prompt tự kiểm tra ngày, chỉ chạy tiếp khi hôm nay cách ngày 1 tháng sau đúng 3 ngày (ngày cuối tháng trừ 2: 29 với tháng 31 ngày, 28 với tháng 30 ngày, 26 hoặc 27 với tháng 2). Anh Tin chọn ngày 16/10/2026: mỗi tháng nghiên cứu một lần, trước ngày 1 tháng mới 3 ngày, chỉ lập lịch cho tháng kế tiếp.
- Chạy 6:47 sáng để xong trước lịch viết blog thứ Sáu 8:52 của phiên Adtek - Blog post.
- Gắn vào phiên **Adtek - Marketing** (session_01XqVohyrjLRctpapS6FbMXD).
- Trang kết quả: https://claude.ai/artifact/BHoYZVz5Nk9Wc3zfg2AHgL (file `reports/chien-luoc-noi-dung.html`).

## Phạm vi một tháng

Kế hoạch tháng M gồm các tuần có thứ Hai nằm trong tháng M (ví dụ tháng 11/2026: 2/11 đến 6/12). Quy tắc này bảo đảm phiên Blog post luôn có lịch trước thứ Sáu viết bài cho tuần đầu tiên của tháng.

## Nhịp đăng (anh Tin chọn 16/10/2026)

| Kênh | Nhịp | Giờ |
|---|---|---|
| Blog | 4 bài/tuần: thứ Hai, Ba, Năm, Sáu | 08:05 đến 08:55, phút chọn ngẫu nhiên |
| Facebook | 1 bài mỗi ngày, định dạng riêng cho Facebook, không đăng lại bài blog | 12:13 ngày thường, 20:13 thứ Bảy và Chủ nhật |
| TikTok | 3 video/tuần từ 1 bài blog (công cụ trong `video/`) | 19:13 thứ Ba, Năm, Bảy |

Định dạng Facebook xoay theo ngày: thứ Hai góc số liệu, thứ Ba thuật ngữ 1 phút, thứ Tư carousel hướng dẫn, thứ Năm tin nóng (có tin lớn thì thay), thứ Sáu phép tính nhanh hoặc mini-case Adtek, thứ Bảy hiểu lầm và sự thật hoặc câu hỏi mở, Chủ nhật video ngắn (Reels, dùng lại video TikTok; chưa có video thì đổi sang câu hỏi mở). Bài liên quan tới một bài blog đã lên sóng thì Page bình luận link bài đó.

## Các bước

1. Pull nhánh `claude/tender-ptolemy-o4l8v0`.
2. Nghiên cứu: chạy song song 2 agent (ngành tăng trưởng tại Việt Nam; xu hướng công nghệ digital marketing), chỉ tìm thay đổi kể từ lần cập nhật trước ghi trong nhật ký nghiên cứu của trang. Mỗi số liệu có nguồn, tháng/năm, link; ghi rõ số chưa xác minh hoặc lệch giữa các nguồn.
3. Cập nhật phần nghiên cứu trong `reports/chien-luoc-noi-dung.html` (bức tranh thị trường, bảng ngành, bảng công nghệ), thêm một dòng vào nhật ký nghiên cứu.
4. Lập kế hoạch tháng mới cho cả 3 kênh:
   - Chủ đề tháng nối với thông điệp xuyên suốt.
   - Blog: chọn bài từ `calendar.json` (status planned hoặc backlog) và bài mới từ nghiên cứu, ưu tiên tin có tính thời sự và ngành tăng trưởng; mỗi bài có số bài, tiêu đề, cụm, từ khóa, ngày giờ.
   - Facebook: 1 bài mỗi ngày theo định dạng xoay vòng, mỗi bài có tiêu đề câu hỏi, brief, số liệu kèm nguồn, bài blog để bình luận link (chỉ khi bài đó đã lên sóng trước ngày đăng). Mini-case cần số liệu dự án thì ghi rõ hạn anh Tin cung cấp.
   - TikTok: 3 video/tuần từ 1 bài blog đã lên sóng trước ngày đăng video, mỗi video một góc.
   - Ghi `reports/lich-dang-<yyyy-mm>.json` và thay 3 bảng lịch trong trang (mỗi kênh một bảng).
5. Đăng lại trang: Artifact publish file `reports/chien-luoc-noi-dung.html` với url ở trên.
6. Đồng bộ cho các phiên đăng bài: chỉ làm khi mục "Đồng bộ" dưới đây ghi ĐÃ CHO PHÉP. Khi đó ghi lịch vào `content/editorial/calendar.json` trên nhánh `claude/brave-curie-2c6zbc` và gửi send_message cho từng phiên (Blog post, Facebook post, Designer, SEO, phiên làm TikTok) nêu lịch tuần đầu.
7. Ghi `logs/changelog.md`, commit, push lên `claude/tender-ptolemy-o4l8v0`.
8. Báo anh Tin: push notification (dưới 200 ký tự, nêu chủ đề tháng và số bài từng kênh), tin nhắn trong phiên (xu hướng mới, thay đổi so với tháng trước, việc cần anh cung cấp), email Gmail tới hi@tinle.co tiêu đề "[Adtek Marketing] Kế hoạch nội dung tháng <tháng>" kèm link trang, tiếng Việt có dấu.

## Đồng bộ

CHƯA CHO PHÉP (16/10/2026): đang chờ anh Tin cho phép ghi vào nhánh `claude/brave-curie-2c6zbc` và sửa lịch tự động của các phiên đăng bài.
