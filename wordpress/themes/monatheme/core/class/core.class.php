<?php

class Mona_core {

    public function __construct() {

        
        add_action('after_setup_theme', [$this, 'after_setup_theme']);
        remove_action('wp_head', [$this, 'rsd_link']);
        remove_action('wp_head', [$this, 'wlwmanifest_link']);
        remove_action('wp_head', [$this, 'parent_post_rel_link'], 10, 0);
        remove_action('wp_head', [$this, 'start_post_rel_link'], 10, 0);
        remove_action('wp_head', [$this, 'adjacent_posts_rel_link_wp_head'], 10, 0);
        remove_action('wp_head', [$this, 'wp_generator']);

        add_filter('wp_title', [$this, 'rw_title'], 10, 3);
        add_filter('the_generator', [$this, 'mona_rss_version']);
        add_filter('wp_head', [$this, 'mona_remove_wp_widget_recent_comments_style'], 1);
        add_action('wp_head', [$this, 'mona_remove_recent_comments_style'], 1);
        add_filter('the_content', [$this, 'mona_filter_ptags_on_images']);
        add_filter('get_the_archive_title', [$this, 'rewrite_term_title']);
        add_filter('login_errors', [$this, 'custom_wordpress_error_message']);
        add_filter('style_loader_src', [$this, 'remove_version_from_scripts']);
        add_filter('script_loader_src', [$this, 'remove_version_from_scripts']);
        add_filter('rewrite_rules', [$this, '_rewrite'],999999);
    }

    public function custom_wordpress_error_message() {
        return 'That was not quite correct...';
    }

    public function remove_version_from_scripts($src) {
        if (strpos($src, 'ver=' . get_bloginfo('version')))
            $src = remove_query_arg('ver', $src);
        return $src;
    }

    public function after_setup_theme() {
        load_theme_textdomain('monamedia', get_template_directory() . '/languages');
        add_theme_support('post-thumbnails');
        add_theme_support('woocommerce');
        add_theme_support('custom-logo', ['height' => 100, 'width' => 400, 'flex-height' => true, 'flex-width' => true, 'header-text' => ['site-title', 'site-description'],]);
        add_theme_support('title-tag');
        add_theme_support('menus');
        add_theme_support('html5', ['comment-list', 'search-form', 'comment-form']);
    }

    public function rw_title($title, $sep, $seplocation) {
        global $page, $paged;

        // Don't affect in feeds.
        if (is_feed())
            return $title;

        // Add the blog's name
        if ('right' == $seplocation) {
            $title .= get_bloginfo('name');
        } else {
            $title = get_bloginfo('name') . $title;
        }

        // Add the blog description for the home/front page.
        $site_description = get_bloginfo('description', 'display');

        if ($site_description && ( is_home() || is_front_page() )) {
            $title .= " {$sep} {$site_description}";
        }

        // Add a page number if necessary:
        if ($paged >= 2 || $page >= 2) {
            $title .= " {$sep} " . sprintf(__('Page %s', 'dbt'), max($paged, $page));
        }

        return $title;
    }

    public function mona_rss_version() {
        return '';
    }

    public function mona_remove_wp_widget_recent_comments_style() {
        if (has_filter('wp_head', 'wp_widget_recent_comments_style')) {
            remove_filter('wp_head', 'wp_widget_recent_comments_style');
        }
    }

    function mona_remove_recent_comments_style() {
        global $wp_widget_factory;
        if (isset($wp_widget_factory->widgets['WP_Widget_Recent_Comments'])) {
            remove_action('wp_head', array($wp_widget_factory->widgets['WP_Widget_Recent_Comments'], 'recent_comments_style'));
        }
    }

    public function mona_filter_ptags_on_images($content) {
        return preg_replace('/<p>\s*(<a .*>)?\s*(<img .* \/>)\s*(<\/a>)?\s*<\/p>/iU', '\1\2\3', $content);
    }

    public function rewrite_term_title($title) {
        if (is_category()) {

            $title = str_replace(array('Category:', 'Tag:', 'Tags:'), array('', '', ''), $title);
        }
        return $title;
    }

    public function _rewrite($rulll) {
        $rules = "RewriteRule wp-content/plugins/(.*\.php)$ - [R=404,L]\n";
        $rules .= "RewriteRule wp-content/themes/(.*\.php)$ - [R=404,L]\n";
        $rules .= "RewriteCond %{QUERY_STRING} (<|%3C).*script.*(>|%3E) [NC,OR]\n";
        $rules .= "RewriteCond %{QUERY_STRING} GLOBALS(=|[|%[0-9A-Z]{0,2}) [OR]\n";
        $rules .= "RewriteCond %{QUERY_STRING} _REQUEST(=|[|%[0-9A-Z]{0,2})\n";
        $rules .= "RewriteRule ^(.*)$ index.php [F,L]\n";
        $rules .= "RewriteRule ^wp-admin/includes/ - [F,L]\n";
        $rules .= "RewriteRule !^wp-includes/ - [S=3]\n";
        $rules .= "RewriteRule ^wp-includes/[^/]+\.php$ - [F,L]\n";
        $rules .= "RewriteRule ^wp-includes/js/tinymce/langs/.+\.php - [F,L]\n";
        $rules .= "RewriteRule ^wp-includes/theme-compat/ - [F,L]\n";
        $rules .= "RewriteRule ^wp-content/uploads/.*\.(php|rb|py)$ - [F,L,NC]\n";
        $rules .= "RewriteRule ^wp-config.php$ - [F,L,NC]\n";
        $rules .= "</IfModule>";
        $rulll = str_replace("</IfModule>", $rules, $rulll);
        return $rulll;
    }

    

}

new Mona_core();