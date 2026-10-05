<?php 
    $mona_aboutus_news = get_field('mona_aboutus_news');
    if( $mona_aboutus_news['news'] ){
?>
<section class="section news about">
    <div class="container">
        <h2 class="sec-tt team-tt" data-aos="fade-down"><?php echo $mona_aboutus_news['title']; ?></h2>
        <div class="sec-desc team-desc" data-aos="fade-up">
            <?php echo $mona_aboutus_news['description']; ?>
        </div>
        <?php 
        $post_per = $mona_aboutus_news['count'];
		if ( empty ( $post_per ) ) {	
			$post_per = 12;
		}
        $order = 'DESC';
        $argsPost = array(
            'post_type' => 'post',
            'post_status' => 'publish',
			'posts_per_page' => $post_per,
            'order' => $order,
            'tax_query' => [
                'relation'=>'AND',
				[
					'taxonomy' => 'category',
					'field' => 'term_id',
					'terms' => (array)$mona_aboutus_news['news'],
					'include_children' => 'true',
					'operator' => 'IN',
				]
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
        <?php } 
        wp_reset_query(); ?>
    </div>
</section>
<?php } ?>