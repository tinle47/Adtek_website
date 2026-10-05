<?php
/**
 * Plugin Name: Adtek SEO Meta REST
 * Description: Cho phép đọc và sửa SEO title, meta description, noindex của Yoast qua REST API (chỉ người có quyền sửa bài).
 * Version:     1.1.0
 * Author:      Adtek
 */

defined( 'ABSPATH' ) || exit;

add_action(
	'init',
	static function () {
		$post_types = array( 'post', 'page', 'mona_solution', 'mona_glossary', 'mona_reports', 'mona_recruitment', 'mona_case_study' );
		$keys       = array( '_yoast_wpseo_title', '_yoast_wpseo_metadesc', '_yoast_wpseo_meta-robots-noindex' );

		foreach ( $post_types as $post_type ) {
			foreach ( $keys as $key ) {
				register_post_meta(
					$post_type,
					$key,
					array(
						'type'          => 'string',
						'single'        => true,
						'show_in_rest'  => true,
						'auth_callback' => static function ( $allowed, $meta_key, $post_id ) {
							return current_user_can( 'edit_post', $post_id );
						},
					)
				);
			}
		}
	},
	20
);

/*
 * Trang lưu trữ (archive) của các loại nội dung tùy chỉnh đang để trống vì archive.php của theme
 * không hiển thị gì: bỏ khỏi sitemap và đánh dấu noindex để Google không lập chỉ mục trang trống.
 */
function adtek_empty_archive_types() {
	return array( 'mona_glossary', 'mona_reports', 'mona_recruitment', 'mona_solution', 'mona_case_study', 'mona_ecommerce', 'mona_team' );
}

add_filter(
	'wpseo_sitemap_post_type_archive_link',
	static function ( $link, $post_type ) {
		return in_array( $post_type, adtek_empty_archive_types(), true ) ? false : $link;
	},
	10,
	2
);

add_filter(
	'wpseo_robots',
	static function ( $robots ) {
		return is_post_type_archive( adtek_empty_archive_types() ) ? 'noindex, follow' : $robots;
	}
);

