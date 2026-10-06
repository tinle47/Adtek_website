<?php
/**
 * Plugin Name: Adtek Public Preview
 * Description: Link xem trước bản nháp không cần đăng nhập, có mã bí mật và hạn dùng (mặc định 7 ngày). Link do REST API tạo, chỉ người có quyền sửa bài mới tạo được.
 * Version:     1.0.0
 * Author:      Adtek
 */

defined( 'ABSPATH' ) || exit;

const ADTEK_PREVIEW_KEY     = '_adtek_preview_key';
const ADTEK_PREVIEW_EXPIRES = '_adtek_preview_expires';

/*
 * REST: POST /wp-json/adtek/v1/preview/<id> tạo mã mới (tham số days, mặc định 7) và trả link.
 *       DELETE /wp-json/adtek/v1/preview/<id> thu hồi link.
 */
add_action(
	'rest_api_init',
	static function () {
		register_rest_route(
			'adtek/v1',
			'/preview/(?P<id>\d+)',
			array(
				array(
					'methods'             => 'POST',
					'permission_callback' => static function ( $request ) {
						return current_user_can( 'edit_post', (int) $request['id'] );
					},
					'callback'            => static function ( $request ) {
						$id   = (int) $request['id'];
						$days = max( 1, min( 30, (int) ( $request['days'] ?? 7 ) ) );
						if ( ! get_post( $id ) ) {
							return new WP_Error( 'not_found', 'Không có bài này.', array( 'status' => 404 ) );
						}
						$key     = wp_generate_password( 24, false );
						$expires = time() + $days * DAY_IN_SECONDS;
						update_post_meta( $id, ADTEK_PREVIEW_KEY, $key );
						update_post_meta( $id, ADTEK_PREVIEW_EXPIRES, $expires );
						return array(
							'url'     => add_query_arg(
								array(
									'p'             => $id,
									'preview'       => 'true',
									'adtek_preview' => $key,
								),
								home_url( '/' )
							),
							'expires' => gmdate( 'c', $expires ),
							'version' => '1.0.0',
						);
					},
				),
				array(
					'methods'             => 'DELETE',
					'permission_callback' => static function ( $request ) {
						return current_user_can( 'edit_post', (int) $request['id'] );
					},
					'callback'            => static function ( $request ) {
						delete_post_meta( (int) $request['id'], ADTEK_PREVIEW_KEY );
						delete_post_meta( (int) $request['id'], ADTEK_PREVIEW_EXPIRES );
						return array( 'deleted' => true );
					},
				),
			)
		);
	}
);

/** Mã trên URL có khớp với bài và còn hạn không. */
function adtek_preview_valid( $post_id ) {
	if ( empty( $_GET['adtek_preview'] ) || ! is_string( $_GET['adtek_preview'] ) ) {
		return false;
	}
	$key     = get_post_meta( $post_id, ADTEK_PREVIEW_KEY, true );
	$expires = (int) get_post_meta( $post_id, ADTEK_PREVIEW_EXPIRES, true );
	return $key && $expires > time() && hash_equals( $key, wp_unslash( $_GET['adtek_preview'] ) );
}

/*
 * Khi mã hợp lệ, coi bản nháp, bài chờ duyệt hoặc bài đã hẹn giờ như bài đã đăng trong lượt xem này
 * (chỉ trong bộ nhớ, không đổi trạng thái thật trong cơ sở dữ liệu).
 */
add_filter(
	'posts_results',
	static function ( $posts, $query ) {
		if ( is_admin() || ! $query->is_main_query() || count( $posts ) !== 1 || empty( $_GET['adtek_preview'] ) ) {
			return $posts;
		}
		$post = $posts[0];
		if ( in_array( $post->post_status, array( 'draft', 'pending', 'future' ), true ) && adtek_preview_valid( $post->ID ) ) {
			$post->post_status = 'publish';
			$GLOBALS['adtek_is_public_preview'] = true;
		}
		return $posts;
	},
	10,
	2
);

/* Trang xem trước: không lập chỉ mục, không lưu bộ nhớ đệm (kể cả LiteSpeed Cache). */
add_action(
	'template_redirect',
	static function () {
		if ( empty( $GLOBALS['adtek_is_public_preview'] ) ) {
			return;
		}
		nocache_headers();
		header( 'X-Robots-Tag: noindex, nofollow', true );
		do_action( 'litespeed_control_set_nocache', 'adtek public preview' );
		add_filter( 'wp_robots', 'wp_robots_no_robots' );
		add_filter( 'wpseo_robots', static fn() => 'noindex, nofollow' );
	}
);
