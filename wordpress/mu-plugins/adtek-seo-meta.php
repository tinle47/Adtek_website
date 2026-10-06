<?php
/**
 * Plugin Name: Adtek SEO Meta REST
 * Description: Cho phép đọc và sửa SEO title, meta description, noindex của Yoast qua REST API (bài viết, trang, chuyên mục; chỉ người có quyền sửa).
 * Version:     1.3.1
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

/*
 * Sitemap đa ngôn ngữ (WPML + Yoast): sitemap đang liệt kê cả bài tiếng Việt và tiếng Anh
 * nhưng gán mọi URL theo ngôn ngữ đang xem, nên URL bị trùng và bản /en/ biến mất.
 * Ghi lại URL của từng mục theo đúng ngôn ngữ của bài đó.
 */
add_filter(
	'wpseo_sitemap_entry',
	static function ( $url, $type, $post ) {
		if ( 'post' !== $type || empty( $post->ID ) || empty( $url['loc'] ) ) {
			return $url;
		}
		$details = apply_filters( 'wpml_post_language_details', null, $post->ID );
		if ( empty( $details['language_code'] ) ) {
			return $url;
		}
		$url['loc'] = apply_filters( 'wpml_permalink', get_permalink( $post->ID ), $details['language_code'], true );
		return $url;
	},
	20,
	3
);

/*
 * SEO title và meta description của chuyên mục (Yoast lưu trong option riêng, không phải term meta):
 * mở qua trường REST "adtek_seo" = { title, desc } trên endpoint categories.
 */
add_action(
	'rest_api_init',
	static function () {
		register_rest_field(
			'category',
			'adtek_seo',
			array(
				'get_callback'    => static function ( $term ) {
					if ( ! class_exists( 'WPSEO_Taxonomy_Meta' ) ) {
						return null;
					}
					return array(
						'title' => (string) WPSEO_Taxonomy_Meta::get_term_meta( $term['id'], 'category', 'title' ),
						'desc'  => (string) WPSEO_Taxonomy_Meta::get_term_meta( $term['id'], 'category', 'desc' ),
					);
				},
				'update_callback' => static function ( $value, $term ) {
					if ( ! class_exists( 'WPSEO_Taxonomy_Meta' ) || ! current_user_can( 'manage_categories' ) ) {
						return new WP_Error( 'adtek_seo_forbidden', 'Không thể cập nhật SEO chuyên mục.', array( 'status' => 403 ) );
					}
					// set_value() của Yoast thay cả bộ meta của term, nên gộp với dữ liệu đang có rồi lưu một lần.
					$option  = get_option( 'wpseo_taxonomy_meta' );
					$current = ( is_array( $option ) && isset( $option['category'][ $term->term_id ] ) && is_array( $option['category'][ $term->term_id ] ) )
						? $option['category'][ $term->term_id ]
						: array();
					foreach ( array( 'title' => 'wpseo_title', 'desc' => 'wpseo_desc' ) as $field => $key ) {
						if ( isset( $value[ $field ] ) ) {
							$current[ $key ] = sanitize_text_field( $value[ $field ] );
						}
					}
					if ( method_exists( 'WPSEO_Taxonomy_Meta', 'set_values' ) ) {
						WPSEO_Taxonomy_Meta::set_values( $term->term_id, 'category', $current );
					} else {
						$option = is_array( $option ) ? $option : array();
						$option['category'][ $term->term_id ] = $current;
						update_option( 'wpseo_taxonomy_meta', $option );
					}
					return true;
				},
				'schema'          => array( 'type' => 'object' ),
			)
		);
	}
);

