<?php
// Môi trường WordPress giả lập tối giản để chạy adtek_perf_process() trên HTML thật.
$S = getenv( 'PERF_WORK' ) ?: dirname( __DIR__, 2 ) . '/build/perf';
define( 'ABSPATH', $S . '/site/' );
define( 'DAY_IN_SECONDS', 86400 );
define( 'ADTEK_PERF_FONT_DIR', $S . '/site/wp-content/mu-plugins/adtek-performance/fonts' );
if ( getenv( 'DELAY_TAGS' ) ) define( 'ADTEK_PERF_DELAY_TAGS', true );
function add_action() {} function add_filter() {}
function home_url( $p = '' ) { return 'https://adtek.agency' . $p; }
function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); }
function wp_upload_dir() { return array( 'basedir' => ABSPATH . 'wp-content/uploads', 'baseurl' => 'https://adtek.agency/wp-content/uploads', 'error' => false ); }
function trailingslashit( $s ) { return rtrim( $s, '/\\' ) . '/'; }
function wp_mkdir_p( $d ) { return is_dir( $d ) || mkdir( $d, 0777, true ); }
function esc_url( $u ) { return htmlspecialchars( $u, ENT_QUOTES ); }
function esc_attr( $u ) { return htmlspecialchars( $u, ENT_QUOTES ); }
function wp_json_encode( $d ) { return json_encode( $d ); }
function get_template_directory() { return ABSPATH . 'wp-content/themes/monatheme'; }
require dirname( __DIR__, 2 ) . '/wordpress/mu-plugins/adtek-performance.php';
foreach ( array_slice( $argv, 1 ) as $name ) {
	$in  = file_get_contents( "$S/pages/$name.orig.html" );
	$t   = microtime( true );
	$out = adtek_perf_optimize( $in ); // gọi trực tiếp để thấy lỗi nếu có
	printf( "%-10s %7d -> %7d bytes  %.0f ms\n", $name, strlen( $in ), strlen( $out ), ( microtime( true ) - $t ) * 1000 );
	file_put_contents( "$S/pages/$name.opt.html", $out );
}
