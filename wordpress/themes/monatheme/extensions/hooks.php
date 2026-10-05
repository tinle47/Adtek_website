<?php
add_filter( 'gutenberg_use_widgets_block_editor', '__return_false' );
add_filter( 'use_widgets_block_editor', '__return_false' );
/**
 * Undocumented function
 *
 * @param [type] $url
 * @param [type] $path
 * @param [type] $blog_id
 * @return void
 */
function mona_filter_admin_url($url, $path, $blog_id){

    if ( $path === 'admin-ajax.php' && ! is_admin() ){

        $url.='?mona-ajax';
    }
    return $url;
}
add_filter('admin_url', 'mona_filter_admin_url', 999,3);

/**
 * Undocumented function
 *
 * @return void
 */
function mona_redirect_external_after_logout() {

	wp_redirect( get_the_permalink( MONA_PAGE_HOME ) );
	exit();
}
//add_action( 'wp_logout', 'mona_redirect_external_after_logout');

/**
 * Undocumented function
 *
 * @param [type] $query
 * @return void
 */
function mona_parse_request_post_type( $query ) {

    if ( ! $query->is_main_query() || 2 != count( $query->query ) || ! isset( $query->query['page'] ) ) {
        return;
    }

    if ( ! empty( $query->query['name'] ) ) {
        $query->set( 'post_type', array(
                'post',
                'page',
                'mona_recruitment',
                'mona_reports',
            )
        );
    }
}
//add_action( 'pre_get_posts', 'mona_parse_request_post_type' );

/**
 * Undocumented function
 *
 * @param [type] $post_states
 * @param [type] $post
 * @return void
 */
function mona_add_post_state( $post_states, $post ) {

    if ( $post->ID == MONA_PAGE_BLOG ) {
        $post_states[] = __( 'PAGE - News', 'mona-admin' );
    }

    if ( $post->ID == MONA_PAGE_ABOUT ) {
        $post_states[] = __( 'PAGE - AboutUs', 'mona-admin' );
    }

    if ( $post->ID == MONA_PAGE_CONTACT ) {
        $post_states[] = __( 'PAGE - Contact', 'mona-admin' );
    }

    if ( $post->ID == MONA_PAGE_RECRUITMENT ) {
        $post_states[] = __( 'PAGE - Recruitment', 'mona-admin' );
    }

    if ( $post->ID == MONA_PAGE_RESOURCES ) {
        $post_states[] = __( 'PAGE - Reports', 'mona-admin' );
    }

    if ( $post->ID == MONA_PAGE_SOLUTIONS ) {
        $post_states[] = __( 'PAGE - Solutions', 'mona-admin' );
    }

    if ( $post->ID == MONA_PAGE_GLOSSARY ) {
        $post_states[] = __( 'PAGE - Glosary', 'mona-admin' );
    }

    if ( $post->ID == MONA_PAGE_FAQ ) {
        $post_states[] = __( 'PAGE - FAQ', 'mona-admin' );
    }

    if ( $post->ID == MONA_PAGE_RESOURCE_MAP ) {
        $post_states[] = __( 'PAGE - Map', 'mona-admin' );
    }
    
    return $post_states;
}
add_filter( 'display_post_states', 'mona_add_post_state', 10, 2 );

// function wp_starts_with_posts_where( $where, $query ) {
//     global $wpdb;

//     $starts_with = esc_sql( $query->get( 'starts_with' ) );

//     if ( $starts_with ) {
//         $where .= " AND $wpdb->posts.post_title LIKE '$starts_with%'";
//     }

//     return $where;
// }
// add_filter( 'posts_where', 'wp_starts_with_posts_where', 10, 2 );