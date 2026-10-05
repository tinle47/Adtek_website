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
                <h1 class="news-detail-tt"><?php echo get_the_title($post_ID); ?></h1>
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

            <?php 
$reports_contactform = mona_get_option('reports_contactform');
if( !empty($reports_contactform) ){
    $report_file_id  = get_post_meta($post_ID, 'mona_report_file', true);
    $report_file_url = wp_get_attachment_url($report_file_id);
?>
<div class="download section">
    <div class="download-wrap">
        <?php echo do_shortcode($reports_contactform); ?>
    </div>
</div>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        var field = document.querySelector('input[name="your_report_link"]') 
                 || document.querySelector('input[name="your-report-link"]');
        if (field) {
            field.value = '<?php echo esc_js($report_file_url); ?>';
        }
    });
</script>
<?php } ?>
        </div>
    </section>

    <section class="section news read">
        <div class="container">
            <h2 class="sec-tt news-tt sec-tt-left" data-aos="fade-down">
                <?php echo __('Read This Next','monamedia'); ?>
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
            } 
            wp_reset_query(); ?>
        </div>
    </section>

    <?php 
        /*
        ** GET
        ** TEMPLATE PART
        ** global Section Stay in touch
        */
        $slug_part = 'patch/global-content/section';
        $name_part = 'stay-in-touch';
        get_template_part($slug_part, $name_part);
    ?>

</main>