<?php
/**
 * Plugin Name: Adtek SEO Meta REST
 * Description: Cho phép đọc và sửa SEO title, meta description, noindex của Yoast qua REST API (chỉ người có quyền sửa bài).
 * Version:     1.0.0
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
