<?php
/**
 * Undocumented function
 *
 * @return void
 */
function mona_register_sidebars() {

    register_sidebar( array(
        'id' => 'sidebar_post',
        'name' => __('Sidebar', 'mona_media'),
        'description' => __('Nội dung widget.', 'mona_media'),
        'before_widget' => '<div id="%1$s" class="widget widget-sidebar %2$s">',
        'after_widget' => '</div>',
        'before_title' => '<h3 class="blog-aside-tt">',
        'after_title' => '</h3>',
    )); 

    register_sidebar( array(
        'id' => 'header_topright',
        'name' => __('SocialNetwork', 'mona_media'),
        'description' => __('Nội dung widget.', 'mona_media'),
        'before_widget' => '<div id="%1$s" class="widget widget-header-topright %2$s">',
        'after_widget' => '</div>',
        'before_title' => '<h3 class="blog-aside-tt">',
        'after_title' => '</h3>',
    ));

    register_sidebar( array(
        'id' => 'footer_col_1',
        'name' => __('Footer Col 1', 'mona_media'),
        'description' => __('Nội dung widget.', 'mona_media'),
        'before_widget' => '<div id="%1$s" class="widget widget-footer-col-1 %2$s">',
        'after_widget' => '</div>',
        'before_title' => '<h3 class="blog-aside-tt">',
        'after_title' => '</h3>',
    ));

    register_sidebar( array(
        'id' => 'footer_col_2',
        'name' => __('Footer Col 2', 'mona_media'),
        'description' => __('Nội dung widget.', 'mona_media'),
        'before_widget' => '<div id="%1$s" class="widget widget-footer-col-2 %2$s">',
        'after_widget' => '</div>',
        'before_title' => '<h3 class="blog-aside-tt">',
        'after_title' => '</h3>',
    ));

    register_sidebar( array(
        'id' => 'footer_col_3',
        'name' => __('Footer Col 3', 'mona_media'),
        'description' => __('Nội dung widget.', 'mona_media'),
        'before_widget' => '<div id="%1$s" class="widget widget-footer-col-3 %2$s">',
        'after_widget' => '</div>',
        'before_title' => '<h3 class="blog-aside-tt">',
        'after_title' => '</h3>',
    ));
}
add_action('widgets_init', 'mona_register_sidebars');