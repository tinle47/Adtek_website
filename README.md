# Adtek Website

Mã nguồn và công cụ quản lý website https://adtek.agency (WordPress trên hosting Mắt Bão, Plesk + LiteSpeed).

## wordpress/mu-plugins/adtek-header-auth.php

Hosting loại bỏ header `Authorization` từ kết nối bên ngoài, nên Application Password không đăng nhập được qua REST API. Plugin này cho phép gửi cùng thông tin đó qua header `X-Adtek-Auth`.

- Giá trị header: base64 của `username:application-password`.
- WordPress core vẫn kiểm tra mật khẩu, quyền hạn và việc thu hồi như bình thường.
- Khi header tới được WordPress, response có thêm `X-Adtek-Auth-Received: 1`.

Cài đặt: upload file vào `httpdocs/wp-content/mu-plugins/` (tạo thư mục nếu chưa có). Plugin tự kích hoạt, xem tại Plugins > Must-Use.
