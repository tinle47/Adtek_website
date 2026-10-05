<?php
/**
 * Template name: Resources Map Page
 * @author : Hy Hý
 */
get_header();
while (have_posts()):
    the_post();
    ?>

<main class="main">
    <?php 
        /*
        ** GET
        ** TEMPLATE PART
        ** Breadcrumb
        */
        $slug_part = 'patch/breadcrumb';
        $name_part = '';
        get_template_part($slug_part, $name_part);
    ?>

    <?php 
    $mona_resources_map_about = get_field('mona_resources_map_about');
    if( !empty($mona_resources_map_about) ){
    ?>
    <section class="section resources-map">
        <div class="container">
            <div class="resources-map-ctn">
                <div class="resources-map-text">
                    <h2 class="sec-tt resources-map-tt" data-aos="fade-down">
                        <?php echo $mona_resources_map_about['resources_map_about_title']; ?>
                    </h2>
                    <div class="resources-desc mona-content" data-aos="fade-up">
                        <?php echo $mona_resources_map_about['resources_map_about_description']; ?>
                    </div>
                </div>
                <div class="resources-map-img" data-aos="fade-up">
                    <?php echo wp_get_attachment_image( $mona_resources_map_about['resources_map_about_img'], 'full'); ?>
                </div>
            </div>
        </div>
    </section>
    <?php } ?>

    <?php 
        $mona_resources_ranking = get_field('mona_resources_ranking');
        if( !empty($mona_resources_ranking) ){
    ?>
    <section class="resources-ranking">
        <div class="container">
            <h2 class="sec-tt resources-ranking-tt" data-aos="fade-up">
                <?php echo $mona_resources_ranking['ranking_title']; ?>
            </h2>
            <?php 
                if( !empty($mona_resources_ranking['ranking_filter']) ){
            ?>
            <div class="filter-form" data-aos="fade-up">
                <form id="filterRankingEcommerce">
                    <div class="f-r">
                        <?php 
                        foreach ($mona_resources_ranking['ranking_filter'] as $key => $filter) { 
                            $terms_child = get_terms( array(
                                'taxonomy' => $filter['filter_detail']->taxonomy,
                                'parent' => $filter['filter_detail']->term_id,
                                'hide_empty' => false,
                            ) );

                            $enable_first_child_in_filter_detail = $filter['enable_first_child_in_filter_detail'];
                        ?>
                        <div class="f-c">
                            <select class="select2 form-control" name="<?php echo $filter['filter_detail']->slug ?>"
                                id="<?php echo $filter['filter_detail']->slug; ?>">

                                <?php if( empty($enable_first_child_in_filter_detail) ){ ?>
                                <option value="">
                                    <?php echo __('Select ','monamedia'); ?>
									<?php echo $filter['filter_detail']->name; ?>
                                </option>
                                <?php } ?>

                                <?php if( !empty($terms_child) ){ 
                                    foreach ($terms_child as $key_child => $child_item) {
                                ?>

                                <?php if ( !empty($enable_first_child_in_filter_detail) && $key_child==0 ) { ?>
                                <option value="<?php echo $child_item->slug; ?>" selected>
                                    <?php echo $child_item->name ?>
								</option>

                                <?php }else { ?>
                                <option value="<?php echo $child_item->slug; ?>"
                                    <?php echo mona_selected(@$_GET[$filter['filter_detail']->slug], $child_item->slug);  ?>>
                                    <?php echo $child_item->name ?></option>
                                <?php } ?>

                                <?php } } ?>
                            </select>
                        </div>
                        <?php } ?>
                        <div class="f-c">
                            <button type="submit" class="btn">
                                <?php echo __('Search', 'monamedia'); ?>
                                <img src="<?php echo get_site_url() ?>/template/assets/images/search.svg" alt="">
                            </button>
                        </div>
                    </div>
                </form>
            </div>
            <?php } ?>
            <div class="resources-infographic" data-aos="fade-up">
                <div class="infographic-header">
                    <div class="infographic-header-item">
                        <div class="item">
                            <?php echo __('Enterprise','monamedia'); ?>
                        </div>
                    </div>
                    <div class="infographic-header-item">
                        <div class="item">
                            <?php echo __('Traffic per month','monamedia'); ?>
                        </div>
                    </div>
                    <div class="infographic-header-item">
                        <div class="item">
                            <?php echo __('IOS Ranking','monamedia') ?>
                        </div>
                    </div>
                    <div class="infographic-header-item">
                        <div class="item">
                            <?php echo __('Android Ranking','monamedia') ?>
                        </div>
                    </div>
                    <div class="infographic-header-item">
                        <div class="item">
                            <?php echo __('Youtube','monamedia') ?>
                        </div>
                    </div>
                    <div class="infographic-header-item">
                        <div class="item">
                            <?php echo __('Instagram','monamedia') ?>
                        </div>
                    </div>
                    <div class="infographic-header-item">
                        <div class="item">
                            <?php echo __('Facebook','monamedia') ?>
                        </div>
                    </div>
                </div>

                <?php 
                    if( !empty($mona_resources_ranking['ranking_list']) ){
                        
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
                        foreach ($mona_resources_ranking['ranking_filter'] as $key => $filter) { 
                            $enable_first_child_in_filter_detail = $filter['enable_first_child_in_filter_detail'];
                            if( !empty($enable_first_child_in_filter_detail) && !isset($_GET[$filter['filter_detail']->slug])){
                                $terms_child = get_terms( array(
                                    'taxonomy' => $filter['filter_detail']->taxonomy,
                                    'parent' => $filter['filter_detail']->term_id,
                                    'hide_empty' => false,
                                ) );

                                if( !empty($terms_child) ){ 
                                    $args['tax_query'][] = [
                                        'taxonomy' => $terms_child[0]->taxonomy,
                                        'field' => 'slug',
                                        'terms' => $terms_child[0]->slug,
                                    ];
                                }

                            }
                        }

                        $loop = new WP_Query($args);
                        if( $loop->have_posts() ){
                        ?>
                <div class="infographic-data is-loading-group2">
                    <?php 
                        while ($loop->have_posts()) {
                            $loop->the_post();
                    ?>

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

                    <?php } ?>
                </div>
                <?php 
                    }else{ ?>

                <div class="mona-mess-empty">
                    <p><?php echo __( 'Search results are empty', 'monamedia' ) ?></p>
                </div>

                <?php
                } ?>
                <?php }else{ ?>

                <div class="mona-mess-empty">
                    <p><?php echo __( 'Content is being update', 'monamedia' ) ?></p>
                </div>

                <?php
                } wp_reset_query(); ?>
            </div>
        </div>
    </section>
    <?php } ?>

</main>

<?php
endwhile;
get_footer();
?>