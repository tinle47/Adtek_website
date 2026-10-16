<?php
/**
 * Plugin Name: Adtek Yoast Settings REST
 * Description: Đọc và sửa cấu hình Yoast SEO, cài đặt SEO của WPML và hồ sơ mạng xã hội của tác giả qua REST (chỉ quản trị viên).
 * Version:     1.0.0
 * Author:      Adtek
 */

defined( 'ABSPATH' ) || exit;

/*
 * GET  /wp-json/adtek/v1/yoast-settings
 *      Trả toàn bộ cấu hình Yoast (WPSEO_Options::get_all), cài đặt SEO của WPML và phiên bản plugin.
 * POST /wp-json/adtek/v1/yoast-settings
 *      { "settings": { "khóa_yoast": giá_trị }, "wpml_seo": { ... }, "user": { "id": 4, "meta": { ... } }, "purge": true }
 *      Chỉ ghi khóa Yoast đang tồn tại (gõ sai tên trả unknown_key), trả giá trị cũ và mới của từng khóa để lưu backup.
 */

function adtek_yoast_user_keys() {
	// Trường hồ sơ tác giả Yoast dùng cho schema Person (sameAs) và trang tác giả.
	return array( 'facebook', 'instagram', 'linkedin', 'myspace', 'pinterest', 'soundcloud', 'tumblr', 'twitter', 'youtube', 'wikipedia', 'adtek_job_title' );
}

function adtek_yoast_purge_all() {
	do_action( 'litespeed_purge_all' );
	if ( function_exists( 'WP_Optimize' ) && method_exists( WP_Optimize(), 'get_page_cache' ) ) {
		WP_Optimize()->get_page_cache()->purge();
	}
	wp_cache_flush();
}

add_action(
	'rest_api_init',
	static function () {
		$can = static function () {
			return current_user_can( 'manage_options' );
		};

		register_rest_route(
			'adtek/v1',
			'/yoast-settings',
			array(
				array(
					'methods'             => 'GET',
					'permission_callback' => $can,
					'callback'            => static function () {
						if ( ! class_exists( 'WPSEO_Options' ) ) {
							return new WP_Error( 'no_yoast', 'Yoast SEO chưa bật.', array( 'status' => 500 ) );
						}
						$wpml  = get_option( 'icl_sitepress_settings' );
						$users = array();
						foreach ( get_users( array( 'has_published_posts' => array( 'post' ), 'fields' => array( 'ID', 'display_name' ) ) ) as $u ) {
							$meta = array( 'description' => get_the_author_meta( 'description', $u->ID ) );
							foreach ( adtek_yoast_user_keys() as $k ) {
								$meta[ $k ] = get_user_meta( $u->ID, $k, true );
							}
							$users[] = array( 'id' => (int) $u->ID, 'name' => $u->display_name, 'meta' => $meta );
						}
						return array(
							'version'  => '1.0.0',
							'yoast'    => defined( 'WPSEO_VERSION' ) ? WPSEO_VERSION : null,
							'settings' => WPSEO_Options::get_all(),
							'wpml_seo' => ( is_array( $wpml ) && isset( $wpml['seo'] ) ) ? $wpml['seo'] : null,
							'authors'  => $users,
						);
					},
				),
				array(
					'methods'             => 'POST',
					'permission_callback' => $can,
					'callback'            => static function ( $request ) {
						if ( ! class_exists( 'WPSEO_Options' ) ) {
							return new WP_Error( 'no_yoast', 'Yoast SEO chưa bật.', array( 'status' => 500 ) );
						}
						$out = array( 'version' => '1.0.0' );

						$settings = $request['settings'];
						if ( is_array( $settings ) ) {
							$all = WPSEO_Options::get_all();
							foreach ( $settings as $key => $value ) {
								if ( ! array_key_exists( $key, $all ) ) {
									$out['settings'][ $key ] = 'unknown_key';
									continue;
								}
								$old = $all[ $key ];
								WPSEO_Options::set( $key, $value );
								$out['settings'][ $key ] = array( 'old' => $old, 'new' => WPSEO_Options::get( $key ) );
							}
						}

						$wpml_seo = $request['wpml_seo'];
						if ( is_array( $wpml_seo ) ) {
							$wpml = get_option( 'icl_sitepress_settings' );
							if ( ! is_array( $wpml ) ) {
								$out['wpml_seo'] = 'no_wpml';
							} else {
								$old         = isset( $wpml['seo'] ) && is_array( $wpml['seo'] ) ? $wpml['seo'] : array();
								$wpml['seo'] = array_merge( $old, $wpml_seo );
								update_option( 'icl_sitepress_settings', $wpml );
								$out['wpml_seo'] = array( 'old' => $old, 'new' => $wpml['seo'] );
							}
						}

						$user = $request['user'];
						if ( is_array( $user ) && ! empty( $user['id'] ) && is_array( $user['meta'] ?? null ) ) {
							$id = (int) $user['id'];
							foreach ( $user['meta'] as $key => $value ) {
								if ( 'description' === $key ) {
									$old = get_the_author_meta( 'description', $id );
									wp_update_user( array( 'ID' => $id, 'description' => wp_kses_post( $value ) ) );
								} elseif ( in_array( $key, adtek_yoast_user_keys(), true ) ) {
									$old   = get_user_meta( $id, $key, true );
									$value = 'adtek_job_title' === $key ? sanitize_text_field( $value ) : esc_url_raw( $value );
									update_user_meta( $id, $key, $value );
								} else {
									$out['user'][ $key ] = 'unknown_key';
									continue;
								}
								$out['user'][ $key ] = array( 'old' => $old, 'new' => $value );
							}
						}

						if ( $request['purge'] ) {
							adtek_yoast_purge_all();
							$out['purged'] = true;
						}
						return $out;
					},
				),
			)
		);
	}
);
