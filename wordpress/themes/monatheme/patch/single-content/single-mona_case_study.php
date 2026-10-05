<?php 
    global $post;
    $post_ID = $post->ID;
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

    <section class="news-detail" data-aos="fade-up">
        <div class="container">
            <div class="news-detail-wrap">
                <h1 class="news-detail-tt">
                    <?php echo get_the_title($post_ID); ?>
                </h1>
                <div class="news-time news-detail-time">
                    <img src="<?php echo get_site_url() ?>/template/assets/images/calendar.svg" alt="">
                    <?php echo get_the_date('F d, Y', $post_ID) ?>
                </div>

                <?php
                $mona_post_detail_image = get_field('mona_post_detail_image',$post_ID);
                if ( $mona_post_detail_image ) {
                ?>
                <div class="blog-item-img">
                    <?php echo wp_get_attachment_image( $mona_post_detail_image, 'full' ) ?>
                </div>
                <?php } ?>

                <div class="mona-content">
                    <?php echo the_content(); ?>
                </div>
            </div>

            <div class="share" data-aos="fade-up">
                <div class="share-text">
                    <?php echo __('Share','monamedia'); ?>
                </div>
                <div class="share-social">
                    <a onclick="javascript:window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=500');return false;"
                        href="https://www.facebook.com/sharer/sharer.php?u=<?php echo urlencode(get_the_permalink()); ?>&t=<?php the_title(); ?>">
                        <img src="<?php echo get_site_url() ?>/template/assets/images/share-fb.svg" alt="">
                    </a>
                    <a onclick="javascript:window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=500');return false;"
                        href="http://www.twitter.com/share?url=<?php echo urlencode(get_the_permalink()); ?>">
                        <img src="<?php echo get_site_url() ?>/template/assets/images/share-tw.svg" alt="">
                    </a>
                    <a onclick="javascript:window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=500');return false;"
                        href="https://www.linkedin.com/cws/share?url=<?php echo urlencode(get_the_permalink()); ?>&title=<?php the_title(); ?>">
                        <img src="<?php echo get_site_url() ?>/template/assets/images/share-in.svg" alt="">
                    </a>
                </div>
            </div>
        </div>
    </section>

	<?php 
	$order = 'DESC';

							 $argsPost = array(
								 'post_type' => 'mona_case_study',
								 'post_status' => 'publish',
								 'posts_per_page' => 9,
								 'post__not_in'=> (array)get_the_ID(),
								 // 'paged' => $paged,
								 // 'offset' => $offset,
								 'order' => $order,
							 );

							 $loop = new WP_Query($argsPost);
							 if( $loop->have_posts() ){
	?>
    <section class="section news related-glossary-mona">
        <div class="container">
            <h2 class="sec-tt news-tt sec-tt-left" data-aos="fade-down">
                <?php echo __('Related Posts','monamedia'); ?>
            </h2>
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
                        } wp_reset_query(); ?>
                    </div>
                </div>
            </div>
        </div>
    </section>
	<?php } ?>
</main>