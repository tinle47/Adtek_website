<?php

class Mona_hook {

    public function __construct() {
        add_filter('pre_get_posts', [$this, 'prefix_limit_post_types_in_search']);
        add_filter('wpcf7_autop_or_not', '__return_false');
    }

    public function prefix_limit_post_types_in_search($query) {
        if (!is_admin()) {
            $query->set('ignore_sticky_posts', true);
            $ptype = $query->get('post_type', true);
            $ptype = (array) $ptype;

            if ($query->is_main_query() && is_home()) {
                $ptype[] = 'post';
                $query->set('post_type', $ptype);
                $query->set( 'posts_per_page' , 5);
            }

            if ($query->is_main_query() && is_category()) {
                $ptype[] = 'post';
                $query->set('post_type', $ptype);
                $query->set( 'posts_per_page' , 5);
            }

            if (isset($_GET['s'])) {
                $ptype[] = 'post';
                $query->set('post_type', $ptype);
                $query->set( 'posts_per_page' , 6);
            }

            if ($query->is_main_query() && $query->is_tax('department_recruitment')) {
                $ptype[] = 'mona_recruitment';
                $query->set('post_type', $ptype);
                $query->set('posts_per_page', 6);
            }
			
			if ($query->is_main_query() && $query->is_tax('category_reports')) {
				$post_per = 9;
				if ( wp_is_mobile() ) {
					$post_per = 8;
				}
                $ptype[] = 'mona_reports';
                $query->set('post_type', $ptype);
                $query->set('posts_per_page', $post_per);
            }

        }

        return $query;
    }

}

new Mona_hook();