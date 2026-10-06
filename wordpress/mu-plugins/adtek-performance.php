<?php
/**
 * Plugin Name: Adtek Performance
 * Description: Tăng tốc tải trang, nhất là trên di động: gộp và rút gọn CSS, font nhẹ (Latin + tiếng Việt), Font Awesome tải nền và chỉ giữ icon đang dùng, ưu tiên ảnh chính, lazy-load ảnh còn lại, bỏ jQuery nạp trùng, hoãn Crisp tới khi người dùng tương tác, tắt emoji.
 * Version:     1.0.0
 * Author:      Adtek
 *
 * Plugin chỉ sửa HTML trả về cho trình duyệt, không đổi dữ liệu hay theme.
 * - Tắt nhanh: thêm define( 'ADTEK_PERF_DISABLE', true ); vào wp-config.php, hoặc xóa file này rồi xóa cache WP-Optimize.
 * - Xem trang gốc chưa tối ưu để so sánh: thêm ?adtek_perf=0 vào URL.
 * - Hoãn cả Google Tag Manager / gtag tới khi người dùng tương tác (điểm cao hơn, nhưng có thể mất số liệu
 *   của người vào rồi thoát ngay): define( 'ADTEK_PERF_DELAY_TAGS', true );
 * - Giữ hiệu ứng AOS trên di động: define( 'ADTEK_PERF_KEEP_AOS_MOBILE', true );
 * File CSS gộp được ghi vào wp-content/uploads/adtek-perf/ và tự tạo lại khi file nguồn thay đổi.
 */

defined( 'ABSPATH' ) || exit;

define( 'ADTEK_PERF_VERSION', '1.0.0' );

if ( ! defined( 'ADTEK_PERF_FONT_DIR' ) ) {
	define( 'ADTEK_PERF_FONT_DIR', __DIR__ . '/adtek-performance/fonts' );
}

/*
 * Emoji: WordPress tự nạp script và CSS chuyển ký tự emoji thành ảnh. Trình duyệt hiện nay hiển thị emoji sẵn.
 */
add_action(
	'init',
	static function () {
		remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
		remove_action( 'wp_print_styles', 'print_emoji_styles' );
		remove_action( 'wp_enqueue_scripts', 'wp_enqueue_emoji_styles' );
		remove_action( 'wp_footer', 'print_emoji_detection_script' );
		add_filter( 'emoji_svg_url', '__return_false' );
	}
);

/*
 * Lần đầu chạy phiên bản mới: xóa cache trang của WP-Optimize để mọi trang được tạo lại với HTML đã tối ưu.
 */
add_action(
	'init',
	static function () {
		if ( get_option( 'adtek_perf_version' ) === ADTEK_PERF_VERSION ) {
			return;
		}
		update_option( 'adtek_perf_version', ADTEK_PERF_VERSION, true );
		adtek_perf_purge_page_cache();
	},
	99
);

function adtek_perf_purge_page_cache() {
	if ( function_exists( 'WP_Optimize' ) ) {
		$wpo = WP_Optimize();
		if ( is_object( $wpo ) && method_exists( $wpo, 'get_page_cache' ) ) {
			$cache = $wpo->get_page_cache();
			if ( is_object( $cache ) && method_exists( $cache, 'purge' ) ) {
				$cache->purge();
				return;
			}
		}
	}
	if ( function_exists( 'wpo_cache_flush' ) ) {
		wpo_cache_flush();
	}
}

function adtek_perf_enabled() {
	if ( defined( 'ADTEK_PERF_DISABLE' ) && ADTEK_PERF_DISABLE ) {
		return false;
	}
	if ( isset( $_GET['adtek_perf'] ) && '0' === $_GET['adtek_perf'] ) { // phpcs:ignore WordPress.Security.NonceVerification
		return false;
	}
	if ( is_admin() || wp_doing_ajax() || wp_doing_cron() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
		return false;
	}
	if ( is_feed() || is_robots() || is_trackback() || is_embed() || is_customize_preview() ) {
		return false;
	}
	return ! isset( $_SERVER['REQUEST_METHOD'] ) || 'GET' === $_SERVER['REQUEST_METHOD'];
}

add_action(
	'template_redirect',
	static function () {
		if ( adtek_perf_enabled() ) {
			ob_start( 'adtek_perf_process' );
		}
	},
	-1000
);

/**
 * Callback của output buffer: nếu có lỗi bất kỳ thì trả lại HTML gốc, không bao giờ làm hỏng trang.
 */
function adtek_perf_process( $html ) {
	if ( ! is_string( $html ) || strlen( $html ) < 255 || false === stripos( $html, '<html' ) || false === stripos( $html, '</head>' ) ) {
		return $html;
	}
	try {
		$out = adtek_perf_optimize( $html );
		return ( is_string( $out ) && '' !== $out ) ? $out : $html;
	} catch ( \Throwable $e ) {
		return $html;
	}
}

function adtek_perf_optimize( $html ) {
	$split = stripos( $html, '</head>' );
	$head  = substr( $html, 0, $split );
	$body  = substr( $html, $split );

	$head = adtek_perf_remove_emoji( $head );
	$body = adtek_perf_remove_emoji( $body );

	// jQuery bị nạp hai lần (trong <head> và cuối trang): bỏ bản trong <head>, bản cuối trang vẫn chạy trước mọi script cần nó.
	$head = adtek_perf_remove_duplicate_head_scripts( $head, $body );

	$css  = adtek_perf_bundle_css( $head, $html );
	$head = $css['head'];

	$preload = '';
	$body    = adtek_perf_optimize_images( $body, $preload );
	$body    = adtek_perf_optimize_scripts( $body );
	if ( defined( 'ADTEK_PERF_DELAY_TAGS' ) && ADTEK_PERF_DELAY_TAGS ) {
		$head = adtek_perf_delay_tags( $head );
	}

	$extra = '';
	if ( ! ( defined( 'ADTEK_PERF_KEEP_AOS_MOBILE' ) && ADTEK_PERF_KEEP_AOS_MOBILE ) ) {
		// AOS ẩn nội dung (opacity: 0) tới khi JavaScript cuối trang chạy xong, làm màn hình di động trắng vài giây.
		$extra .= '<style id="adtek-perf-inline">@media (max-width:767.98px){[data-aos]{opacity:1!important;transform:none!important;transition:none!important}}</style>';
	}
	if ( $css['fa'] ) {
		$fa     = esc_url( $css['fa'] );
		$extra .= '<link rel="stylesheet" id="adtek-perf-icons" href="' . $fa . '" media="print" onload="this.media=\'all\'" /><noscript><link rel="stylesheet" href="' . $fa . '" /></noscript>';
	}
	$head .= $extra;

	if ( '' !== $preload ) {
		$head = adtek_perf_insert_early( $head, $preload );
	}

	if ( false !== strpos( $body, 'data-adtek-delay' ) ) {
		$body = adtek_perf_insert_before_body_end( $body, adtek_perf_delay_loader() );
	}

	return $head . $body;
}

/* ---------------------------------------------------------------------------------------------
 * Tiện ích HTML
 * ------------------------------------------------------------------------------------------- */

function adtek_perf_attr( $tag, $name ) {
	if ( preg_match( '/\s' . preg_quote( $name, '/' ) . '\s*=\s*(["\'])(.*?)\1/is', $tag, $m ) ) {
		return html_entity_decode( $m[2], ENT_QUOTES );
	}
	if ( preg_match( '/\s' . preg_quote( $name, '/' ) . '\s*=\s*([^\s>"\']+)/i', $tag, $m ) ) {
		return html_entity_decode( $m[1], ENT_QUOTES );
	}
	return null;
}

function adtek_perf_has_attr( $tag, $name ) {
	return (bool) preg_match( '/\s' . preg_quote( $name, '/' ) . '(\s*=|[\s\/>])/i', $tag );
}

function adtek_perf_add_attr( $tag, $attr ) {
	return preg_replace( '/\s*(\/?)>$/', ' ' . $attr . '$1>', $tag, 1 );
}

function adtek_perf_remove_attr( $tag, $name ) {
	return preg_replace( '/\s' . preg_quote( $name, '/' ) . '\s*=\s*(["\']).*?\1/is', '', $tag );
}

function adtek_perf_insert_early( $head, $html ) {
	if ( preg_match( '/<meta\s+charset=[^>]*>/i', $head, $m, PREG_OFFSET_CAPTURE ) ) {
		$pos = $m[0][1] + strlen( $m[0][0] );
		return substr( $head, 0, $pos ) . $html . substr( $head, $pos );
	}
	if ( preg_match( '/<link\b[^>]*rel=["\']?stylesheet[^>]*>/i', $head, $m, PREG_OFFSET_CAPTURE ) ) {
		return substr( $head, 0, $m[0][1] ) . $html . substr( $head, $m[0][1] );
	}
	return $head . $html;
}

function adtek_perf_insert_before_body_end( $body, $html ) {
	$pos = strripos( $body, '</body>' );
	return false === $pos ? $body . $html : substr( $body, 0, $pos ) . $html . substr( $body, $pos );
}

function adtek_perf_remove_emoji( $html ) {
	$html = preg_replace( '#<style[^>]*id=["\']wp-emoji-styles-inline-css["\'][^>]*>.*?</style>#is', '', $html );
	$html = preg_replace( '#<script[^>]*id=["\']wp-emoji-settings["\'][^>]*>.*?</script>\s*(<script[^>]*>(?:(?!</script>).)*wp-emoji-loader(?:(?!</script>).)*</script>)?#is', '', $html );
	return $html;
}

/* ---------------------------------------------------------------------------------------------
 * Script
 * ------------------------------------------------------------------------------------------- */

function adtek_perf_remove_duplicate_head_scripts( $head, $body ) {
	return preg_replace_callback(
		'#<script\b[^>]*\bsrc=(["\'])([^"\']+)\1[^>]*>\s*</script>\s*#i',
		static function ( $m ) use ( $body ) {
			$tag = $m[0];
			if ( adtek_perf_has_attr( $tag, 'async' ) || adtek_perf_has_attr( $tag, 'defer' ) ) {
				return $tag;
			}
			return preg_match( '#<script\b[^>]*\bsrc=(["\'])' . preg_quote( $m[2], '#' ) . '\1#i', $body ) ? '' : $tag;
		},
		$head
	);
}

function adtek_perf_optimize_scripts( $body ) {
	$site_host = wp_parse_url( home_url( '/' ), PHP_URL_HOST );

	return preg_replace_callback(
		'#<script\b[^>]*\bsrc=(["\'])([^"\']+)\1[^>]*>#i',
		static function ( $m ) use ( $site_host ) {
			$tag = $m[0];
			$src = $m[2];

			// Crisp chat: chỉ tải khi người dùng cuộn, chạm hoặc di chuột (cấu hình window.$crisp phía trước vẫn giữ nguyên).
			if ( false !== stripos( $src, 'client.crisp.chat/' ) ) {
				return '<script id="crisp-js" type="text/plain" data-adtek-delay="' . esc_url( $src ) . '">';
			}

			// Thư viện JS của theme (jQuery, Swiper, GSAP...) ở cuối trang: thêm defer để trình duyệt vẽ trang trước,
			// thứ tự chạy giữa chúng và với script type="module" phía sau vẫn giữ nguyên.
			$host = wp_parse_url( $src, PHP_URL_HOST );
			$path = (string) wp_parse_url( $src, PHP_URL_PATH );
			if ( ( ! $host || $host === $site_host ) && preg_match( '#^/template(-v2)?/js/#', $path )
				&& ! adtek_perf_has_attr( $tag, 'async' ) && ! adtek_perf_has_attr( $tag, 'defer' )
				&& ! preg_match( '/\stype=(["\']?)module\1/i', $tag ) ) {
				return adtek_perf_add_attr( $tag, 'defer' );
			}
			return $tag;
		},
		$body
	);
}

/**
 * Hoãn Google Tag Manager và gtag.js (chỉ khi bật ADTEK_PERF_DELAY_TAGS).
 */
function adtek_perf_delay_tags( $head ) {
	$head = preg_replace_callback(
		'#<script\b([^>]*)>((?:(?!</script>).)*googletagmanager\.com/gtm\.js(?:(?!</script>).)*)</script>#is',
		static function ( $m ) {
			if ( false !== stripos( $m[1], 'src=' ) ) {
				return $m[0];
			}
			return '<script type="text/plain" data-adtek-delay="inline">' . $m[2] . '</script>';
		},
		$head
	);
	return preg_replace_callback(
		'#<script\b[^>]*\bsrc=(["\'])(https://www\.googletagmanager\.com/gtag/js[^"\']*)\1[^>]*>#i',
		static function ( $m ) {
			$id = adtek_perf_attr( $m[0], 'id' );
			return '<script' . ( $id ? ' id="' . esc_attr( $id ) . '"' : '' ) . ' type="text/plain" data-adtek-delay="' . esc_url( $m[2] ) . '">';
		},
		$head
	);
}

function adtek_perf_delay_loader() {
	return '<script id="adtek-perf-delay">(function(){var d=document,w=window,done=0,ev=["scroll","wheel","mousemove","touchstart","keydown","click"];'
		. 'function run(){if(done)return;done=1;ev.forEach(function(e){w.removeEventListener(e,run,{passive:true})});'
		. 'd.querySelectorAll("script[data-adtek-delay]").forEach(function(o){var s=d.createElement("script"),v=o.getAttribute("data-adtek-delay");'
		. 'if(v==="inline"){s.text=o.text}else{s.src=v;s.async=true}var id=o.id;if(id){o.removeAttribute("id");s.id=id}o.parentNode.insertBefore(s,o.nextSibling)})}'
		. 'ev.forEach(function(e){w.addEventListener(e,run,{passive:true})})})();</script>';
}

/* ---------------------------------------------------------------------------------------------
 * Ảnh
 * ------------------------------------------------------------------------------------------- */

function adtek_perf_optimize_images( $body, &$preload ) {
	$main = stripos( $body, '<main' );
	if ( false === $main ) {
		$main = stripos( $body, '</header>' );
	}
	$main = false === $main ? 0 : $main;

	preg_match_all( '#<img\b[^>]*>#i', $body, $all, PREG_OFFSET_CAPTURE );
	if ( empty( $all[0] ) ) {
		return $body;
	}

	// Ảnh chính màn hình đầu (LCP): banner trang chủ, ảnh đầu bài viết, nếu không có thì ảnh lớn đầu tiên trong <main>.
	$lcp = null;
	foreach ( array( 'id="section-banner"', 'blog-dt-content' ) as $marker ) {
		$at = strpos( $body, $marker, $main );
		if ( false === $at ) {
			continue;
		}
		foreach ( $all[0] as $i => $img ) {
			if ( $img[1] > $at && adtek_perf_is_lcp_candidate( $img[0] ) ) {
				$lcp = $i;
				break 2;
			}
		}
	}
	if ( null === $lcp ) {
		$seen = 0;
		foreach ( $all[0] as $i => $img ) {
			if ( $img[1] < $main ) {
				continue;
			}
			if ( adtek_perf_is_lcp_candidate( $img[0] ) ) {
				$lcp = $i;
				break;
			}
			if ( ++$seen >= 3 ) {
				break;
			}
		}
	}

	$out  = '';
	$last = 0;
	foreach ( $all[0] as $i => $img ) {
		list( $tag, $offset ) = $img;
		$new = $tag;

		// WordPress đang gắn fetchpriority="high" cho logo, làm logo giành băng thông với ảnh chính.
		if ( preg_match( '/class=(["\'])[^"\']*custom-logo/i', $new ) ) {
			$new = adtek_perf_remove_attr( $new, 'fetchpriority' );
		}

		if ( $i === $lcp ) {
			$new = adtek_perf_remove_attr( $new, 'loading' );
			$new = adtek_perf_remove_attr( $new, 'fetchpriority' );
			$new = adtek_perf_add_attr( $new, 'fetchpriority="high"' );
			// sizes="auto" chỉ hợp lệ với ảnh lazy.
			$new = preg_replace( '/\ssizes=(["\'])auto,\s*/i', ' sizes=$1', $new );
			$preload = adtek_perf_preload_tag( $new );
		} elseif ( null !== $lcp && $i > $lcp && $offset > $main && ! adtek_perf_has_attr( $new, 'loading' ) ) {
			$src = (string) adtek_perf_attr( $new, 'src' );
			if ( '' !== $src && 0 !== strpos( $src, 'data:' ) && ! preg_match( '/class=(["\'])[^"\']*(swiper-lazy|lazyload)/i', $new ) ) {
				$new = adtek_perf_add_attr( $new, 'loading="lazy"' );
				if ( ! adtek_perf_has_attr( $new, 'decoding' ) ) {
					$new = adtek_perf_add_attr( $new, 'decoding="async"' );
				}
			}
		}

		$out .= substr( $body, $last, $offset - $last ) . $new;
		$last = $offset + strlen( $tag );
	}
	return $out . substr( $body, $last );
}

function adtek_perf_is_lcp_candidate( $tag ) {
	$src = (string) adtek_perf_attr( $tag, 'src' );
	if ( '' === $src || 0 === strpos( $src, 'data:' ) || preg_match( '/\.svg(\?|$)/i', $src ) ) {
		return false;
	}
	$width = adtek_perf_attr( $tag, 'width' );
	return null === $width || (int) $width >= 300;
}

function adtek_perf_preload_tag( $img ) {
	$src = adtek_perf_attr( $img, 'src' );
	if ( ! $src ) {
		return '';
	}
	$tag    = '<link rel="preload" as="image" href="' . esc_url( $src ) . '"';
	$srcset = adtek_perf_attr( $img, 'srcset' );
	if ( $srcset ) {
		$tag  .= ' imagesrcset="' . esc_attr( $srcset ) . '"';
		$sizes = adtek_perf_attr( $img, 'sizes' );
		if ( $sizes ) {
			$tag .= ' imagesizes="' . esc_attr( $sizes ) . '"';
		}
	}
	return $tag . ' fetchpriority="high" />';
}

/* ---------------------------------------------------------------------------------------------
 * CSS: gộp các <link> liền nhau thành một file, giữ nguyên thứ tự áp dụng style
 * ------------------------------------------------------------------------------------------- */

function adtek_perf_storage() {
	$uploads = wp_upload_dir( null, false );
	if ( ! empty( $uploads['error'] ) ) {
		return null;
	}
	return array(
		'dir' => trailingslashit( $uploads['basedir'] ) . 'adtek-perf',
		'url' => trailingslashit( $uploads['baseurl'] ) . 'adtek-perf',
	);
}

function adtek_perf_bundle_css( $head, $html ) {
	$result = array(
		'head' => $head,
		'fa'   => null,
	);

	$storage = adtek_perf_storage();
	if ( ! $storage || ( ! is_dir( $storage['dir'] ) && ! wp_mkdir_p( $storage['dir'] ) ) || ! is_writable( $storage['dir'] ) ) {
		return $result;
	}

	// Gom nhóm: các stylesheet nội bộ liền nhau; thẻ <style> hoặc stylesheet không gộp được sẽ ngắt nhóm.
	preg_match_all( '#<style\b[^>]*>.*?</style>|<link\b[^>]*>#is', $head, $tags, PREG_OFFSET_CAPTURE );
	$groups  = array();
	$current = array();
	foreach ( $tags[0] as $found ) {
		list( $tag, $offset ) = $found;
		if ( 0 === stripos( $tag, '<link' ) ) {
			$rel = strtolower( (string) adtek_perf_attr( $tag, 'rel' ) );
			if ( 'stylesheet' !== $rel ) {
				continue;
			}
			$media = strtolower( trim( (string) adtek_perf_attr( $tag, 'media' ) ) );
			$file  = ( '' === $media || 'all' === $media || 'screen' === $media ) ? adtek_perf_url_to_file( (string) adtek_perf_attr( $tag, 'href' ) ) : null;
			if ( $file ) {
				$current[] = array( $tag, $offset, $file );
				continue;
			}
		}
		if ( $current ) {
			$groups[] = $current;
			$current  = array();
		}
	}
	if ( $current ) {
		$groups[] = $current;
	}
	if ( ! $groups ) {
		return $result;
	}

	$replacements = array();
	$fa_sources   = array();
	foreach ( $groups as $n => $group ) {
		$bundle = adtek_perf_get_bundle( array_column( $group, 2 ), $storage );
		if ( ! $bundle ) {
			continue;
		}
		foreach ( $bundle['fa'] as $fa_file ) {
			$fa_sources[ $fa_file ] = true;
		}
		foreach ( $group as $k => $item ) {
			$replacements[] = array(
				$item[1],
				strlen( $item[0] ),
				0 === $k ? '<link rel="stylesheet" id="adtek-perf-css-' . ( $n + 1 ) . '" href="' . esc_url( $bundle['url'] ) . '" />' : '',
			);
		}
	}

	usort(
		$replacements,
		static function ( $a, $b ) {
			return $b[0] - $a[0];
		}
	);
	foreach ( $replacements as $r ) {
		$head = substr_replace( $head, $r[2], $r[0], $r[1] );
	}
	$result['head'] = $head;

	if ( $fa_sources ) {
		$result['fa'] = adtek_perf_get_icon_bundle( array_keys( $fa_sources ), $html, $storage );
	}
	return $result;
}

/**
 * Đổi URL CSS của chính website thành đường dẫn file trên ổ đĩa (bỏ ?ver=...). Trả về null nếu không đọc được.
 */
function adtek_perf_url_to_file( $url ) {
	if ( '' === $url ) {
		return null;
	}
	$parts = wp_parse_url( $url );
	$home  = wp_parse_url( home_url( '/' ) );
	if ( ! empty( $parts['host'] ) && strtolower( $parts['host'] ) !== strtolower( $home['host'] ) ) {
		return null;
	}
	$path = rawurldecode( isset( $parts['path'] ) ? $parts['path'] : '' );
	if ( '.css' !== strtolower( substr( $path, -4 ) ) ) {
		return null;
	}
	$base = isset( $home['path'] ) ? rtrim( $home['path'], '/' ) : '';
	if ( '' !== $base && 0 === strpos( $path, $base . '/' ) ) {
		$path = substr( $path, strlen( $base ) );
	}
	$root = realpath( ABSPATH );
	$file = realpath( $root . '/' . ltrim( $path, '/' ) );
	if ( ! $file || 0 !== strpos( $file, $root . DIRECTORY_SEPARATOR ) || ! is_readable( $file ) ) {
		return null;
	}
	return $file;
}

/**
 * Đường dẫn URL (tính từ gốc website) của một file trên ổ đĩa, dùng để đổi url() tương đối trong CSS.
 */
function adtek_perf_file_to_url_path( $file ) {
	$root = realpath( ABSPATH );
	$home = wp_parse_url( home_url( '/' ), PHP_URL_PATH );
	$base = $home ? rtrim( $home, '/' ) : '';
	return $base . '/' . str_replace( DIRECTORY_SEPARATOR, '/', ltrim( substr( $file, strlen( $root ) ), DIRECTORY_SEPARATOR ) );
}

/**
 * Trả về file gộp cho một nhóm CSS, tạo mới khi chưa có hoặc khi một file nguồn (kể cả file @import) thay đổi.
 */
function adtek_perf_get_bundle( array $files, array $storage ) {
	$key      = substr( md5( ADTEK_PERF_VERSION . '|' . implode( '|', $files ) ), 0, 12 );
	$manifest = $storage['dir'] . '/' . $key . '.json';

	if ( is_readable( $manifest ) ) {
		$data = json_decode( (string) file_get_contents( $manifest ), true );
		if ( is_array( $data ) && ! empty( $data['file'] ) && is_file( $storage['dir'] . '/' . $data['file'] ) && adtek_perf_deps_fresh( $data['deps'] ) ) {
			adtek_perf_touch( $storage['dir'] . '/' . $data['file'] );
			return array(
				'url' => $storage['url'] . '/' . $data['file'],
				'fa'  => $data['fa'],
			);
		}
	}

	$deps = array();
	$fa   = array();
	$css  = '';
	$top  = array();
	foreach ( $files as $file ) {
		$css .= adtek_perf_read_css( $file, $deps, $fa, $top, 0 ) . "\n";
	}
	$css = implode( '', $top ) . adtek_perf_minify_css( $css );

	$name = $key . '-' . substr( md5( $css ), 0, 10 ) . '.css';
	if ( ! adtek_perf_write( $storage['dir'] . '/' . $name, $css ) ) {
		return null;
	}
	adtek_perf_write(
		$manifest,
		wp_json_encode(
			array(
				'file' => $name,
				'deps' => $deps,
				'fa'   => array_values( array_unique( $fa ) ),
			)
		)
	);
	adtek_perf_cleanup( $storage['dir'] );

	return array(
		'url' => $storage['url'] . '/' . $name,
		'fa'  => array_values( array_unique( $fa ) ),
	);
}

function adtek_perf_deps_fresh( $deps ) {
	if ( ! is_array( $deps ) ) {
		return false;
	}
	foreach ( $deps as $file => $mtime ) {
		if ( ! is_file( $file ) || filemtime( $file ) !== $mtime ) {
			return false;
		}
	}
	return true;
}

/**
 * Đọc một file CSS: nhúng trực tiếp các @import nội bộ (thay vì tải nối tiếp), đổi url() tương đối thành tuyệt đối.
 * File Font Awesome được tách riêng để tải nền.
 */
function adtek_perf_read_css( $file, array &$deps, array &$fa, array &$top, $depth ) {
	if ( $depth > 5 || isset( $deps[ $file ] ) ) {
		return '';
	}
	$deps[ $file ] = filemtime( $file );

	$css      = (string) file_get_contents( $file );
	$css      = preg_replace( '/^\xEF\xBB\xBF/', '', $css );
	$css      = preg_replace( '/@charset\s+[^;]+;/i', '', $css );
	$url_path = adtek_perf_file_to_url_path( $file );
	$dir_url  = substr( $url_path, 0, strrpos( $url_path, '/' ) + 1 );

	$css = preg_replace_callback(
		'/@import\s+(?:url\(\s*)?(["\']?)([^"\')\s;]+)\1\s*\)?\s*([^;]*);/i',
		static function ( $m ) use ( $dir_url, &$deps, &$fa, &$top, $depth ) {
			$target = adtek_perf_resolve_url( $dir_url, $m[2] );
			$media  = trim( $m[3] );
			$child  = ( 0 === strpos( $target, '/' ) && 0 !== strpos( $target, '//' ) ) ? adtek_perf_url_to_file( $target ) : null;
			if ( ! $child ) {
				// Không nhúng được (ví dụ CSS bên ngoài): đưa @import lên đầu file gộp cho hợp lệ.
				$top[] = '@import url("' . $target . '")' . ( '' !== $media ? ' ' . $media : '' ) . ';';
				return '';
			}
			if ( false !== stripos( $child, DIRECTORY_SEPARATOR . 'fontawesome' ) ) {
				$fa[] = $child;
				return '';
			}
			$inner = adtek_perf_read_css( $child, $deps, $fa, $top, $depth + 1 );
			return ( '' !== $media && 'all' !== strtolower( $media ) ) ? '@media ' . $media . '{' . $inner . '}' : $inner;
		},
		$css
	);

	return adtek_perf_rewrite_urls( $css, $dir_url );
}

function adtek_perf_rewrite_urls( $css, $dir_url ) {
	return preg_replace_callback(
		'/url\(\s*(["\']?)([^"\')]+)\1\s*\)/i',
		static function ( $m ) use ( $dir_url ) {
			$url = trim( $m[2] );
			if ( preg_match( '#^(data:|\#|[a-z][a-z0-9+.-]*:|//)#i', $url ) ) {
				return $m[0];
			}
			return 'url("' . adtek_perf_light_font( adtek_perf_resolve_url( $dir_url, $url ) ) . '")';
		},
		$css
	);
}

function adtek_perf_resolve_url( $dir_url, $url ) {
	if ( preg_match( '#^([a-z][a-z0-9+.-]*:|//)#i', $url ) ) {
		return $url;
	}
	$suffix = '';
	if ( preg_match( '/^([^?#]*)([?#].*)$/', $url, $m ) ) {
		$url    = $m[1];
		$suffix = $m[2];
	}
	$path  = 0 === strpos( $url, '/' ) ? $url : $dir_url . $url;
	$parts = array();
	foreach ( explode( '/', $path ) as $segment ) {
		if ( '..' === $segment ) {
			array_pop( $parts );
		} elseif ( '.' !== $segment && '' !== $segment ) {
			$parts[] = $segment;
		}
	}
	return '/' . implode( '/', $parts ) . $suffix;
}

/**
 * Roboto/Oswald của theme chứa cả bảng chữ Cyrillic, Hy Lạp...: dùng bản rút gọn chỉ giữ Latin + tiếng Việt (nhẹ hơn khoảng 80%).
 */
function adtek_perf_light_font( $url_path ) {
	if ( ! preg_match( '#/template/assets/fonts/(?:Roboto|Oswald)/([A-Za-z-]+\.woff2)$#', $url_path, $m ) ) {
		return $url_path;
	}
	$light = realpath( ADTEK_PERF_FONT_DIR . '/' . $m[1] );
	if ( ! $light || 0 !== strpos( $light, realpath( ABSPATH ) . DIRECTORY_SEPARATOR ) ) {
		return $url_path;
	}
	return adtek_perf_file_to_url_path( $light );
}

function adtek_perf_minify_css( $css ) {
	$css = preg_replace( '#/\*.*?\*/#s', '', $css );
	$css = preg_replace( '/\s+/', ' ', $css );
	$css = preg_replace( '/\s*([{};])\s*/', '$1', $css );
	$css = preg_replace( '/;}/', '}', $css );
	return trim( $css );
}

function adtek_perf_write( $file, $content ) {
	$tmp = $file . '.' . uniqid( '', true ) . '.tmp';
	if ( false === file_put_contents( $tmp, $content ) ) {
		return false;
	}
	if ( ! rename( $tmp, $file ) ) {
		@unlink( $tmp ); // phpcs:ignore WordPress.PHP.NoSilencedErrors
		return false;
	}
	return true;
}

/**
 * Ghi nhận file vẫn đang được dùng (cập nhật mtime tối đa mỗi ngày một lần) để không bị dọn nhầm.
 */
function adtek_perf_touch( $file ) {
	if ( filemtime( $file ) < time() - DAY_IN_SECONDS ) {
		@touch( $file ); // phpcs:ignore WordPress.PHP.NoSilencedErrors
	}
}

/**
 * Xóa file gộp không được dùng hơn 30 ngày (trang trong cache có thể còn trỏ tới file cũ nên không xóa ngay).
 */
function adtek_perf_cleanup( $dir ) {
	foreach ( (array) glob( $dir . '/*.css' ) as $file ) {
		if ( $file && filemtime( $file ) < time() - 30 * DAY_IN_SECONDS ) {
			@unlink( $file ); // phpcs:ignore WordPress.PHP.NoSilencedErrors
		}
	}
}

/* ---------------------------------------------------------------------------------------------
 * Font Awesome: file gốc (bản Pro 6 nặng 500 KB) chứa hàng nghìn icon, chỉ giữ icon thực sự dùng
 * ------------------------------------------------------------------------------------------- */

function adtek_perf_get_icon_bundle( array $sources, $html, array $storage ) {
	$icons = adtek_perf_icons_in( $html ) + adtek_perf_theme_icons( $storage );
	ksort( $icons );

	$sig = ADTEK_PERF_VERSION . '|' . implode( ',', array_keys( $icons ) );
	foreach ( $sources as $file ) {
		$sig .= '|' . $file . ':' . filemtime( $file );
	}
	$name = 'icons-' . substr( md5( $sig ), 0, 12 ) . '.css';
	$path = $storage['dir'] . '/' . $name;

	if ( is_file( $path ) ) {
		adtek_perf_touch( $path );
	} else {
		$css = '';
		foreach ( $sources as $file ) {
			$url_path = adtek_perf_file_to_url_path( $file );
			$part     = adtek_perf_rewrite_urls( (string) file_get_contents( $file ), substr( $url_path, 0, strrpos( $url_path, '/' ) + 1 ) );
			$css     .= adtek_perf_filter_icons( adtek_perf_minify_css( $part ), $icons );
		}
		// font-display: block làm icon ẩn tới 3 giây; swap cho hiện ngay khi font tải xong.
		$css = str_replace( 'font-display:block', 'font-display:swap', $css );
		if ( ! adtek_perf_write( $path, $css ) ) {
			return null;
		}
	}
	return $storage['url'] . '/' . $name;
}

function adtek_perf_icons_in( $text ) {
	preg_match_all( '/\bfa-([a-z0-9]+(?:-[a-z0-9]+)*)/', $text, $m );
	return array_fill_keys( $m[1], true );
}

/**
 * Icon xuất hiện trong mã theme và JS giao diện (kể cả icon do JavaScript chèn vào sau), quét lại mỗi ngày.
 */
function adtek_perf_theme_icons( array $storage ) {
	$cache = $storage['dir'] . '/theme-icons.json';
	if ( is_readable( $cache ) && filemtime( $cache ) > time() - DAY_IN_SECONDS ) {
		$icons = json_decode( (string) file_get_contents( $cache ), true );
		if ( is_array( $icons ) ) {
			return $icons;
		}
	}

	$icons = array();
	$dirs  = array( get_template_directory(), ABSPATH . 'template/js', ABSPATH . 'template-v2/js' );
	foreach ( $dirs as $dir ) {
		if ( ! is_dir( $dir ) ) {
			continue;
		}
		$it = new RecursiveIteratorIterator( new RecursiveDirectoryIterator( $dir, FilesystemIterator::SKIP_DOTS ) );
		foreach ( $it as $file ) {
			$path = $file->getPathname();
			if ( preg_match( '#[\\\\/](libs|node_modules|element-widget)[\\\\/]#', $path ) || ! preg_match( '/\.(php|js)$/', $path ) || $file->getSize() > 1048576 ) {
				continue;
			}
			$icons += adtek_perf_icons_in( (string) file_get_contents( $path ) );
		}
	}
	adtek_perf_write( $cache, wp_json_encode( $icons ) );
	return $icons;
}

/**
 * Bỏ các rule ".fa-ten-icon:before{content:...}" của icon không dùng; giữ nguyên @font-face và các class tiện ích.
 */
function adtek_perf_filter_icons( $css, array $icons ) {
	return preg_replace_callback(
		'/(?<![^{}])([^{}@]+)\{([^{}]*)\}/',
		static function ( $m ) use ( $icons ) {
			$selectors = explode( ',', $m[1] );
			$keep      = array();
			foreach ( $selectors as $selector ) {
				if ( ! preg_match( '/\.fa-([a-z0-9-]+)::?(?:before|after)\s*$/', $selector, $s ) ) {
					return $m[0];
				}
				if ( isset( $icons[ $s[1] ] ) ) {
					$keep[] = $selector;
				}
			}
			return $keep ? implode( ',', $keep ) . '{' . $m[2] . '}' : '';
		},
		$css
	);
}
