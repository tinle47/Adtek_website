# Brief cập nhật sâu 9 bài lưu trữ (anh Tin chọn phương án B, 17/10/2026)

Bối cảnh: 29 bài dịch cũ (2021 đến 2023) vừa đăng lại với ngày gốc. 20 bài lỗi thời hoặc trùng chủ đề đã noindex. 9 bài còn giá trị được viết lại thành bản 2026 để Google thấy nội dung có giá trị riêng, giảm rủi ro nội dung dịch lại và bản quyền.

Đây là sửa lớn: chỉ soạn bản nháp trong repo, KHÔNG sửa bài trên WordPress. Anh Tin duyệt rồi phiên SEO mới đưa lên.

## Đầu vào

- Nội dung hiện tại: `cd tools && python3 seo_post.py get <ID> <file>` (đọc từ WordPress, chỉ đọc).
- Danh sách bài và thuật ngữ đã đăng để làm link nội bộ: `content/editorial/internal-links.json`. Chỉ link tới URL có trong file này.
- Quy tắc viết: `content/editorial/README.md` (mục Quy tắc liên kết) và skill `anti-ai-writing`.

## Yêu cầu bản cập nhật

1. Giữ nguyên URL (slug), giữ chủ đề và ý hữu ích của bài cũ; bỏ phần đã sai hoặc hết thời, viết lại bằng giọng văn của Adtek, không dịch từng câu từ nguồn gốc.
2. Cập nhật bối cảnh 2025 đến 2026: số liệu, tính năng nền tảng, thay đổi chính sách. Mọi con số và nhận định có mốc thời gian phải tra bằng WebSearch hoặc WebFetch và có nguồn uy tín (báo cáo nghiên cứu, tài liệu chính thức của nền tảng, cơ quan nhà nước), ghi rõ tháng/năm. Ít nhất 3 nguồn ngoài. Không chắc thì bỏ, tuyệt đối không bịa số liệu, tên tính năng hay case khách hàng.
3. Thêm góc nhìn cho thị trường Việt Nam khi có số liệu thật, và một mục "Góc nhìn Adtek" hoặc checklist áp dụng ngay (khung làm việc, câu hỏi kiểm tra, các bước). Không bịa kết quả dự án.
4. Độ dài 1,500 đến 2,200 chữ. Cấu trúc HTML như các bài trong content/posts/*.html (h2, h3, p, ul, table nếu cần). Không có h1. Đoạn mở đầu có định nghĩa hoặc câu trả lời trực tiếp, chứa từ khóa chính.
5. Từ khóa chính: chọn 1 cụm tiếng Việt người dùng thật sự tìm, xuất hiện trong đoạn mở đầu, ít nhất 1 H2, tự nhiên 3 đến 6 lần.
6. Link nội bộ: 3 đến 5 link tới bài hoặc thuật ngữ liên quan trong internal-links.json, anchor là từ khóa bài đích (không dùng "xem thêm", "tại đây"). Link dạng tương đối `/slug/`.
7. Link ngoài: `<a href="..." target="_blank" rel="nofollow noopener">`.
8. Cuối bài: một câu mời liên hệ `/contact/`, rồi một dòng ghi nguồn tham khảo gốc, ví dụ: `<p><em>Bài viết được Adtek biên soạn lại và cập nhật năm 2026, tham khảo nội dung gốc của AppsFlyer (2021).</em></p>`.
9. Không dùng ký tự gạch dài (em dash), không emoji, số theo định dạng US (1,500; 12.5%).

## Đầu ra

- `content/posts/archive-updates/<slug>.html`: nội dung bài.
- `content/posts/archive-updates/<slug>.json`:
  `{"wp_id": ..., "slug": "...", "keyword": "...", "seo_title": "(30 đến 60 ký tự, có từ khóa ở đầu)", "meta_desc": "(120 đến 156 ký tự, có từ khóa)", "title": "(H1 mới nếu cần đổi, giữ nghĩa cũ)", "changes": ["các thay đổi chính so với bài cũ"], "sources": [{"name": "...", "url": "...", "date": "tháng/năm"}], "confirm": ["điểm cần anh Tin xác nhận, có thể rỗng"]}`
- Không commit, không push, không gọi API ghi lên WordPress. Báo lại ngắn gọn: slug, số chữ, từ khóa, số nguồn, điểm cần xác nhận.
