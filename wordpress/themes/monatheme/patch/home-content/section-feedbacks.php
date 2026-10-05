<?php 
        $mona_feedback = get_field('mona_feedback');
        if( !empty($mona_feedback['feedbacks']) ){
    ?>
<section class="section client-say">
    <div class="container">
        <div class="client-say-ctn">
            <div class="client-say-text">
                <h2 class="sec-tt client-say-tt" data-aos="fade-down">
                    <?php echo $mona_feedback['title']; ?>
                </h2>
                <div class="sec-desc client-say-desc" data-aos="fade-up">
                    <?php echo $mona_feedback['description']; ?>
                </div>
                <div class="client-say-text-bg">
                    <?php echo wp_get_attachment_image($mona_feedback['background'], '960x534'); ?>
                </div>
            </div>
            <div class="client-say-content">
                <div class="client-say-content-wrap">
                    <div class="swiper-container">
                        <div class="swiper-wrapper">
                            <?php foreach ($mona_feedback['feedbacks'] as $key_feedback => $feedback_item) { ?>
                            <div class="swiper-slide">
                                <div class="content-item">
                                    <div class="content-quote">
                                        <img src="<?php echo get_site_url() ?>/template/assets/images/quote.svg" alt="">
                                    </div>
                                    <div class="content-text">
                                        <div class="desc">
                                            <?php echo $feedback_item['feedback_content']; ?>
                                        </div>
                                        <div class="customer">
                                            <div class="customer-avt">
                                                <?php echo wp_get_attachment_image( $feedback_item['feedback_avatar'], 'thumbnail'); ?>
                                            </div>
                                            <div class="customer-info">
                                                <div class="name">
                                                    <?php echo $feedback_item['feedback_name']; ?>
                                                </div>
                                                <div class="title">
                                                    <?php echo $feedback_item['feedback_title']; ?>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <?php } ?>
                        </div>
                    </div>
                </div>

                <div class="client-say-navi">
                    <div class="swiper-next">
                        <img src="<?php echo get_site_url() ?>/template/assets/images/navi-arrow.svg" alt="">
                    </div>
                </div>
                <div class="swiper-pagination"></div>
            </div>
        </div>
    </div>
</section>
<?php } ?>