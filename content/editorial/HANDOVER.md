# Bàn giao dự án blog Adtek sang tài khoản Claude mới

Cập nhật: 14/10/2026. Đây là tài liệu để tài khoản Claude mới tiếp tục dự án blog mà không cần đọc lại lịch sử trò chuyện.

## 1. Trạng thái hiện tại

| Bài | Tiêu đề | WordPress | Trạng thái | Lịch đăng |
|---|---|---|---|---|
| 1 | Kế hoạch 11.11: checklist 30 ngày | 6086 | Đã đăng | 13/10, 20:53 |
| 2 | Quảng cáo Meta 2026: Andromeda | 6088 | Đã đặt lịch (đã duyệt) | 15/10, 20:20 |
| 3 | TikTok Shop vs Shopee 2026 | 6093 | Đã đặt lịch (tự duyệt D+1) | 20/10, 12:21 |
| 4 | Luật bảo vệ dữ liệu cá nhân 2026 | 6096 | Đã đặt lịch (tự duyệt D+1, còn điểm pháp lý cần xác nhận) | 22/10, 20:11 |
| 5 đến 32 | Xem `calendar.json` | | Chưa viết | 27/10/2026 đến 28/1/2027 |

Việc đang dở:

- Liên kết ngược cho bài 1 (đã đăng 13/10) và bài 2: làm trong lần chạy thứ Sáu kế tiếp.
- Đăng Facebook: đã chọn Graph API (16/10/2026). Page Adtek Growth Agency (ID 101888089257566), công cụ `tools/fb_post.py`: đăng ảnh 4:5 + câu CTA chung + `fb_caption`, Page tự bình luận `fb_comment` chứa link. Network secret cho `graph.facebook.com` phải là **Page access token** (kiểm tra: `curl -sS "https://graph.facebook.com/me?fields=id,name"` trả về Page, không phải System User). Bài 1 đến 4 chưa đăng Facebook, chờ anh Tin duyệt lịch.

## 2. Những gì nằm trong repo (đi theo dự án)

Repo `tinle47/adtek_website`, nhánh `claude/brave-curie-2c6zbc`.

- `content/editorial/README.md`: toàn bộ quy trình (nhịp đăng, duyệt, liên kết, cập nhật).
- `content/editorial/calendar.json`: 32 bài, trạng thái, giờ đăng, metadata, bài Facebook.
- `content/editorial/routines/`: nguyên văn prompt của 2 lịch tự động.
- `content/posts/`: HTML và ảnh bìa từng bài.
- `tools/blog_post.py`, `tools/approval_email.py`, `tools/render_cover.js`, `tools/build_blog_page.py`: công cụ tạo ảnh bìa, đưa nháp, đặt lịch, email duyệt, dựng trang lịch.
- `templates/blog-plan.html`: mẫu trang "Lịch blog Adtek".
- `wordpress/mu-plugins/`: các plugin đã cài trên hosting (đăng nhập REST, SEO meta, link xem trước không cần đăng nhập).
- `logs/changelog.md`: nhật ký mọi thay đổi trên website.

## 3. Những gì gắn với tài khoản cũ, phải thiết lập lại

| Hạng mục | Việc cần làm ở tài khoản mới |
|---|---|
| GitHub | Kết nối GitHub và cài Claude GitHub App cho repo `tinle47/adtek_website` |
| Môi trường cloud | Tạo môi trường mới. Network access cho phép `adtek.agency` và `www.adtek.agency`. Thêm network secret cho 2 host này, gửi header `X-Adtek-Auth` = base64 của `username:application-password` (xem README gốc). Nên tạo một Application Password mới trong WordPress cho tài khoản mới, rồi thu hồi mật khẩu cũ sau khi chuyển xong |
| Gmail | Kết nối connector Gmail để gửi email tới hi@tinle.co |
| Thông báo đẩy | Đăng nhập ứng dụng Claude trên điện thoại bằng tài khoản mới |
| Lịch tự động | Tạo lại 2 routine theo `content/editorial/routines/` (cùng lịch, cùng prompt), gắn vào một phiên cố định |
| Trang "Lịch blog Adtek" | Trang cũ thuộc tài khoản cũ. Dựng lại bằng `python3 tools/build_blog_page.py <file.html>` rồi publish artifact mới, hoặc chia sẻ trang cũ cho tài khoản mới |
| Facebook (Graph API) | Thêm `graph.facebook.com` vào network access; network secret header `Authorization: Bearer <Page access token>` (lấy từ System User `claude-blog` trong Business Manager, token không hết hạn, đổi sang Page token bằng `GET /101888089257566?fields=access_token`). Token System User cần đủ 5 quyền: `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`, `pages_manage_engagement`, `pages_read_user_content` (thiếu quyền cuối thì không bình luận được). Chạy `python3 tools/fb_post.py check` phải ra Page 101888089257566 |

## 4. Thứ tự chuyển giao để không chạy trùng

Hai tài khoản cùng chạy lịch sẽ viết trùng bài 5 và 6. Làm theo thứ tự:

1. Thiết lập xong mục 3 ở tài khoản mới (trừ lịch tự động).
2. Trong phiên mới, kiểm tra đăng nhập WordPress bằng lệnh chỉ đọc `curl -sS "https://adtek.agency/wp-json/wp/v2/users/me?context=edit"` (phải trả về tên người dùng, không phải lỗi 401), và gửi thử 1 email qua Gmail.
3. Tắt 2 lịch tự động blog ở tài khoản cũ.
4. Tạo 2 lịch tự động ở tài khoản mới.

Lịch thứ Sáu kế tiếp chạy lúc 8:52 sáng 16/10. Nếu chưa chuyển xong trước giờ đó, cứ để tài khoản cũ chạy lượt này rồi chuyển sau.

## 5. Câu mở đầu cho phiên mới

Dán vào phiên Claude Code mới (repo `tinle47/adtek_website`):

> Đọc content/editorial/HANDOVER.md và content/editorial/README.md trên nhánh claude/brave-curie-2c6zbc. Đây là dự án blog Adtek chuyển từ tài khoản Claude khác sang. Kiểm tra kết nối WordPress, Gmail, rồi tạo lại 2 lịch tự động theo content/editorial/routines/ và gắn vào phiên này.
