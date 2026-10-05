<?php
/**
 * Undocumented function
 *
 * Add enqueue css, js
 */
function mona_style() {

    wp_enqueue_style( 'mona-custom', get_template_directory_uri() . '/css/mona-custom.css', array(), rand() );

    wp_enqueue_script( 'mona-front', get_template_directory_uri() . '/js/front.js', array(), false, true );

    wp_enqueue_script( 'mona-sweetalert', get_template_directory_uri() . '/js/sweetalert.min.js', array(), false, true );

    wp_localize_script('mona-front', 'mona_ajax_url', array(
        'ajaxURL' => admin_url('admin-ajax.php'),
        'siteURL' => get_site_url(),
    ));

}
add_action('wp_enqueue_scripts', 'mona_style');

/**
 * Undocumented function
 *
 * @param [type] $tag
 * @param [type] $handle
 * @param [type] $src
 * @return void
 */
function mona_add_module_to_my_script( $tag, $handle, $src ) {

    if ( 'mona-front' === $handle ) {

        $tag = '<script type="module" src="' . esc_url( $src ) . '"></script>';

    }

    return $tag;
}
add_filter('script_loader_tag', 'mona_add_module_to_my_script', 10, 3);
