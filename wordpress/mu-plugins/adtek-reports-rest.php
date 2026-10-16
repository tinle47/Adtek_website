<?php
/**
 * Plugin Name: Adtek Reports REST
 * Description: Mở 3 bộ lọc của mục Reports (Category, Field, Year) qua REST API để tạo và gắn báo cáo cho Trung Tâm Tài Nguyên mà không cần vào wp-admin. Quyền tạo/gắn giữ nguyên như trong wp-admin.
 * Version:     1.0.0
 * Author:      Adtek
 */

defined( 'ABSPATH' ) || exit;

/*
 * Theme đăng ký category_reports, field_reports, year_reports mà không bật show_in_rest,
 * nên REST không đọc, tạo hay gắn được các bộ lọc này cho bài mona_reports.
 * Bật show_in_rest cho 3 taxonomy:
 *   GET/POST /wp-json/wp/v2/category_reports, /field_reports, /year_reports  (đọc, tạo term)
 *   POST /wp-json/wp/v2/mona_reports/<id> với {"category_reports": [id], "field_reports": [id], "year_reports": [id]}
 * File PDF (trường ACF mona_report_file) ghi qua /wp-json/adtek/v1/acf/<id> của plugin adtek-acf-rest.
 */
add_filter(
	'register_taxonomy_args',
	function ( $args, $taxonomy ) {
		if ( in_array( $taxonomy, array( 'category_reports', 'field_reports', 'year_reports' ), true ) ) {
			$args['show_in_rest'] = true;
		}
		return $args;
	},
	10,
	2
);
