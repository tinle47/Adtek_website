<?php
// AJAX
function mona_ajax_add_to_cart() {
}
//add_action('wp_ajax_mona_ajax_add_to_cart', 'mona_ajax_add_to_cart'); // login
//add_action('wp_ajax_nopriv_mona_ajax_add_to_cart', 'mona_ajax_add_to_cart'); // no login

function mona_ajax_get_cities() {
    
    $city_slug = $_POST['country_recruitment'];
    $slug_city_action = $_POST['slug_city_action'];
    $city_obj = get_term_by( 'slug', $city_slug, 'city_recruitment' );

    if ( empty($city_obj) ) {

        echo wp_send_json_error(
            [
                'status' => 'error',
                'mess' => __( 'Province/City does not exist', 'monamedia' ),
            ]
        );
        wp_die();
        
    }else{

        $city_recruitment = get_terms(
            array(
                'taxonomy' => 'city_recruitment',
                'parent' => $city_obj->term_id,
                'hide_empty' => true,
            )
        );
        
        $html = '';

        if( !empty($city_recruitment) ){

            foreach ($city_recruitment as $key => $city_recruitment_item) {

                if( !empty($slug_city_action) && $slug_city_action == $city_recruitment_item->slug){
                    $selectedOption = 'selected';
                }else{
                    $selectedOption = '';
                }

                $html .= '<option value="' . $city_recruitment_item->slug . '" '. $selectedOption .'>'. $city_recruitment_item->name .'</option>';
            }
            
            echo wp_send_json_success(
                [
                    'status' => 'success',
                    'mess' =>  __( 'Quickly update the Province/City list ', 'monamedia' ) ,
                    'html' => $html
                ]
            );
            wp_die();

        }else{

            echo wp_send_json_error(
                [
                    'status' => 'error',
                    'mess' =>  __( 'No matching Province/City found', 'monamedia' ),
                ]
            );
            wp_die();
            
        }
         
    }
    wp_die();
}
add_action('wp_ajax_mona_ajax_get_cities', 'mona_ajax_get_cities'); // login
add_action('wp_ajax_nopriv_mona_ajax_get_cities', 'mona_ajax_get_cities'); // no login

function mona_ajax_get_rankingEcommerce() {
    
    $form = array();
    parse_str($_POST['form'], $form);

    if ( empty($form) ) {

        echo wp_send_json_error(
            [
                'status' => 'error',
                'mess' => __( 'Please select information!', 'monamedia' ),
            ]
        );
        wp_die();
        
    }else{

        $html = '';
        
        $mona_resources_ranking = get_field('mona_resources_ranking', MONA_PAGE_RESOURCE_MAP);
        if( !empty($mona_resources_ranking) ){
            $stackIDRanking = [];
            foreach ($mona_resources_ranking['ranking_list'] as $key => $ranking_item) {
                array_push($stackIDRanking, $ranking_item['ranking_obj']);
            }
            
            $post_per_page = -1;
            $args = array(
                'post_type' => 'mona_ecommerce',
                'post_status' => 'publish',
                'posts_per_page' => $post_per_page,
                'post__in'=> (array)$stackIDRanking,
                'orderby' => 'post__in',
                'meta_query' => [
                    'relation' => 'AND',
                ],
                'tax_query' => [
                    'relation'=>'AND',
                ]
            );

            foreach ($form as $key => $form_item) {
                
                if( !empty($form_item) ){
                    $args['tax_query'][] = [
                        'taxonomy' => 'category_ecommerce',
                        'field' => 'slug',
                        'terms' => $form_item,
                    ];
                }
            }

            $loop = new WP_Query($args);

            if( $loop->have_posts() ){
                ob_start();
                while ($loop->have_posts()) {
                    $loop->the_post(); ?>


<?php 
    /*
    ** GET
    ** TEMPLATE PART
    ** Box Ecommerce
    */
    $slug_part = 'patch/loop/box';
    $name_part = 'ecommerce';
    get_template_part($slug_part, $name_part);
?>

<?php
                }

                echo wp_send_json_success(
                    [
                        'status' => 'success',
                        'mess' =>  __( 'Quickly update the ranking list', 'monamedia' ) ,
                        'html' => ob_get_clean()
                    ]
                );
                wp_die();

            }else{

                echo wp_send_json_error(
                    [
                        'status' => 'error',
                        'mess' =>  __( 'No matching results were found', 'monamedia' ) ,
                        'html' => ob_get_clean()
                    ]
                );
                wp_die();

            }
        }
         
    }
    wp_die();
}
add_action('wp_ajax_mona_ajax_get_rankingEcommerce', 'mona_ajax_get_rankingEcommerce'); // login
add_action('wp_ajax_nopriv_mona_ajax_get_rankingEcommerce', 'mona_ajax_get_rankingEcommerce'); // no login mona_ajax_get_cost_estimates