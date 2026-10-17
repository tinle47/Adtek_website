<?php
/**
 * Plugin Name: Adtek Yoast Settings REST
 * Description: Đọc và sửa cấu hình Yoast SEO, cài đặt SEO của WPML và hồ sơ mạng xã hội của tác giả qua REST (chỉ quản trị viên); phục vụ /llms.txt tiếng Việt thay cho file của Yoast; chuyển hướng 301 và nối bản dịch WPML.
 * Version:     1.2.0
 * Author:      Adtek
 */

defined( 'ABSPATH' ) || exit;

/*
 * GET  /wp-json/adtek/v1/yoast-settings
 *      Trả toàn bộ cấu hình Yoast (WPSEO_Options::get_all), cài đặt SEO của WPML và phiên bản plugin.
 * POST /wp-json/adtek/v1/yoast-settings
 *      { "settings": { "khóa_yoast": giá_trị }, "wpml_seo": { ... }, "user": { "id": 4, "meta": { ... } }, "purge": true }
 *      Chỉ ghi khóa Yoast đang tồn tại (gõ sai tên trả unknown_key), trả giá trị cũ và mới của từng khóa để lưu backup.
 *      Thêm "llms": { "pillars": [ID bài trụ cột] } và "llms_cleanup": true (xóa file llms.txt cũ do Yoast tạo, chỉ khi đã tắt llms.txt của Yoast).
 *
 * /llms.txt (từ 1.1.0): file của Yoast bị ghi 2 lần nối nhau khi chạy cùng WPML, nên tắt llms.txt của Yoast
 * và để plugin này tạo nội dung tiếng Việt từ dữ liệu WordPress, lưu đệm 12 giờ, làm mới khi có bài đăng hoặc cập nhật.
 *
 * Từ 1.2.0:
 *      "redirects": { "/glossary/cpm-2/": "/glossary/cpm/", "/cu/": null } thêm hoặc xóa (null) chuyển hướng 301, lưu ở option adtek_redirects.
 *      Thay cho plugin redirect riêng: chỉ nhận đường dẫn nội bộ bắt đầu bằng /.
 *      "wpml_link": { "id": 123, "translation_of": 11, "lang": "vi" } nối trang 123 làm bản dịch ngôn ngữ lang của trang 11.
 */

const ADTEK_LLMS_CACHE = 'adtek_llms_txt_v3';

function adtek_llms_md( $text ) {
	// Tiêu đề và mô tả nằm trong cú pháp link Markdown: bỏ ngoặc vuông, gộp khoảng trắng.
	$text = html_entity_decode( wp_strip_all_tags( (string) $text ), ENT_QUOTES, 'UTF-8' );
	return trim( preg_replace( '/\s+/u', ' ', str_replace( array( '[', ']' ), array( '(', ')' ), $text ) ) );
}

function adtek_llms_desc( $post ) {
	$desc = get_post_meta( $post->ID, '_yoast_wpseo_metadesc', true );
	if ( ! $desc ) {
		$desc = has_excerpt( $post ) ? $post->post_excerpt : wp_trim_words( strip_shortcodes( $post->post_content ), 30, '' );
	}
	$desc = adtek_llms_md( $desc );
	if ( mb_strlen( $desc ) > 220 ) {
		$desc = rtrim( mb_substr( $desc, 0, 217 ), ' ,.;:' ) . '...';
	}
	return $desc ? ': ' . $desc : '';
}

function adtek_llms_line( $post, $title = null ) {
	return '- [' . adtek_llms_md( $title ? $title : get_the_title( $post ) ) . '](' . get_permalink( $post ) . ')' . adtek_llms_desc( $post );
}

function adtek_llms_page( $slug ) {
	// get_page_by_path không qua bộ lọc WPML: bản EN có thể trùng slug, nên quy về bản tiếng Việt.
	$page = get_page_by_path( $slug );
	if ( ! $page ) {
		return null;
	}
	$vi   = (int) apply_filters( 'wpml_object_id', $page->ID, 'page', true, 'vi' );
	$page = $vi ? get_post( $vi ) : $page;
	return ( $page && 'publish' === $page->post_status ) ? $page : null;
}

function adtek_llms_build() {
	// /llms.txt không thuộc thư mục ngôn ngữ nào nên WPML có thể chạy ở ngữ cảnh tiếng Anh: ép tiếng Việt khi lấy dữ liệu,
	// dùng get_option( 'home' ) (không qua bộ lọc ngôn ngữ của WPML) để dựng link trang chủ và bản tiếng Anh.
	do_action( 'wpml_switch_language', 'vi' );
	$base  = trailingslashit( get_option( 'home' ) );
	$home  = $base;
	$lines = array(
		'# Adtek',
		'',
		'> Adtek là growth marketing agency tại Việt Nam, thành lập năm 2022, giúp thương hiệu tăng trưởng từ xây dựng thương hiệu đến doanh thu: Brand Commerce, quảng cáo hiệu suất, SEO và AI Search, dữ liệu và CRM, thương mại điện tử.',
		'',
		'Tệp này giúp các trợ lý AI nắm nội dung chính của adtek.agency. Nội dung tiếng Việt, bản tiếng Anh ở mục English.',
		'',
		'## Giới thiệu và liên hệ',
	);
	$intro = array( 'solutions', 'contact', 'bao-chi', 'faq', 'chinh-sach-bao-mat' );
	$lines[] = '- [Trang chủ Adtek](' . $home . '): Growth marketing agency, Brand Commerce, Lead Generation, SEO.';
	foreach ( $intro as $slug ) {
		$page = adtek_llms_page( $slug );
		if ( $page ) {
			$lines[] = adtek_llms_line( $page );
		}
	}

	$solutions = get_posts( array( 'post_type' => 'mona_solution', 'numberposts' => 30, 'orderby' => 'menu_order title', 'order' => 'ASC', 'suppress_filters' => false ) );
	if ( $solutions ) {
		$lines[] = '';
		$lines[] = '## Dịch vụ';
		foreach ( $solutions as $p ) {
			$lines[] = adtek_llms_line( $p );
		}
	}

	$pillar_ids = array_filter( array_map( 'intval', (array) get_option( 'adtek_llms_pillars', array() ) ) );
	$pillars    = $pillar_ids ? get_posts( array( 'post_type' => 'post', 'post__in' => $pillar_ids, 'orderby' => 'post__in', 'numberposts' => 20, 'suppress_filters' => false ) ) : array();
	if ( $pillars ) {
		$lines[] = '';
		$lines[] = '## Bài trụ cột';
		foreach ( $pillars as $p ) {
			$lines[] = adtek_llms_line( $p );
		}
	}

	$recent = get_posts( array( 'post_type' => 'post', 'numberposts' => 20, 'post__not_in' => $pillar_ids, 'suppress_filters' => false ) );
	if ( $recent ) {
		$lines[] = '';
		$lines[] = '## Bài mới';
		foreach ( $recent as $p ) {
			$lines[] = adtek_llms_line( $p );
		}
	}

	$reports = get_posts( array( 'post_type' => 'mona_reports', 'numberposts' => 20, 'suppress_filters' => false ) );
	if ( $reports ) {
		$lines[] = '';
		$lines[] = '## Báo cáo';
		foreach ( $reports as $p ) {
			$lines[] = adtek_llms_line( $p );
		}
	}

	$lines[] = '';
	$lines[] = '## Tài nguyên';
	foreach ( array( 'blog', 'resources-glossary', 'resources-report', 'vietnam-e-commerce-map' ) as $slug ) {
		$page = adtek_llms_page( $slug );
		if ( $page ) {
			$lines[] = adtek_llms_line( $page );
		}
	}

	$lines[] = '';
	$lines[] = '## English';
	$lines[] = '- [Adtek (English)](' . $base . 'en/): Growth marketing agency in Vietnam.';
	$lines[] = '- [Blog (English)](' . $base . 'en/blog/)';

	$lines[] = '';
	$lines[] = '## Optional';
	$lines[] = '- [Sitemap](' . $base . 'sitemap_index.xml)';
	return implode( "\n", $lines ) . "\n";
}

add_action(
	'parse_request',
	static function () {
		$path = wp_parse_url( isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '', PHP_URL_PATH );
		if ( '/llms.txt' !== $path ) {
			return;
		}
		$body = get_transient( ADTEK_LLMS_CACHE );
		if ( false === $body ) {
			$body = adtek_llms_build();
			set_transient( ADTEK_LLMS_CACHE, $body, 12 * HOUR_IN_SECONDS );
		}
		do_action( 'litespeed_control_set_nocache', 'adtek llms.txt' );
		status_header( 200 );
		header( 'Content-Type: text/plain; charset=utf-8' );
		header( 'Cache-Control: public, max-age=3600' );
		header( 'X-Robots-Tag: noindex' );
		echo $body; // phpcs:ignore WordPress.Security.EscapeOutput -- văn bản thuần, đã lọc thẻ ở adtek_llms_md.
		exit;
	},
	0
);

add_action(
	'transition_post_status',
	static function ( $new, $old ) {
		if ( 'publish' === $new || 'publish' === $old ) {
			delete_transient( ADTEK_LLMS_CACHE );
		}
	},
	10,
	2
);

/*
 * Chuyển hướng 301 (từ 1.2.0): bản đồ đường dẫn lưu ở option adtek_redirects, sửa qua REST.
 * Chỉ đường dẫn nội bộ, so khớp đúng đường dẫn (bỏ query, chuẩn hóa dấu / cuối).
 */
function adtek_redirect_path( $path ) {
	$path = wp_parse_url( (string) $path, PHP_URL_PATH );
	if ( ! $path || '/' !== $path[0] || false !== strpos( $path, '//' ) ) {
		return '';
	}
	return trailingslashit( strtolower( rawurldecode( $path ) ) );
}

add_action(
	'template_redirect',
	static function () {
		$map = get_option( 'adtek_redirects', array() );
		if ( ! $map || ! is_array( $map ) ) {
			return;
		}
		$path = adtek_redirect_path( isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '' );
		if ( $path && isset( $map[ $path ] ) ) {
			// get_option( 'home' ) không qua bộ lọc ngôn ngữ của WPML: đích đã là đường dẫn đầy đủ (có /en/ nếu cần).
			wp_safe_redirect( untrailingslashit( get_option( 'home' ) ) . $map[ $path ], 301, 'Adtek' );
			exit;
		}
	},
	0
);

function adtek_yoast_user_keys() {
	// Trường hồ sơ tác giả Yoast dùng cho schema Person (sameAs) và trang tác giả.
	return array( 'facebook', 'instagram', 'linkedin', 'myspace', 'pinterest', 'soundcloud', 'tumblr', 'twitter', 'youtube', 'wikipedia', 'adtek_job_title', 'adtek_avatar_id' );
}

/*
 * Ảnh đại diện tác giả từ Thư viện (user meta adtek_avatar_id = ID ảnh) thay cho Gravatar.
 * Dùng cho trang tác giả và schema Person của Yoast (cả hai lấy qua get_avatar).
 */
add_filter(
	'pre_get_avatar_data',
	static function ( $args, $id_or_email ) {
		$user_id = 0;
		if ( is_numeric( $id_or_email ) ) {
			$user_id = (int) $id_or_email;
		} elseif ( $id_or_email instanceof WP_User ) {
			$user_id = $id_or_email->ID;
		} elseif ( $id_or_email instanceof WP_Post ) {
			$user_id = (int) $id_or_email->post_author;
		} elseif ( $id_or_email instanceof WP_Comment ) {
			$user_id = (int) $id_or_email->user_id;
		} elseif ( is_string( $id_or_email ) && is_email( $id_or_email ) ) {
			$u       = get_user_by( 'email', $id_or_email );
			$user_id = $u ? $u->ID : 0;
		}
		$media = $user_id ? (int) get_user_meta( $user_id, 'adtek_avatar_id', true ) : 0;
		if ( $media ) {
			$size = isset( $args['size'] ) ? (int) $args['size'] : 96;
			$src  = wp_get_attachment_image_src( $media, array( $size, $size ) );
			if ( $src ) {
				$args['url']          = $src[0];
				$args['found_avatar'] = true;
			}
		}
		return $args;
	},
	10,
	2
);

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
							'version'  => '1.2.0',
							'yoast'    => defined( 'WPSEO_VERSION' ) ? WPSEO_VERSION : null,
							'settings' => WPSEO_Options::get_all(),
							'wpml_seo' => ( is_array( $wpml ) && isset( $wpml['seo'] ) ) ? $wpml['seo'] : null,
							'authors'  => $users,
							'llms'     => array(
								'pillars'   => get_option( 'adtek_llms_pillars', array() ),
								'yoast_file' => file_exists( ABSPATH . 'llms.txt' ),
							),
							'redirects' => get_option( 'adtek_redirects', array() ),
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
						$out = array( 'version' => '1.2.0' );

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
									if ( 'adtek_job_title' === $key ) {
										$value = sanitize_text_field( $value );
									} elseif ( 'adtek_avatar_id' === $key ) {
										$value = absint( $value );
									} else {
										$value = esc_url_raw( $value );
									}
									update_user_meta( $id, $key, $value );
								} else {
									$out['user'][ $key ] = 'unknown_key';
									continue;
								}
								$out['user'][ $key ] = array( 'old' => $old, 'new' => $value );
							}
						}

						$llms = $request['llms'];
						if ( is_array( $llms ) && isset( $llms['pillars'] ) ) {
							$old = get_option( 'adtek_llms_pillars', array() );
							update_option( 'adtek_llms_pillars', array_values( array_filter( array_map( 'intval', (array) $llms['pillars'] ) ) ) );
							delete_transient( ADTEK_LLMS_CACHE );
							$out['llms'] = array( 'old' => $old, 'new' => get_option( 'adtek_llms_pillars' ) );
						}

						if ( $request['llms_cleanup'] ) {
							$file = ABSPATH . 'llms.txt';
							if ( WPSEO_Options::get( 'enable_llms_txt' ) ) {
								$out['llms_cleanup'] = 'yoast_llms_still_enabled';
							} elseif ( ! file_exists( $file ) ) {
								$out['llms_cleanup'] = 'no_file';
							} elseif ( false === strpos( (string) file_get_contents( $file ), 'Generated by Yoast SEO' ) ) {
								$out['llms_cleanup'] = 'not_yoast_file';
							} else {
								$out['llms_cleanup'] = wp_delete_file( $file ) || ! file_exists( $file ) ? 'deleted' : 'delete_failed';
							}
							delete_transient( ADTEK_LLMS_CACHE );
						}

						$redirects = $request['redirects'];
						if ( is_array( $redirects ) ) {
							$old = get_option( 'adtek_redirects', array() );
							$map = is_array( $old ) ? $old : array();
							foreach ( $redirects as $from => $to ) {
								$from = adtek_redirect_path( $from );
								if ( ! $from ) {
									continue;
								}
								if ( null === $to ) {
									unset( $map[ $from ] );
								} elseif ( adtek_redirect_path( $to ) && adtek_redirect_path( $to ) !== $from ) {
									$map[ $from ] = adtek_redirect_path( $to );
								}
							}
							update_option( 'adtek_redirects', $map, true );
							$out['redirects'] = array( 'old' => $old, 'new' => $map );
						}

						$link = $request['wpml_link'];
						if ( is_array( $link ) && ! empty( $link['id'] ) && ! empty( $link['translation_of'] ) && ! empty( $link['lang'] ) ) {
							$id   = (int) $link['id'];
							$src  = (int) $link['translation_of'];
							$type = apply_filters( 'wpml_element_type', get_post_type( $src ) );
							$trid = apply_filters( 'wpml_element_trid', null, $src, $type );
							if ( ! $trid || ! get_post( $id ) || get_post_type( $id ) !== get_post_type( $src ) ) {
								$out['wpml_link'] = 'bad_request';
							} else {
								$src_lang = apply_filters( 'wpml_element_language_code', null, array( 'element_id' => $src, 'element_type' => get_post_type( $src ) ) );
								do_action(
									'wpml_set_element_language_details',
									array(
										'element_id'           => $id,
										'element_type'         => $type,
										'trid'                 => $trid,
										'language_code'        => sanitize_key( $link['lang'] ),
										'source_language_code' => $src_lang,
									)
								);
								$out['wpml_link'] = apply_filters( 'wpml_get_element_translations', null, $trid, $type );
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
