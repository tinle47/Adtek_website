# Brief 3 bài cụm User Acquisition (anh Tin yêu cầu 17/10/2026)

Bối cảnh: Search Console cho thấy /glossary/user-acquisition-ua/ là trang duy nhất có từ khóa không thương hiệu (ua, ua là gì, ua marketing là gì, user acquisition là gì, vị trí 7 đến 12). Anh Tin muốn thêm 2 đến 3 bài có giá trị theo chuẩn E-E-A-T để xây cụm chủ đề quanh UA. Lịch blog đã có bài 27 "App User Acquisition 2026" (đăng 5/11, phiên Blog post viết): KHÔNG viết trùng góc tổng quan đó. Đây là bản nháp trong repo, KHÔNG ghi WordPress, KHÔNG commit, KHÔNG push. Anh Tin duyệt, phiên Marketing xếp ngày, rồi mới đăng.

## Chuẩn E-E-A-T bắt buộc

- Experience: không bịa trải nghiệm, case khách hàng, kết quả dự án hay con số nội bộ. Mỗi bài có đúng 1 mục ngắn "Góc nhìn từ thực tế" chứa chỗ trống `<p>[ANH TIN BỔ SUNG: câu hỏi cụ thể cho anh Tin, ví dụ một bài học khi chạy UA ở Shopee]</p>`; ghi điểm này vào confirm. Phần còn lại viết như người làm nghề: quy trình, ngưỡng kiểm tra, sai lầm thường gặp, có ví dụ minh họa ghi rõ "ví dụ giả định".
- Expertise: tác giả là Tín Lê (Founder & Managing Director Adtek, hơn 10 năm digital marketing tại VNG, Adayroi, Lazada, Shopee; Former Head of Online Marketing @ Shopee Vietnam; đội Adtek có chứng chỉ Google Ads, Meta Blueprint, Apple Ads). Không viết tiểu sử trong bài (trang tác giả đã có), chỉ được nhắc "đội Adtek có chứng chỉ Apple Ads" khi liên quan.
- Authoritativeness, Trust: ít nhất 4 nguồn ngoài uy tín, ưu tiên tài liệu chính thức (Apple Developer, Apple Ads, Google Ads Help, Meta Business Help, AppsFlyer, Adjust, Sensor Tower, data.ai, Statista có tác giả gốc) có tháng/năm, tra bằng WebSearch/WebFetch và mở trang kiểm tra. Số liệu không chắc thì bỏ. Benchmark phải nói rõ nguồn, thị trường, năm, và lưu ý "chỉ để tham khảo". Có dòng đầu bài `<p><em>Cập nhật tháng 10/2026.</em></p>`.

## Quy tắc viết (content/editorial/README.md)

- 1,800 đến 2,300 chữ, tiếng Việt tự nhiên, skill anti-ai-writing. Không h1. h2, h3, p, ul, ol, table. Không span style. Đoạn mở đầu trả lời trực tiếp, chứa từ khóa chính; từ khóa ở ít nhất 1 H2, 3 đến 6 lần tự nhiên.
- Không ký tự gạch dài (em dash) hay en dash, không emoji, số định dạng US (1,500; 12.5%).
- Một phần dùng được ngay: khung, checklist hoặc bảng tính.
- Link nội bộ tương đối, CHỈ tới URL trong content/editorial/internal-links.json, KHÔNG tới /glossary/retargeting/. Bắt buộc: 1 link tới /glossary/user-acquisition-ua/ (anchor "user acquisition" hoặc "UA là gì"); link thuật ngữ ở lần nhắc đầu (SKAdNetwork, ATT, IDFA, ROAS, LTV, ASO, mobile attribution, install fraud, deep linking, organic install, CPM nếu có nhắc); ít nhất 2 bài blog app marketing đã đăng: /nhung-dieu-can-biet-ve-app-marketing-kpis/, /khoi-chay-thanh-cong-ung-dung-tren-app-store/, /chien-luoc-app-marketing-9-phuong-phap/. Anchor là từ khóa bài đích, không "xem thêm", "tại đây".
- Link ngoài: `target="_blank" rel="nofollow noopener"`.
- Cuối bài 1 câu mời liên hệ /contact/ cho dịch vụ App Marketing / UA của Adtek, không hứa kết quả.

## Đầu ra mỗi bài

- content/posts/<slug>.html
- content/posts/ua-cluster/<slug>.json:
  {"title": "...", "keyword": "...", "cluster": "C2 hoặc C3", "slug": "...", "seo_title": "30 đến 60 ký tự, bắt đầu bằng từ khóa", "meta_desc": "120 đến 156 ký tự, có từ khóa", "words": <số chữ>,
   "cover": {"kicker": "...", "title": "tiêu đề ngắn, có thể bọc 1 từ khóa trong *...*", "subtitle": "...", "chips": ["3 đến 4 chip ngắn"], "hero": "một con số có trong bài", "hero_text": "cụm chữ đọc liền sau số", "fb_kicker": "..."},
   "summary": "2 đến 3 câu", "links_internal": ["..."], "sources": [{"name","url","date"}], "confirm": ["..."]}
- Tự kiểm tra trước khi báo xong: số chữ, không — hay –, link nội bộ đều có trong internal-links.json, link ngoài có nofollow, không h1, có đúng 1 chỗ [ANH TIN BỔ SUNG: ...]. Báo lại ngắn: slug, số chữ, số nguồn, điểm cần xác nhận.
