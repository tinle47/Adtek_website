<?php
function mona_page_navi($wp_query='') {
	if($wp_query==''){
	global $wp_query;
	}

    $bignum = 999999999;
    if ($wp_query->max_num_pages <= 1)
        return;
    echo '<div class="pagination text-center">';
    echo paginate_links(array(
        'base' => str_replace($bignum, '%#%', esc_url(get_pagenum_link($bignum))),
        'format' => '',
        'current' => max(1, get_query_var('paged')),
        'total' => $wp_query->max_num_pages,
        'prev_text' => '<img src="'. get_site_url() .'/template/assets/images/pagination-arrow.svg" alt="">',
        'next_text' => '<img src="'. get_site_url() .'/template/assets/images/pagination-arrow.svg" alt="">',
        'type' => 'list',
        'end_size' => 3,
        'mid_size' => 3
    ));
    echo '</div>';
}

function mona_page_nani_ajax($wp_query = '', $paged = '') {
	if($wp_query==''){
	global $wp_query;
	}
    if($paged == '') {
        $paged = max(1, get_query_var('paged'));
    }
    $bignum = 999999999;
    if ($wp_query->max_num_pages <= 1)
        return;
    echo '<div class="pagination ajax-pagination">';
    echo paginate_links(array(
        'base' => str_replace($bignum, '%#%', esc_url(get_pagenum_link($bignum))),
        'format' => '',
        'total' => $wp_query->max_num_pages,
        'current' => $paged,
        'end_size' => 3,
        'mid_size' => 3,
        'prev_text' => false,
        'next_text' => false,
        'type' => 'list',
        'add_args'=> false,
        'add_fragment' => '',
        'before_page_number' => '',
        'after_page_number' => ''
    ));
    echo '</div>';
}