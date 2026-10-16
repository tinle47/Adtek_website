# Adtek Website

Mã nguồn và công cụ quản lý website https://adtek.agency (WordPress trên hosting Mắt Bão, Plesk + LiteSpeed).

## wordpress/mu-plugins/adtek-header-auth.php

Hosting loại bỏ header `Authorization` từ kết nối bên ngoài, nên Application Password không đăng nhập được qua REST API. Plugin này cho phép gửi cùng thông tin đó qua header `X-Adtek-Auth`.

- Giá trị header: base64 của `username:application-password`.
- WordPress core vẫn kiểm tra mật khẩu, quyền hạn và việc thu hồi như bình thường.
- Khi header tới được WordPress, response có thêm `X-Adtek-Auth-Received: 1`.

Cài đặt: upload file vào `httpdocs/wp-content/mu-plugins/` (tạo thư mục nếu chưa có). Plugin tự kích hoạt, xem tại Plugins > Must-Use.

## wordpress/mu-plugins/adtek-public-preview.php

Tạo link xem trước bản nháp không cần đăng nhập, dùng trong email nhắc duyệt bài (`tools/approval_email.py`).

- `POST /wp-json/adtek/v1/preview/<id>` (tham số `days`, mặc định 7, tối đa 30) trả link dạng `https://adtek.agency/?p=<id>&preview=true&adtek_preview=<mã>`. Chỉ tài khoản có quyền sửa bài mới tạo được.
- `DELETE /wp-json/adtek/v1/preview/<id>` thu hồi link.
- Link chỉ hiện bài nháp, chờ duyệt hoặc đã hẹn giờ khi mã khớp và còn hạn. Trang xem trước có noindex, không lưu cache (kể cả LiteSpeed Cache).

Cài đặt: upload file vào `httpdocs/wp-content/mu-plugins/`. Khi chưa cài, email tự dùng link xem trước cần đăng nhập.

## wordpress/mu-plugins/adtek-acf-rest.php

Đọc và ghi trường ACF của trang/bài qua REST, dùng cho nội dung trang chủ (mẫu Home V2).

- `GET /wp-json/adtek/v1/acf/<id>` trả toàn bộ trường ACF.
- `POST /wp-json/adtek/v1/acf/<id>` với `{"fields": {"tên_trường": giá_trị}}` ghi từng trường (nhóm, repeater truyền dạng mảng), trả kết quả từng trường và dữ liệu sau khi ghi. Tên trường không có trong ACF bị bỏ qua (`unknown_field`).
- `POST` với `{"purge": true}` (không kèm fields) chỉ xóa cache trang. Từ bản 1.1.0, mỗi lần ghi đều xóa cache WP-Optimize theo đúng link của trang (WP-Optimize không tự xóa trang chủ `/en/`). Từ bản 1.2.1, trang chủ của mỗi ngôn ngữ được xóa thêm theo link khách mở (`/`, `/en/`), trường `purged` trả danh sách link đã xóa.
- Chỉ tài khoản có quyền sửa bài dùng được.

Đồng bộ trang chủ EN theo bản VI: sửa chữ trong `content/pages/home.json`, chạy `python3 tools/sync_home.py` (chạy thử) rồi `--apply`.

## Lưu ý khi sửa trang tiếng Anh qua REST

Lưu nội dung một trang bản dịch (POST `/wp/v2/pages/<id>` với `content`) có thể làm WPML đặt lại slug theo bản tiếng Việt, ví dụ trang 5242 từ `press` thành `bao-chi` khiến `/en/press/` trả 404. Sau mỗi lần ghi trang EN, đọc lại `link` và nếu slug đổi thì gửi lại `{"slug": "<slug cũ>"}`. Ghi riêng `meta` không gặp lỗi này.

## wordpress/mu-plugins/adtek-yoast-settings.php

Đọc và sửa cấu hình Yoast SEO qua REST (Yoast không có API cấu hình), dùng cho phiên Adtek - SEO. Chỉ quản trị viên dùng được.

- `GET /wp-json/adtek/v1/yoast-settings` trả toàn bộ cấu hình Yoast (`WPSEO_Options::get_all`), cài đặt SEO của WPML (`icl_sitepress_settings['seo']`, gồm hreflang) và hồ sơ tác giả (tiểu sử, `adtek_job_title`, LinkedIn và các mạng xã hội Yoast dùng cho schema Person).
- `POST` với `{"settings": {...}, "wpml_seo": {...}, "user": {"id": 4, "meta": {...}}, "purge": true}`: chỉ ghi khóa đã tồn tại (gõ sai trả `unknown_key`), trả giá trị cũ và mới của từng khóa để lưu backup; `purge` xóa toàn bộ cache LiteSpeed và WP-Optimize.

Cài đặt: upload file vào `httpdocs/wp-content/mu-plugins/`. Đi kèm `wordpress/themes/monatheme/author.php` (trang tác giả, upload vào `httpdocs/wp-content/themes/monatheme/`).

## video/

Hệ thống tạo video infographic TikTok từ bài blog (Remotion + giọng ElevenLabs). Xem `video/README.md`.
