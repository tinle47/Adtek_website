<?php
/**
 * Plugin Name: Adtek Header Auth
 * Description: Cho phép đăng nhập REST API bằng Application Password qua header X-Adtek-Auth, vì hosting loại bỏ header Authorization từ kết nối bên ngoài.
 * Version:     1.0.0
 * Author:      Adtek
 *
 * Cách dùng: gửi header "X-Adtek-Auth: <base64 của username:application-password>".
 * Plugin chỉ chuyển giá trị này vào chỗ WordPress vẫn đọc khi có Basic Auth.
 * Việc kiểm tra mật khẩu, quyền hạn và thu hồi vẫn do WordPress core xử lý.
 */

defined( 'ABSPATH' ) || exit;

if ( ! empty( $_SERVER['HTTP_X_ADTEK_AUTH'] ) && ! isset( $_SERVER['PHP_AUTH_USER'] ) ) {
	$adtek_credentials = base64_decode( $_SERVER['HTTP_X_ADTEK_AUTH'], true );

	if ( false !== $adtek_credentials && false !== strpos( $adtek_credentials, ':' ) ) {
		list( $_SERVER['PHP_AUTH_USER'], $_SERVER['PHP_AUTH_PW'] ) = explode( ':', $adtek_credentials, 2 );

		// Báo cho client biết header đã tới được WordPress (không chứa thông tin nhạy cảm).
		add_filter(
			'rest_post_dispatch',
			static function ( $response ) {
				$response->header( 'X-Adtek-Auth-Received', '1' );
				return $response;
			}
		);
	}

	unset( $adtek_credentials );
}
