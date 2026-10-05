<?php
/**
 * Undocumented function
 *
 * @param [type] $value_num
 * @return void
 */
function mona_replace( $value_num ) {

    $string = preg_replace('/\s+/','',$value_num);

    $stringaz = preg_replace('/[^a-zA-Z0-9_ -]/s', '', $string);

    return $stringaz;
}

/**
 * Undocumented function
 *
 * @param [type] $hotline
 * @return void
 */
function mona_replace_tel( $hotline ) {

    $string = preg_replace('/\s+/','',$hotline);

    $stringaz = preg_replace('/[^0-9_ -]/s', '', $string);

    $tel = 'tel:'.$stringaz;

    return $tel;
}

/**
 * Undocumented function
 *
 * @param string $taxonomy
 * @param string $field
 * @return void
 */
function taxonomy_by_postid( $taxonomy = '', $field = '' ) {

    if ( ! is_single() ) {
        return;
    }

    if ( $taxonomy == '' ) {
        $taxonomy = 'category';
    };

    if ( $field == '' ) {
        $field = 'ids';
    }

    $taxonomyObj = wp_get_post_terms( get_the_ID(), $taxonomy, array("fields" => $field) );
    return $taxonomyObj[0];
}

/**
 * Undocumented function
 *
 * @param string $tag
 * @param string $field
 * @return void
 */
function tag_by_postid( $tag = '', $field = '' ) {

    if ( ! is_single() ) {
        return;
    };

    if ( $tag == '' ) {
        $tag = 'post_tag';
    };

    if ( $field == '' ) {
        $field = 'ids';
    }

    $tagObj = wp_get_post_terms( get_the_ID(), $tag, array("fields" => $field) );
    if ( $tagObj ) {
        return $tagObj[0];
    }
}

/**
 * Undocumented function
 *
 * @param string $postId
 * @param string $taxonomy_
 * @return void
 */
function get_post_term_ids( $postId = '', $taxonomy_ = '' ) {

    $array_ids;

    if ( $postId == '') {
        $postId = get_the_ID();
    }

    $term_list = wp_get_post_terms( $postId, $taxonomy_ );

    if ( ! empty ( $term_list ) ) {

        foreach ( $term_list as $item ) {
            $array_ids[] = $item->term_id;
        }

    } else {

        return ;

    }

    return $array_ids;
}

/**
 * Undocumented function
 *
 * @param [type] $postID
 * @return void
 */
function mona_set_post_views( $postID ) {

    $count_key = 'mona_post_views_count';

    $count = get_post_meta( $postID, $count_key, true );

    if ( $count == '' ){

        $count = 0;
        delete_post_meta( $postID, $count_key );
        add_post_meta( $postID, $count_key, '0' );
    } else {

        $count++;
        update_post_meta( $postID, $count_key, $count );
    }
}

/**
 * Undocumented function
 *
 * @param [type] $postID
 * @return void
 */
function mona_get_post_views( $postID ) {

    $count_key = 'mona_post_views_count';

    $count = get_post_meta( $postID, $count_key, true );

    if ( $count == '' ) {

        delete_post_meta( $postID, $count_key );
        add_post_meta( $postID, $count_key, '0' );
        return "0 lượt xem sp này";
    }

    return $count;
}

/**
 * Undocumented function
 *
 * @return void
 */
function mona_get_home_title() {

    $home_title = get_the_title( get_option('page_on_front') );

    if ( $home_title && $home_title !='' ) {

        $result_title = $home_title;
    } else {

        $result_title = __( 'Trang chủ', 'monamedia' );
    }

    return $result_title;
}

/**
 * Undocumented function
 *
 * @return void
 */
function mona_get_blogs_title() {

    $blogs_title = get_the_title( get_option('page_for_posts', true) );

    if ( $blogs_title && $blogs_title !='' ) {

        $result_title = $blogs_title;
    } else {

        $result_title = __( 'Tin tức & sự kiện', 'monamedia' );
    }

    return $result_title;
}

/**
 * Undocumented function
 *
 * @return void
 */
function mona_get_blogs_url() {

    $blogs_url = get_the_permalink( get_option( 'page_for_posts', true ) );

    return esc_url( $blogs_url );
}

/**
 * Undocumented function
 *
 * @param string $logo_default
 * @return void
 */
function mona_get_logo_image_url( $logo_default = '' ) {

    $logo_url = get_theme_mod( 'custom_logo' );

    if ( $logo_url && $logo_url !='' ) {

        $result_url = wp_get_attachment_image_url( $logo_url );
    } else {

        $result_url = ''.get_site_url().'/template/images/'.$logo_default.'';
    }

    return esc_url( $result_url );
}

/**
 * Undocumented function
 *
 * @param string $attachmen_id
 * @return void
 */
function alt_title_attachment( $attachmen_id = '' ) {

    $attachmen_alt = get_post_meta( $attachmen_id, '_wp_attachment_image_alt', TRUE );

    $attachmen_title = get_the_title($attachmen_id);

    $attachmen_attr = array(
        'alt'   => $attachmen_alt,
        'title' => $attachmen_title,
    );

    return $attachmen_attr;
}

/**
 * Undocumented function
 *
 * @param string $postID
 * @return void
 */
function alt_title_thumbnail( $postID = '' ) {

    $attachment_id = get_post_thumbnail_id( $postID );

    $attachmen_alt = get_post_meta( $attachment_id, '_wp_attachment_image_alt', TRUE );

    $attachmen_title = get_the_title($attachment_id);

    $attachmen_attr = array(
        'alt'   => $attachmen_alt,
        'title' => $attachmen_title,
    );

    return $attachmen_attr;
}

/**
 * Undocumented function
 *
 * @param [type] $term_id
 * @param [type] $taxonomy
 * @param array $args
 * @return void
 */
function breadcrumb_terms_list_html( $term_id, $taxonomy, $args = array() ) {
    $list = '';
    $term = get_term( $term_id, $taxonomy );

    if ( is_wp_error( $term ) ) {
        return $term;
    }

    if ( ! $term ) {
        return $list;
    }

    $term_id = $term->term_id;

    $defaults = array(
        'format'    => 'name',
        'separator' => '',
        'link'      => true,
        'inclusive' => true,
    );

    $args = wp_parse_args( $args, $defaults );

    foreach ( array( 'link', 'inclusive' ) as $bool ) {
        $args[ $bool ] = wp_validate_boolean( $args[ $bool ] );
    }

    $parents = get_ancestors( $term_id, $taxonomy, 'taxonomy' );

    if ( $args['inclusive'] ) {
        array_unshift( $parents, $term_id );
    }

    $obz = get_queried_object();

    foreach ( array_reverse( $parents ) as $term_id ) {
        $parent = get_term( $term_id, $taxonomy );
        $name   = ( 'slug' === $args['format'] ) ? $parent->slug : $parent->name;
        if ( $obz->term_id != $term_id && $parent->parent == 0 ) {
            if ( $args['link'] ) {
                $list .= '<li class="breadcrumb-list"><a class="item" href="' . esc_url( get_term_link( $parent->term_id, $taxonomy ) ) . '">' . $name . '</a></li>' . $args['separator'];
            } else {
                $list .= $name . $args['separator'];
            }
        } else {
            $list .= '<li class="breadcrumb-list active"><a class="item" href="' . esc_url( get_term_link( $parent->term_id, $taxonomy ) ) . '">' . $name . '</a></li>' . $args['separator'];
        }
    }

    return $list;
}

/**
 * Undocumented function
 *
 * @param [type] $image_url
 * @return void
 */
function mona_get_mod_image_id( $image_url = '' ) {

	global $wpdb;

	$attachment = $wpdb->get_col( $wpdb->prepare( "SELECT ID FROM $wpdb->posts WHERE guid='%s';", $image_url ) );

    return $attachment[0];
}

/**
 * Undocumented function
 *
 * @param string $term_id
 * @param string $taxonomy
 * @return boolean
 */
function is_terms_active( $term_id = '', $taxonomy = 'category' ) {

    $termsObj = get_the_terms( get_the_ID(), $taxonomy );

    $count = 0;

    if ( empty( $termsObj ) ) {

        return $count;
    } else {

        foreach ( $termsObj as $key => $item ) {

            if ( $item->term_id === $term_id ) {
                $count++;
            }

        }
    }

    return $count;
}

/**
 * Undocumented function
 *
 * @return void
 */
function mona_get_search() {

    if ( isset( $_GET['keyword'] ) && $_GET['keyword'] !='' ) {

        $search = esc_attr( $_GET['keyword'] );
    } else {

        $search = '';
    }
    return $search;
}

/**
 * Undocumented function
 *
 * @param string $method
 * @param string $value
 * @return void
 */
function mona_checked( $method = '', $value = '' ) {

    if ( isset( $method ) && is_array( $method ) || is_object( $method ) ) {

        foreach ( $method as $key => $item ) {

            if ( $item === $value ) {
                $checked = "checked='checked'";
                return $checked;
            }
        }

    } elseif ( ! empty ( $method ) && ! is_array( $method ) ) {

        if ( $method === $value ) {

            $checked = "checked='checked'";
            return $checked;
        }
    } else {

        $checked = '';
        return $checked;
    }
}

function mona_selected( $method = '', $value = '' ) {

    if ( isset( $method ) && is_array( $method ) || is_object( $method ) ) {

        foreach ( $method as $key => $item ) {

            if ( $item === $value ) {
                $checked = "selected";
                return $checked;
            }
        }

    } elseif ( ! empty ( $method ) && ! is_array( $method ) ) {

        if ( $method === $value ) {

            $checked = "selected";
            return $checked;
        }
    } else {

        $checked = '';
        return $checked;
    }
}