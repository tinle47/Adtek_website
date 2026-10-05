<?php
/**
 * Check hide settings acf

if ( is_user_logged_in() ) {

    if ( get_current_user_id() == 1 ) {

        define( 'ACF_LITE', false );

    } else {
        define( 'ACF_LITE', true );
    }

} else {
    define( 'ACF_LITE', true );
}
 */

if ( is_admin() && current_user_can( 'manage_options' ) ) {
    define( 'ACF_LITE', false );
} else {
    define( 'ACF_LITE', true );
}

/**
 * define
 */
define( 'MONA_PAGE_HOME', get_option( 'page_on_front', true ) );

define( 'MONA_PAGE_BLOG', get_option( 'page_for_posts', true ) );

define( 'MONA_PAGE_ABOUT', url_to_postid( get_the_permalink( 11 ) ) );

define( 'MONA_PAGE_CONTACT', url_to_postid( get_the_permalink( 18 ) ) );

define( 'MONA_PAGE_SOLUTIONS', url_to_postid( get_the_permalink( 372 ) ) );

define( 'MONA_PAGE_RECRUITMENT', url_to_postid( get_the_permalink( 390 ) ) );

define( 'MONA_PAGE_RESOURCES', url_to_postid( get_the_permalink( 400 ) ) );

define( 'MONA_PAGE_FAQ', url_to_postid( get_the_permalink( 412 ) ) );

define( 'MONA_PAGE_GLOSSARY', url_to_postid( get_the_permalink( 425 ) ) );

define( 'MONA_PAGE_RESOURCE_MAP', url_to_postid( get_the_permalink( 599 ) ) );
/**
 * Add core
 */
require_once( get_template_directory() . '/core/class/core.class.php' );
require_once( get_template_directory() . '/core/class/Mona_walker.php' );
require_once( get_template_directory() . '/core/class/hook.class.php' );
require_once( get_template_directory() . '/core/customizer.php' );

/**
 * Add include
 */
require_once( get_template_directory() . '/includes/functions.php' );
require_once( get_template_directory() . '/includes/ajax.php' );

/**
 * Add extension
 */
require_once( get_template_directory() . '/extensions/autoload.php' );

/**
 * Add modules / widget
 */
require_once( get_template_directory() . '/modules/element-widget/class.callback.php' );
require_once( get_template_directory() . '/modules/element-widget/class.widget.php' );

/**
 * Add modules / filter commtent
 */
require_once( get_template_directory() . '/modules/filter-comments/class-filter-commtent.php' );

/**
 * Add widgets
 */
require_once( get_template_directory() . '/widgets/autoload.php' );
