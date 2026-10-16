<?php
/**
 * Plugin Name: Adtek ACF REST
 * Description: Đọc và ghi trường ACF của trang/bài qua REST API, dùng để cập nhật nội dung trang chủ (vi + en) mà không cần vào wp-admin. Chỉ người có quyền sửa bài mới dùng được.
 * Version:     1.2.0
 * Author:      Adtek
 */

defined( 'ABSPATH' ) || exit;

/*
 * REST: GET  /wp-json/adtek/v1/acf/<id> trả toàn bộ trường ACF của bài.
 *       POST /wp-json/adtek/v1/acf/<id> với {"fields": {"tên_trường": giá_trị, ...}} ghi từng trường
 *       (nhóm và repeater truyền dạng mảng theo tên trường con), trả lại dữ liệu sau khi ghi.
 *       POST với {"purge": true} và không có fields: chỉ xóa cache trang.
 */

/*
 * Các link cần xóa cache của bài. Trang chủ có link riêng (/en/homepage/) khác link khách thật sự mở (/en/),
 * nên khi bài là trang chủ của ngôn ngữ nào thì thêm link trang chủ của ngôn ngữ đó.
 */
function adtek_acf_rest_purge_urls( $id ) {
	$urls  = array( get_permalink( $id ) );
	$front = (int) get_option( 'page_on_front' );
	$lang  = apply_filters( 'wpml_element_language_code', null, array( 'element_id' => $id, 'element_type' => get_post_type( $id ) ) );
	if ( $front && $lang ) {
		// Bản dịch của trang chủ sang đúng ngôn ngữ của bài đang sửa.
		$front = (int) apply_filters( 'wpml_object_id', $front, 'page', false, $lang );
	}
	if ( $front && $front === $id ) {
		$urls[] = $lang ? apply_filters( 'wpml_permalink', home_url( '/' ), $lang, true ) : home_url( '/' );
	}
	return array_values( array_unique( array_filter( $urls ) ) );
}

/*
 * Xóa cache trang theo đúng link của bài. WP-Optimize chỉ tự xóa trang chủ ngôn ngữ mặc định,
 * trang chủ tiếng Anh (/en/) phải xóa theo URL.
 */
function adtek_acf_rest_purge( $id ) {
	clean_post_cache( $id );
	do_action( 'litespeed_purge_post', $id );
	$urls = adtek_acf_rest_purge_urls( $id );
	if ( class_exists( 'WPO_Page_Cache' ) ) {
		if ( method_exists( 'WPO_Page_Cache', 'delete_single_post_cache' ) ) {
			WPO_Page_Cache::delete_single_post_cache( $id );
		}
		if ( method_exists( 'WPO_Page_Cache', 'delete_cache_by_url' ) ) {
			foreach ( $urls as $url ) {
				WPO_Page_Cache::delete_cache_by_url( $url );
			}
		}
	}
	return $urls;
}
add_action(
	'rest_api_init',
	static function () {
		$can_edit = static function ( $request ) {
			return current_user_can( 'edit_post', (int) $request['id'] );
		};
		register_rest_route(
			'adtek/v1',
			'/acf/(?P<id>\d+)',
			array(
				array(
					'methods'             => 'GET',
					'permission_callback' => $can_edit,
					'callback'            => static function ( $request ) {
						if ( ! function_exists( 'get_fields' ) ) {
							return new WP_Error( 'no_acf', 'ACF chưa bật.', array( 'status' => 500 ) );
						}
						$id = (int) $request['id'];
						if ( ! get_post( $id ) ) {
							return new WP_Error( 'not_found', 'Không có bài này.', array( 'status' => 404 ) );
						}
						return array(
							'id'      => $id,
							'fields'  => get_fields( $id ) ?: new stdClass(),
							'version' => '1.2.0',
						);
					},
				),
				array(
					'methods'             => 'POST',
					'permission_callback' => $can_edit,
					'callback'            => static function ( $request ) {
						if ( ! function_exists( 'update_field' ) ) {
							return new WP_Error( 'no_acf', 'ACF chưa bật.', array( 'status' => 500 ) );
						}
						$id     = (int) $request['id'];
						$fields = $request['fields'];
						if ( ! get_post( $id ) ) {
							return new WP_Error( 'not_found', 'Không có bài này.', array( 'status' => 404 ) );
						}
						if ( ! $fields && $request['purge'] ) {
							return array(
								'id'      => $id,
								'purged'  => adtek_acf_rest_purge( $id ),
								'version' => '1.2.0',
							);
						}
						if ( ! is_array( $fields ) || ! $fields ) {
							return new WP_Error( 'bad_request', 'Thiếu fields.', array( 'status' => 400 ) );
						}
						$result = array();
						foreach ( $fields as $name => $value ) {
							// Chỉ ghi trường đã khai báo trong ACF, tránh tạo meta rác do gõ sai tên.
							$field = get_field_object( $name, $id ) ?: acf_get_field( $name );
							if ( ! $field ) {
								$result[ $name ] = 'unknown_field';
								continue;
							}
							// Ghi theo field key để ACF nhận đúng cấu trúc nhóm/repeater cả khi bài chưa từng lưu trường này.
							$result[ $name ] = update_field( $field['key'], $value, $id ) ? 'ok' : 'unchanged';
						}
						$purged = adtek_acf_rest_purge( $id );
						return array(
							'id'      => $id,
							'result'  => $result,
							'purged'  => $purged,
							'fields'  => get_fields( $id ) ?: new stdClass(),
							'version' => '1.2.0',
						);
					},
				),
			)
		);
	}
);
