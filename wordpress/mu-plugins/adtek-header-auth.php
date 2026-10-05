<?php
/**
 * Plugin Name: Adtek Header Auth
 * Description: Cho phép đăng nhập REST API bằng Application Password qua header X-Adtek-Auth, vì hosting loại bỏ header Authorization từ kết nối bên ngoài.
 * Version:     1.1.0
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

		// WordPress chỉ chấp nhận Application Password khi biết đây là request REST API.
		// Nếu một plugin (ví dụ WPML) xác định user quá sớm, hằng REST_REQUEST chưa có và
		// mật khẩu bị bỏ qua. Nhận diện request REST qua đường dẫn để tránh trường hợp này.
		$adtek_uri = isset( $_SERVER['REQUEST_URI'] ) ? $_SERVER['REQUEST_URI'] : '';
		if ( false !== strpos( $adtek_uri, '/wp-json/' ) || isset( $_GET['rest_route'] ) ) {
			add_filter( 'application_password_is_api_request', '__return_true' );
		}
		unset( $adtek_uri );

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
