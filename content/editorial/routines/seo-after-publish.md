# Routine: Blog Adtek: tối ưu SEO sau khi đăng

- Lịch: `CRON_TZ=Asia/Ho_Chi_Minh 43 21 * * 2,4` (21:43 thứ Ba và thứ Năm, giờ Việt Nam), sau khung đăng bài muộn nhất 20:00-20:59.
- Gắn vào phiên **Adtek - SEO** (session_013GwSn1yAegYgnHucCuLbNr). Phiên này nhận luôn việc liên kết ngược (trước đây làm trong lịch thứ Sáu của phiên Adtek - Blog post).
- Anh Tin chọn ngày 16/10/2026: lịch cố định thứ Ba và thứ Năm (bài dời ngày được bắt ở lần chạy kế tiếp), phiên SEO tự sửa mọi thứ rồi báo sau, báo qua push notification và tin nhắn trong phiên, chỉ gửi email khi có việc cần anh quyết định. Search Console: gửi lại sitemap sau mỗi lần tối ưu, kiểm tra index từ ngày thứ 2 sau khi đăng, bài chưa index thì gửi anh link bấm tay.

## Prompt

[Lịch tự động thứ Ba, thứ Năm 21:43: tối ưu SEO bài blog vừa lên sóng]
Repo Adtek_website, branch claude/brave-curie-2c6zbc (pull bản mới nhất trước). Làm theo mục "Tối ưu SEO sau khi đăng" trong content/editorial/README.md.
1. Chạy python3 tools/seo_post.py due (tự đổi bài đã lên sóng từ scheduled sang published), rồi python3 tools/gsc.py pending (bài đăng từ 2 ngày trước mà Google chưa index). Nếu cả hai đều rỗng: không gửi thông báo; nếu calendar.json có thay đổi thì commit và push, rồi dừng. Nếu gsc.py báo chưa có GSC_SERVICE_ACCOUNT (container của phiên này chạy từ trước khi biến được thêm): tạo phiên phụ bằng create_session (repo https://github.com/tinle47/Adtek_website, revision claude/brave-curie-2c6zbc) chỉ chạy trong thư mục tools các lệnh gsc.py cần dùng (pending, và submit sau bước 2), không commit, không in khóa, trả về JSON nguyên văn; đọc kết quả bằng list_events rồi ghi index_status, index_checked vào calendar.json ở phiên này. Nếu phiên phụ cũng lỗi: bỏ qua Search Console, ghi một dòng trong tin nhắn báo cáo.
2. Với mỗi bài trong danh sách:
   a. python3 tools/seo_post.py fix <số bài>: focus keyphrase Yoast, alt ảnh, nofollow link ngoài.
   b. Liên kết ngược: python3 tools/seo_post.py links <số bài>. Chèn link về bài mới từ bài trụ cột của cụm (nếu đã đăng) và 2 đến 3 bài trong candidates chưa có link, ưu tiên cùng cụm. Mỗi bài nguồn thêm một câu hoặc một đoạn ngắn ở phần nội dung liên quan, anchor là từ khóa của bài mới hoặc biến thể tự nhiên. Sửa bằng python3 tools/seo_post.py get <ID> <file> rồi put <ID> <file> "lien ket nguoc" (put tự backup vào content/backups và kiểm tra đã ghi).
   c. python3 tools/seo_post.py check <số bài>, sửa mọi mục trong failed:
      - Nội dung (kw_in_intro, kw_in_h2, kw_density, internal_out, links_pillar, links_to, anchor_text, internal_broken): sửa tối thiểu bằng get/put, giữ giọng văn và ý của bài đã duyệt, dùng skill anti-ai-writing, không dùng ký tự gạch dài, không đổi số liệu, nhận định pháp lý hay kết luận.
      - SEO title, meta description (title_length, desc_length, kw_in_title, kw_at_title_start, kw_in_desc): sửa seo_title, meta_desc trong calendar.json rồi chạy python3 tools/seo_post.py meta <số bài>.
      - Không đổi slug bài đã đăng (kw_in_slug chỉ ghi nhận). Lỗi kỹ thuật (http_200, indexable, canonical_self, in_sitemap, schema_article, og_image, h1_single): tìm nguyên nhân, sửa nếu nằm trong quyền REST; nếu cần sửa theme hay plugin thì soạn bản sửa trong repo và báo anh Tin.
   d. Chạy lại check đến khi đạt hết (hoặc chỉ còn mục ghi nhận), rồi python3 tools/seo_post.py done <số bài>.
   e. Sau khi xử lý xong mọi bài: python3 tools/gsc.py submit (hoặc qua phiên phụ như bước 1) (gửi lại sitemap cho Google). Google không có API cho nút "Yêu cầu lập chỉ mục", nên không làm cách khác (không dùng Indexing API, anh Tin chọn ngày 16/10/2026).
3. Ghi logs/changelog.md (mỗi bài một dòng: điểm trước và sau, đã sửa gì, bài nào nhận link ngược), commit, push lên claude/brave-curie-2c6zbc và đồng bộ sang claude/determined-faraday-hhy1ol (git push origin claude/brave-curie-2c6zbc:claude/determined-faraday-hhy1ol).
4. Báo anh Tin:
   - Push notification (PushNotification, dưới 200 ký tự), ví dụ: "SEO bài 3 TikTok Shop vs Shopee: 24/29 lên 29/29, thêm link từ 3 bài. Không có việc cần anh duyệt."
   - Tin nhắn trong phiên: từng bài với link, điểm trước và sau, danh sách thay đổi, bài nào nhận link ngược, việc còn lại.
   - Bài trong not_indexed của gsc.py pending: nêu trong push notification và tin nhắn, kèm link request_indexing để anh bấm "Yêu cầu lập chỉ mục" (nhắc ở mỗi lần chạy tới khi bài được index, tối đa 30 ngày sau ngày đăng; sau đó lịch rà soát ngày 1 hằng tháng xử lý).
   - Chỉ gửi email (Gmail, tới hi@tinle.co, tiêu đề "[Adtek Blog] SEO bài <số>: cần anh xem", tiếng Việt có dấu) khi có việc cần anh quyết định, ví dụ lỗi cần sửa theme hoặc plugin.
