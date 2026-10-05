<section class="section news">
    <div class="container">
        <h2 class="sec-tt news-tt sec-tt-left" data-aos="fade-down">
            <?php echo __('Latest news','monamedia'); ?>
        </h2>

        <?php       
            $order = 'DESC';
            $argsPost = array(
                'post_type' => 'post',
                'post_status' => 'publish',
                'posts_per_page' => 9,
                'post__not_in'=> (array)get_the_ID(),
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
                        
            $loop = new WP_Query($argsPost);
            if( $loop->have_posts() ){
            ?>
        <div class="news-list swiper">
            <div class="swiper-container">
                <div class="swiper-wrapper">
                    <?php 
                        $delayAOS_news = 100;
                        while ($loop->have_posts()) {
                            $loop->the_post();
                        ?>
                    <div class="swiper-slide news-item" data-aos="fade-up"
                        data-aos-delay="<?php echo $delayAOS_news; ?>">
                        <?php 
                            /*
                            ** GET
                            ** TEMPLATE PART
                            ** About Box News
                            */
                            $slug_part = 'patch/loop/box';
                            $name_part = 'news';
                            get_template_part($slug_part, $name_part);
                        ?>
                    </div>
                    <?php 
                            $delayAOS_news += 200;
                        } ?>
                </div>
            </div>
        </div>
        <?php }else{ ?>

        <div class="mona-mess-empty">
            <p><?php echo __( 'Content is being update', 'monamedia' ) ?></p>
        </div>

        <?php
        } wp_reset_query(); ?>
    </div>
</section>