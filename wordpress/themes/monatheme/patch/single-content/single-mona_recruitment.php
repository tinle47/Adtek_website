<?php 
    global $post;
    $post_ID = $post->ID;
    $department = get_post_term_ids($post_ID, 'department_recruitment');
    $level      = get_post_term_ids($post_ID, 'level_recruitment');
    $city      = get_post_term_ids($post_ID, 'city_recruitment');
    $recruitment_contactform = mona_get_option('recruitment_contactform');
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

    <section class="section recruitment-dt" data-aos="fade-up">
        <div class="container">
            <h2 class="sec-tt recruitment-dt-tt">
                <?php echo get_the_title($post_ID); ?>
            </h2>
            <div class="news-time-ctn">
                <div class="news-time news-detail-time">
                    <img src="<?php echo get_site_url() ?>/template/assets/images/calendar.svg" alt="">
                    <?php echo get_the_date('F d,Y', $post_ID); ?>
                </div>
                <div class="news-time news-detail-time">
                    <img src="<?php echo get_site_url() ?>/template/assets/images/document-2.svg" alt="">
                    <?php echo get_the_author(); ?>
                </div>
            </div>
            <div class="recruitment-info">
                <?php 
                    if( !empty($department) ){
                ?>
                <div class="recruitment-info-item">
                    <div class="title"><?php echo __('Department','monamedia'); ?></div>
                    <div class="detail">
                        <?php 
                        foreach ($department as $key => $id) {
                            $obj = get_term_by('id',  $id, 'department_recruitment');
                            if( empty($department[$key+1]) ){
                                echo $obj->name;
                            }else{
                                echo $obj->name . ' - ';
                            }
                        } 
                        ?>
                    </div>
                </div>
                <?php } ?>

                <?php 
                    if( !empty($level) ){
                ?>
                <div class="recruitment-info-item">
                    <div class="title"><?php echo __('Level','monamedia'); ?></div>
                    <div class="detail">
                        <?php 
                        foreach ($level as $key => $id) {
                            $obj = get_term_by('id',  $id, 'level_recruitment');
                            if( empty($level[$key+1]) ){
                                echo $obj->name;
                            }else{
                                echo $obj->name . ' - ';
                            }
                        } 
                        ?>
                    </div>
                </div>
                <?php } ?>

                <?php 
                    if( !empty($city) ){
                ?>
                <div class="recruitment-info-item">
                    <div class="title"><?php echo __('City','monamedia'); ?></div>
                    <div class="detail">
                        <?php 
                        foreach ($city as $key => $id) {
                            $obj = get_term_by('id',  $id, 'city_recruitment');
                            if( empty($city[$key+1]) ){
                                echo $obj->name;
                            }else{
                                echo $obj->name . ' - ';
                            }
                        } 
                        ?>
                    </div>
                </div>
                <?php } ?>
            </div>
            <div class="recruitment-dt-desc mona-content">
                <?php the_content(); ?>
            </div>

            <?php if( !empty($recruitment_contactform) ){ ?>
            <div class="recruitment-dt-btn">
                <a href="#recruitment-popup" class="btn popup-with-zoom-anim"
                    data-nominee="<?php echo get_the_title(); ?>">
                    <?php echo __('Recruitment','monamedia'); ?>
                    <img src="<?php echo get_site_url() ?>/template/assets/images/btn-arrow.svg" alt="">
                </a>
            </div>
            <?php } ?>
        </div>
    </section>
    <?php if( !empty($recruitment_contactform) ){ ?>
    <div id="recruitment-popup" class="recruitment-popup zoom-anim-dialog mfp-hide">
        <div class="recruitment-popup-form">
            <?php echo do_shortcode($recruitment_contactform); ?>
        </div>
    </div>
    <?php } ?>

    <section class="section news about read no-border">
        <div class="container">
            <h2 class="sec-tt news-tt sec-tt-left" data-aos="fade-down">
                <?php echo __('Related Recruitment','monamedia'); ?>
            </h2>
            <?php 
                $post_per_page = 6;
                // $paged = max( 1, get_query_var('paged') );
                // $offset = ( $paged - 1 ) * $post_per_page;
                $order = 'DESC';
                $args = array(
                    'post_type' => 'mona_recruitment',
                    'post_status' => 'publish',
                    'posts_per_page' => $post_per_page,
                    'post__not_in'=> (array)$post_ID,
                    // 'paged' => $paged,
                    // 'offset' => $offset,
                    'order' => $order,
                    'meta_query' => [
                        'relation' => 'AND',
                    ],
                    'tax_query' => [
                        'relation'=>'AND',
                    ]
                );
       
                $loop = new WP_Query($args);
                if( $loop->have_posts() ){
                    
            ?>
            <div class="news-list swiper">
                <div class="swiper-container">
                    <div class="swiper-wrapper">

                        <?php 
                        $delayRelated = 100;
                        while ($loop->have_posts()) {
                            $loop->the_post();
                        ?>

                        <div class="swiper-slide news-item" data-aos="fade-up"
                            data-aos-delay="<?php echo $delayRelated; ?>">
                            <?php 
                            /*
                            ** GET
                            ** TEMPLATE PART
                            ** Box Recruitment
                            */
                            $slug_part = 'patch/loop/box';
                            $name_part = 'news';
                            get_template_part($slug_part, $name_part);
                        ?>
                        </div>

                        <?php 
                        $delayRelated += 200;
                        } ?>
                    </div>
                </div>
            </div>
            <?php }else{ ?>

            <div class="mona-mess-empty">
                <p><?php echo __( 'Content is being update', 'monamedia' ) ?></p>
            </div>

            <?php
            }
            wp_reset_query(); ?>
        </div>
    </section>
</main>