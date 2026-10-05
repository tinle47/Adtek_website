<?php
/**
 * Undocumented function
 *
 * @return void
 */
function mona_hook_add_custom_post() {

    $recruitment = array(
        'labels' => array(
            'name' => 'Recruitment',
            'singular_name' => 'Recruitment',
            'all_items' => __('All Posts', 'monamedia'),
            'add_new' => __('Add New', 'monamedia'),
            'add_new_item' => __('Add New', 'monamedia'),
            'edit_item' => __('Edit Post', 'monamedia'),
            'new_item' => __('Add Post', 'monamedia'),
            'view_item' => __('View Post', 'monamedia'),
            'view_items' => __('View Post', 'monamedia'),
        ),
        'description' => 'Add Post',
        'supports' => array(
            'title',
            'editor',
            'author',
            'thumbnail',
            'comments',
            'revisions',
            'custom-fields',
            'excerpt',
        ),
        'taxonomies' => array('category_recruitment'),
        'hierarchical' => false,
		'show_in_rest' => true,
        'public' => true,
        'has_archive' => true,
        'rewrite' => array(
            'slug' => 'recruitment',
            'with_front' => true
        ),
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_nav_menus' => true,
        'show_in_admin_bar' => true,
        'menu_position' => 5,
        'menu_icon' => 'dashicons-megaphone',
        'can_export' => true,
        'has_archive' => true,
        'exclude_from_search' => true,
        'publicly_queryable' => true,
        'capability_type' => 'post'
    );
    register_post_type('mona_recruitment', $recruitment);

    $tax_recruitments = array(
        'labels' => array(
            'name' => __('Department - Recruitment', 'monamedia'),
            'singular_name' => __('Department - Recruitment', 'monamedia'),
            'search_items' => __('Search', 'monamedia'),
            'all_items' => __('All', 'monamedia'),
            'parent_item' => __('Department Recruitment', 'monamedia'),
            'parent_item_colon' => __('Department Recruitment', 'monamedia'),
            'edit_item' => __('Edit', 'monamedia'),
            'add_new' => __('Add new', 'monamedia'),
            'update_item' => __('Update', 'monamedia'),
            'add_new_item' => __('Update', 'monamedia'),
            'new_item_name' => __('Add new', 'monamedia'),
            'menu_name' => __('Category', 'monamedia'),
        ),
        'hierarchical' => true,
        'show_admin_column' => true,
        'has_archive' => true,
        'public' => true,
        'rewrite' => array(
            'slug' => 'department-recruitments',
            'with_front' => true
        ),
        'capabilities' => array(
            'manage_terms' => 'publish_posts',
            'edit_terms' => 'publish_posts',
            'delete_terms' => 'publish_posts',
            'assign_terms' => 'publish_posts',
        ),
    );
    $tax_level_recruitments = array(
        'labels' => array(
            'name' => __('Level - Recruitment', 'monamedia'),
            'singular_name' => __('Level - Recruitment', 'monamedia'),
            'search_items' => __('Search', 'monamedia'),
            'all_items' => __('All', 'monamedia'),
            'parent_item' => __('Level Recruitment', 'monamedia'),
            'parent_item_colon' => __('Level Recruitment', 'monamedia'),
            'edit_item' => __('Edit', 'monamedia'),
            'add_new' => __('Add new', 'monamedia'),
            'update_item' => __('Update', 'monamedia'),
            'add_new_item' => __('Update', 'monamedia'),
            'new_item_name' => __('Add new', 'monamedia'),
            'menu_name' => __('Level', 'monamedia'),
        ),
        'hierarchical' => true,
        'show_admin_column' => true,
        'has_archive' => true,
        'public' => true,
        'rewrite' => array(
            'slug' => 'level-recruitments',
            'with_front' => true
        ),
        'capabilities' => array(
            'manage_terms' => 'publish_posts',
            'edit_terms' => 'publish_posts',
            'delete_terms' => 'publish_posts',
            'assign_terms' => 'publish_posts',
        ),
    );
    $tax_provinceCity_recruitments = array(
        'labels' => array(
            'name' => __('City - Recruitment', 'monamedia'),
            'singular_name' => __('City - Recruitment', 'monamedia'),
            'search_items' => __('Search', 'monamedia'),
            'all_items' => __('All', 'monamedia'),
            'parent_item' => __('City Recruitment', 'monamedia'),
            'parent_item_colon' => __('City Recruitment', 'monamedia'),
            'edit_item' => __('Edit', 'monamedia'),
            'add_new' => __('Add new', 'monamedia'),
            'update_item' => __('Update', 'monamedia'),
            'add_new_item' => __('Update', 'monamedia'),
            'new_item_name' => __('Add new', 'monamedia'),
            'menu_name' => __('City', 'monamedia'),
        ),
        'hierarchical' => true,
        'show_admin_column' => true,
        'has_archive' => true,
        'public' => true,
        'rewrite' => array(
            'slug' => 'city-recruitments',
            'with_front' => true
        ),
        'capabilities' => array(
            'manage_terms' => 'publish_posts',
            'edit_terms' => 'publish_posts',
            'delete_terms' => 'publish_posts',
            'assign_terms' => 'publish_posts',
        ),
    );
    register_taxonomy('city_recruitment', 'mona_recruitment', $tax_provinceCity_recruitments);
    register_taxonomy('level_recruitment', 'mona_recruitment', $tax_level_recruitments);
    register_taxonomy('department_recruitment', 'mona_recruitment', $tax_recruitments);

    $reports = array(
        'labels' => array(
            'name' => 'Reports',
            'singular_name' => 'Reports',
            'all_items' => __('All Posts', 'monamedia'),
            'add_new' => __('Add New', 'monamedia'),
            'add_new_item' => __('Add New', 'monamedia'),
            'edit_item' => __('Edit Post', 'monamedia'),
            'new_item' => __('Add Post', 'monamedia'),
            'view_item' => __('View Post', 'monamedia'),
            'view_items' => __('View Post', 'monamedia'),
        ),
        'description' => 'Add Post',
        'supports' => array(
            'title',
            'editor',
            'author',
            'thumbnail',
            'comments',
            'revisions',
            'custom-fields',
            'excerpt',
        ),
        'taxonomies' => array('category_reports'),
        'hierarchical' => false,
		'show_in_rest' => true,
        'public' => true,
        'has_archive' => true,
        'rewrite' => array(
            'slug' => 'reports',
            'with_front' => true
        ),
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_nav_menus' => true,
        'show_in_admin_bar' => true,
        'menu_position' => 5,
        'menu_icon' => 'dashicons-nametag',
        'can_export' => true,
        'has_archive' => true,
        'exclude_from_search' => true,
        'publicly_queryable' => true,
        'capability_type' => 'post'
    );
    register_post_type('mona_reports', $reports);

    $tax_reports = array(
        'labels' => array(
            'name' => __('Category - Reports', 'monamedia'),
            'singular_name' => __('Category - Reports', 'monamedia'),
            'search_items' => __('Search', 'monamedia'),
            'all_items' => __('All', 'monamedia'),
            'parent_item' => __('Category Reports', 'monamedia'),
            'parent_item_colon' => __('Category Reports', 'monamedia'),
            'edit_item' => __('Edit', 'monamedia'),
            'add_new' => __('Add new', 'monamedia'),
            'update_item' => __('Update', 'monamedia'),
            'add_new_item' => __('Update', 'monamedia'),
            'new_item_name' => __('Add new', 'monamedia'),
            'menu_name' => __('Category', 'monamedia'),
        ),
        'hierarchical' => true,
        'show_admin_column' => true,
        'has_archive' => true,
        'public' => true,
        'rewrite' => array(
            'slug' => 'category-reports',
            'with_front' => true
        ),
        'capabilities' => array(
            'manage_terms' => 'publish_posts',
            'edit_terms' => 'publish_posts',
            'delete_terms' => 'publish_posts',
            'assign_terms' => 'publish_posts',
        ),
    );
    register_taxonomy('category_reports', 'mona_reports', $tax_reports);
    $tax_field_reports = array(
        'labels' => array(
            'name' => __('Field - Reports', 'monamedia'),
            'singular_name' => __('Field - Reports', 'monamedia'),
            'search_items' => __('Search', 'monamedia'),
            'all_items' => __('All', 'monamedia'),
            'parent_item' => __('Field Reports', 'monamedia'),
            'parent_item_colon' => __('Field Reports', 'monamedia'),
            'edit_item' => __('Edit', 'monamedia'),
            'add_new' => __('Add new', 'monamedia'),
            'update_item' => __('Update', 'monamedia'),
            'add_new_item' => __('Update', 'monamedia'),
            'new_item_name' => __('Add new', 'monamedia'),
            'menu_name' => __('Field', 'monamedia'),
        ),
        'hierarchical' => true,
        'show_admin_column' => true,
        'has_archive' => true,
        'public' => true,
        'rewrite' => array(
            'slug' => 'field-reports',
            'with_front' => true
        ),
        'capabilities' => array(
            'manage_terms' => 'publish_posts',
            'edit_terms' => 'publish_posts',
            'delete_terms' => 'publish_posts',
            'assign_terms' => 'publish_posts',
        ),
    );
    register_taxonomy('field_reports', 'mona_reports', $tax_field_reports);
    $tax_year_reports = array(
        'labels' => array(
            'name' => __('Year - Reports', 'monamedia'),
            'singular_name' => __('Year - Reports', 'monamedia'),
            'search_items' => __('Search', 'monamedia'),
            'all_items' => __('All', 'monamedia'),
            'parent_item' => __('Year Reports', 'monamedia'),
            'parent_item_colon' => __('Year Reports', 'monamedia'),
            'edit_item' => __('Edit', 'monamedia'),
            'add_new' => __('Add new', 'monamedia'),
            'update_item' => __('Update', 'monamedia'),
            'add_new_item' => __('Update', 'monamedia'),
            'new_item_name' => __('Add new', 'monamedia'),
            'menu_name' => __('Year', 'monamedia'),
        ),
        'hierarchical' => true,
        'show_admin_column' => true,
        'has_archive' => true,
        'public' => true,
        'rewrite' => array(
            'slug' => 'year-reports',
            'with_front' => true
        ),
        'capabilities' => array(
            'manage_terms' => 'publish_posts',
            'edit_terms' => 'publish_posts',
            'delete_terms' => 'publish_posts',
            'assign_terms' => 'publish_posts',
        ),
    );
    register_taxonomy('year_reports', 'mona_reports', $tax_year_reports);

    $glossary = array(
        'labels' => array(
            'name' => 'Glossary',
            'singular_name' => 'Glossary',
            'all_items' => __('All Posts', 'monamedia'),
            'add_new' => __('Add New', 'monamedia'),
            'add_new_item' => __('Add New', 'monamedia'),
            'edit_item' => __('Edit Post', 'monamedia'),
            'new_item' => __('Add Post', 'monamedia'),
            'view_item' => __('View Post', 'monamedia'),
            'view_items' => __('View Post', 'monamedia'),
        ),
        'description' => 'Add Post',
        'supports' => array(
            'title',
            'editor',
            'author',
            'thumbnail',
            'comments',
            'revisions',
            'custom-fields',
            'excerpt',
        ),
        'taxonomies' => array('category_glossary'),
        'hierarchical' => false,
		'show_in_rest' => true,
        'public' => true,
        'has_archive' => true,
        'rewrite' => array(
            'slug' => 'glossary',
            'with_front' => true
        ),
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_nav_menus' => true,
        'show_in_admin_bar' => true,
        'menu_position' => 5,
        'menu_icon' => 'dashicons-text-page',
        'can_export' => true,
        'has_archive' => true,
        'exclude_from_search' => true,
        'publicly_queryable' => true,
        'capability_type' => 'post'
    );
    register_post_type('mona_glossary', $glossary);

    $tax_glossary = array(
        'labels' => array(
            'name' => __('Category - Glossary', 'monamedia'),
            'singular_name' => __('Category - Glossary', 'monamedia'),
            'search_items' => __('Search', 'monamedia'),
            'all_items' => __('All', 'monamedia'),
            'parent_item' => __('Category Glossary', 'monamedia'),
            'parent_item_colon' => __('Category Glossary', 'monamedia'),
            'edit_item' => __('Edit', 'monamedia'),
            'add_new' => __('Add new', 'monamedia'),
            'update_item' => __('Update', 'monamedia'),
            'add_new_item' => __('Update', 'monamedia'),
            'new_item_name' => __('Add new', 'monamedia'),
            'menu_name' => __('Category', 'monamedia'),
        ),
        'hierarchical' => true,
        'show_admin_column' => true,
        'has_archive' => true,
        'public' => true,
        'rewrite' => array(
            'slug' => 'category-glossary',
            'with_front' => true
        ),
        'capabilities' => array(
            'manage_terms' => 'publish_posts',
            'edit_terms' => 'publish_posts',
            'delete_terms' => 'publish_posts',
            'assign_terms' => 'publish_posts',
        ),
    );
    register_taxonomy('category_glossary', 'mona_glossary', $tax_glossary);

    $solution = array(
        'labels' => array(
            'name' => 'Solution',
            'singular_name' => 'Solution',
            'all_items' => __('All Posts', 'monamedia'),
            'add_new' => __('Add New', 'monamedia'),
            'add_new_item' => __('Add New', 'monamedia'),
            'edit_item' => __('Edit Post', 'monamedia'),
            'new_item' => __('Add Post', 'monamedia'),
            'view_item' => __('View Post', 'monamedia'),
            'view_items' => __('View Post', 'monamedia'),
        ),
        'description' => 'Add Post',
        'supports' => array(
            'title',
            'editor',
            'author',
            'thumbnail',
            'comments',
            'revisions',
            'custom-fields',
            'excerpt',
        ),
        'taxonomies' => array(),
        'hierarchical' => false,
		'show_in_rest' => true,
        'public' => true,
        'has_archive' => true,
        'rewrite' => array(
            'slug' => 'solution',
            'with_front' => true
        ),
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_nav_menus' => true,
        'show_in_admin_bar' => true,
        'menu_position' => 5,
        'menu_icon' => 'dashicons-editor-help',
        'can_export' => true,
        'has_archive' => true,
        'exclude_from_search' => true,
        'publicly_queryable' => true,
        'capability_type' => 'post'
    );
    register_post_type('mona_solution', $solution);

    $team = array(
        'labels' => array(
            'name' => 'Team',
            'singular_name' => 'Team',
            'all_items' => __('All Posts', 'monamedia'),
            'add_new' => __('Add New', 'monamedia'),
            'add_new_item' => __('Add New', 'monamedia'),
            'edit_item' => __('Edit Post', 'monamedia'),
            'new_item' => __('Add Post', 'monamedia'),
            'view_item' => __('View Post', 'monamedia'),
            'view_items' => __('View Post', 'monamedia'),
        ),
        'description' => 'Add Post',
        'supports' => array(
            'title',
            'editor',
            'author',
            'thumbnail',
            'comments',
            'revisions',
            'custom-fields',
            'excerpt',
        ),
        'taxonomies' => array('category_team'),
        'hierarchical' => false,
		'show_in_rest' => true,
        'public' => true,
        'has_archive' => true,
        'rewrite' => array(
            'slug' => 'team',
            'with_front' => true
        ),
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_nav_menus' => true,
        'show_in_admin_bar' => true,
        'menu_position' => 5,
        'menu_icon' => 'dashicons-groups',
        'can_export' => true,
        'has_archive' => true,
        'exclude_from_search' => true,
        'publicly_queryable' => true,
        'capability_type' => 'post'
    );
    register_post_type('mona_team', $team);

    $ecommerce = array(
        'labels' => array(
            'name' => 'E-Commerce',
            'singular_name' => 'E-Commerce',
            'all_items' => __('All Posts', 'monamedia'),
            'add_new' => __('Add New', 'monamedia'),
            'add_new_item' => __('Add New', 'monamedia'),
            'edit_item' => __('Edit Post', 'monamedia'),
            'new_item' => __('Add Post', 'monamedia'),
            'view_item' => __('View Post', 'monamedia'),
            'view_items' => __('View Post', 'monamedia'),
        ),
        'description' => 'Add Post',
        'supports' => array(
            'title',
            'editor',
            'author',
            'thumbnail',
            'comments',
            'revisions',
            'custom-fields',
            'excerpt',
        ),
        'taxonomies' => array('category_ecommerce'),
        'hierarchical' => false,
		'show_in_rest' => true,
        'public' => true,
        'has_archive' => true,
        'rewrite' => array(
            'slug' => 'ecommerce',
            'with_front' => true
        ),
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_nav_menus' => true,
        'show_in_admin_bar' => true,
        'menu_position' => 5,
        'menu_icon' => 'dashicons-store',
        'can_export' => true,
        'has_archive' => true,
        'exclude_from_search' => true,
        'publicly_queryable' => true,
        'capability_type' => 'post'
    );
    register_post_type('mona_ecommerce', $ecommerce);

    $tax_ecommerce = array(
        'labels' => array(
            'name' => __('Category - Ecommerce', 'monamedia'),
            'singular_name' => __('Category - Ecommerce', 'monamedia'),
            'search_items' => __('Search', 'monamedia'),
            'all_items' => __('All', 'monamedia'),
            'parent_item' => __('Category Ecommerce', 'monamedia'),
            'parent_item_colon' => __('Category Ecommerce', 'monamedia'),
            'edit_item' => __('Edit', 'monamedia'),
            'add_new' => __('Add new', 'monamedia'),
            'update_item' => __('Update', 'monamedia'),
            'add_new_item' => __('Update', 'monamedia'),
            'new_item_name' => __('Add new', 'monamedia'),
            'menu_name' => __('Category', 'monamedia'),
        ),
        'hierarchical' => true,
        'show_admin_column' => true,
        'has_archive' => true,
        'public' => true,
        'rewrite' => array(
            'slug' => 'category-ecommerce',
            'with_front' => true
        ),
        'capabilities' => array(
            'manage_terms' => 'publish_posts',
            'edit_terms' => 'publish_posts',
            'delete_terms' => 'publish_posts',
            'assign_terms' => 'publish_posts',
        ),
    );
    register_taxonomy('category_ecommerce', 'mona_ecommerce', $tax_ecommerce);
	
	$case_study = array(
        'labels' => array(
            'name' => 'Case Study',
            'singular_name' => 'Case Study',
            'all_items' => __('All Posts', 'monamedia'),
            'add_new' => __('Add New', 'monamedia'),
            'add_new_item' => __('Add New', 'monamedia'),
            'edit_item' => __('Edit Post', 'monamedia'),
            'new_item' => __('Add Post', 'monamedia'),
            'view_item' => __('View Post', 'monamedia'),
            'view_items' => __('View Post', 'monamedia'),
        ),
        'description' => 'Add Post',
        'supports' => array(
            'title',
            'editor',
            'author',
            'thumbnail',
            'comments',
            'revisions',
            'custom-fields',
            'excerpt',
        ),
        'taxonomies' => array(),
        'hierarchical' => false,
		'show_in_rest' => true,
        'public' => true,
        'has_archive' => true,
        'rewrite' => array(
            'slug' => 'case-study',
            'with_front' => true
        ),
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_nav_menus' => true,
        'show_in_admin_bar' => true,
        'menu_position' => 5,
        'menu_icon' => 'dashicons-groups',
        'can_export' => true,
        'has_archive' => true,
        'exclude_from_search' => true,
        'publicly_queryable' => true,
        'capability_type' => 'post'
    );
    register_post_type('mona_case_study', $case_study);

    flush_rewrite_rules();
}
add_action('init', 'mona_hook_add_custom_post');