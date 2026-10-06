# Adtek Website

Mã nguồn và công cụ quản lý website https://adtek.agency (WordPress trên hosting Mắt Bão, Plesk + LiteSpeed).

## wordpress/mu-plugins/adtek-header-auth.php

Hosting loại bỏ header `Authorization` từ kết nối bên ngoài, nên Application Password không đăng nhập được qua REST API. Plugin này cho phép gửi cùng thông tin đó qua header `X-Adtek-Auth`.

- Giá trị header: base64 của `username:application-password`.
- WordPress core vẫn kiểm tra mật khẩu, quyền hạn và việc thu hồi như bình thường.
- Khi header tới được WordPress, response có thêm `X-Adtek-Auth-Received: 1`.

Cài đặt: upload file vào `httpdocs/wp-content/mu-plugins/` (tạo thư mục nếu chưa có). Plugin tự kích hoạt, xem tại Plugins > Must-Use.

## wordpress/mu-plugins/adtek-performance.php

Tăng điểm Google PageSpeed (nhất là trên di động) bằng cách sửa HTML trước khi gửi cho trình duyệt. Không đổi dữ liệu, không sửa theme.

| Việc plugin làm | Vì sao |
|---|---|
| Gộp các file CSS liền nhau thành 1 file rút gọn, nhúng sẵn các `@import` | Trước đây ~20 file CSS tải nối tiếp nhau, màn hình trắng tới khi tải xong hết |
| Font Roboto/Oswald dùng bản rút gọn chỉ giữ Latin + tiếng Việt (66 KB còn 14 KB mỗi file) | Font gốc chứa cả chữ Cyrillic, Hy Lạp không dùng tới |
| Font Awesome tải nền và chỉ giữ icon đang dùng (500 KB còn khoảng 6-27 KB) | Bản Pro 6 chứa hàng nghìn icon, chặn hiển thị trang |
| Ảnh chính màn hình đầu (banner, ảnh đầu bài) được ưu tiên tải; ảnh phía dưới lazy-load | WordPress đang ưu tiên nhầm logo, ảnh chính phải chờ |
| Bỏ jQuery nạp trùng trong `<head>` ở trang con, thêm `defer` cho thư viện JS của theme | jQuery bị tải hai lần và chặn hiển thị |
| Crisp chat chỉ tải khi người dùng cuộn, chạm hoặc di chuột | Giảm JavaScript bên thứ ba lúc tải trang |
| Tắt hiệu ứng AOS trên di động (màn hình dưới 768px) | AOS ẩn nội dung tới khi JavaScript chạy xong, màn hình di động trắng vài giây |
| Tắt script emoji của WordPress | Không cần với trình duyệt hiện nay |

File CSS gộp nằm trong `wp-content/uploads/adtek-perf/`, tự tạo lại khi file nguồn thay đổi. Nếu có lỗi bất kỳ, plugin trả nguyên HTML gốc.

Cài đặt: giải nén `deploy/adtek-performance.zip` vào `httpdocs/wp-content/` (ghi đè), để có:

```
wp-content/mu-plugins/adtek-performance.php
wp-content/mu-plugins/adtek-performance/fonts/*.woff2
```

Lần đầu chạy, plugin tự xóa cache trang của WP-Optimize. Kiểm tra: mở trang chủ, xem mã nguồn có `adtek-perf-css-1`.

Tùy chọn (thêm vào `wp-config.php`):

- `define( 'ADTEK_PERF_DISABLE', true );` tắt toàn bộ plugin.
- `define( 'ADTEK_PERF_DELAY_TAGS', true );` hoãn cả Google Tag Manager và gtag tới khi người dùng tương tác. Điểm cao hơn, nhưng có thể mất số liệu của người vào rồi thoát ngay mà không chạm màn hình.
- `define( 'ADTEK_PERF_KEEP_AOS_MOBILE', true );` giữ hiệu ứng AOS trên di động.

Xem trang gốc để so sánh: thêm `?adtek_perf=0` vào URL. Gỡ bỏ: xóa file và thư mục trên rồi bấm Purge cache trong WP-Optimize.

Font rút gọn được tạo bằng `python3 tools/subset_fonts.py`.
