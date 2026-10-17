# Brief viết dày 15 thuật ngữ (anh Tin chọn ngày 17/10/2026)

Bối cảnh: 34 trang thuật ngữ dưới 300 chữ chưa từng được Google thu thập. Anh Tin chọn viết dày 15 thuật ngữ người Việt hay tìm dạng "... là gì" và gắn với dịch vụ Adtek; 19 thuật ngữ còn lại đã noindex. Đây là sửa lớn: chỉ soạn bản nháp trong repo, KHÔNG ghi lên WordPress, anh Tin duyệt rồi phiên SEO đưa lên.

## Đầu vào

- Nội dung hiện tại (chỉ đọc): `cd tools && python3 -c "from fix_alt import api; r=api('GET','mona_glossary?slug=<slug>&context=edit&_fields=id,title,content,meta')[0]; print(r['id']); print(r['content']['raw'])"`
- Link nội bộ: chỉ dùng URL có trong `content/editorial/internal-links.json`, trừ các thuật ngữ đã noindex: video-views-objective, logo, brand-message, culture, sequencing, customer-service, cpm-2, brand-experience, reach-objective, brand-extension, attribution-window, deferred-deep-linking, under-delivery, click-to-install-time-ctit, click-hijacking, click-farms, click-injection, click-redirection, frequency.
- Quy tắc viết: skill `anti-ai-writing`, không gạch dài (em dash), không emoji, số theo định dạng US.

## Yêu cầu mỗi thuật ngữ

1. 500 đến 800 chữ, tiếng Việt. Câu đầu tiên là định nghĩa trực tiếp, trả lời "X là gì?" trong 1 đến 2 câu, có thuật ngữ gốc và cách gọi tiếng Việt.
2. Cấu trúc HTML: không có h1 (theme đã in tên thuật ngữ làm H1). Dùng h2 cho các mục, ví dụ: X là gì, vì sao quan trọng, các thành phần hoặc cách tính (công thức nếu có), ví dụ thực tế ở Việt Nam (chỉ dùng ví dụ có nguồn công khai, hoặc ví dụ minh họa ghi rõ là giả định), phân biệt với thuật ngữ dễ nhầm, câu hỏi thường gặp (2 đến 3 câu hỏi ngắn). Dùng p, ul, table khi cần, không dùng span style.
3. Ít nhất 2 nguồn ngoài uy tín (tài liệu nền tảng, sách hoặc hiệp hội chuyên ngành, báo cáo nghiên cứu) có tháng/năm, tra bằng WebSearch. Không bịa số liệu. Link ngoài: `target="_blank" rel="nofollow noopener"`.
4. 2 đến 4 link nội bộ: thuật ngữ liên quan (đặc biệt giữa các thuật ngữ brand với nhau) và bài blog liên quan. Link tương đối `/glossary/slug/` hoặc `/slug/`, anchor là tên thuật ngữ hoặc từ khóa bài đích.
5. Kết thúc bằng 1 câu mời liên hệ `/contact/` gắn với dịch vụ liên quan (Brand Strategy, quảng cáo, đo lường) mà không hứa kết quả.

## Đầu ra

- `content/glossary-updates/<slug>.html`
- `content/glossary-updates/<slug>.json`: `{"id": <ID WordPress>, "slug": "...", "keyword": "<thuật ngữ> là gì", "seo_title": "30 đến 60 ký tự, bắt đầu bằng từ khóa", "meta_desc": "120 đến 156 ký tự, có từ khóa", "sources": [{"name": "...", "url": "...", "date": "tháng/năm"}], "confirm": ["điểm cần anh Tin xác nhận, có thể rỗng"]}`
- Không commit, không push, không ghi WordPress. Báo lại ngắn: mỗi slug, số chữ, số nguồn, điểm cần xác nhận.
