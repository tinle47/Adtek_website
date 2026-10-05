<?php
    $mona_aboutus_descriptions = get_field('mona_aboutus_descriptions');
    if( empty($mona_aboutus_descriptions) ){
        $mona_aboutus_descriptions = get_field('mona_aboutus_descriptions', MONA_PAGE_HOME);
    }
    if( !empty($mona_aboutus_descriptions) ){
?>
<section class="section about">
    <div class="container">
        <div class="about-ctn">
            <div class="about-text">
                <?php
                    if( !empty($mona_aboutus_descriptions['title']) ){
                ?>
                <h2 class="sec-tt about-tt" data-aos="fade-down">
                    <?php echo $mona_aboutus_descriptions['title']; ?>
                </h2>
                <?php } ?>

                <?php
                    if( !empty($mona_aboutus_descriptions['description']) ){
                ?>
                <div class="sec-desc about-desc mona-content" data-aos="fade-up">
                    <?php echo $mona_aboutus_descriptions['description']; ?>
                </div>
                <?php } ?>

                <?php
                    if( !empty($mona_aboutus_descriptions['link']) ){
                ?>
                <div class="about-btn" data-aos="fade-up">
                    <a href="<?php echo $mona_aboutus_descriptions['link']; ?>" class="btn">
                        <?php echo __('Explore','monamedia'); ?>
                        <img src="<?php echo get_site_url() ?>/template/assets/images/btn-arrow.svg" alt="">
                    </a>
                </div>
                <?php } ?>
            </div>
            <?php if ( wp_is_mobile() ) { ?>
            <div class="about-img about-mobile-images">
                <?php if ( ! empty( $mona_aboutus_descriptions['decor_img_mobile'] ) ) { ?>
                <div class="ab-image-mobile">
                    <div class="swiper-container">
                        <div class="swiper-wrapper">
                            <?php foreach ( $mona_aboutus_descriptions['decor_img_mobile'] as $key_img => $id_img) { ?>
                            <div class="swiper-slide img-item-mobile">
                                 <?php echo wp_get_attachment_image( $id_img, '570x345'); ?>
                            </div>
                            <?php } ?>
                        </div>
                    </div>
                    <div class="swiper-pagination"></div>
                </div>
                <?php } ?>
            </div>
            <?php } else { ?>
            <div class="about-img">
                <?php if( !empty($mona_aboutus_descriptions['decor_img']) ){ ?>
                <div class="img-list">
                    <?php
                        $stt = 1;
                        foreach ($mona_aboutus_descriptions['decor_img'] as $key_img => $id_img) {
                            $dataAOS_img = $stt==1?'fade-down-right':$dataAOS_img;
                            $dataAOS_img = $stt==2?'fade-down-left':$dataAOS_img;
                            $dataAOS_img = $stt==3?'fade-up-left':$dataAOS_img;
                    ?>
                    <div class="img-item" data-aos="<?php echo $dataAOS_img; ?>">
                        <?php echo wp_get_attachment_image( $id_img, 'full'); ?>
                    </div>

                    <?php
                        $stt++;
                        } ?>
                </div>
                <?php } ?>
            </div>
            <?php } ?>
        </div>
    </div>
</section>
<?php } ?>
