<?php 
    $mona_home_banners = get_field('mona_home_banners');
    if( !empty($mona_home_banners) ){
?>
<div class="banner">
    <div class="swiper-container">
        <div class="swiper-wrapper">
            <?php 
                foreach ($mona_home_banners as $key => $banner_item) {
                    if(wp_is_mobile()){
                        $banner_img = wp_get_attachment_image( $banner_item['banner_mobile'], 'full');
                    }else{
                        $banner_img = wp_get_attachment_image( $banner_item['banner_desktop'], 'full');
                    }
            ?>
            <div class="swiper-slide banner-item">
                <div class="banner-img">
                    <?php echo $banner_img; ?>
                </div>
                <div class="banner-text">
                    <div class="container">
                        <div class="banner-text-wrap">
                            <h1 class="banner-tt">
                                <?php echo $banner_item['banner_title']; ?>
                            </h1>
                            <div class="banner-desc">
                                <?php echo $banner_item['banner_description']; ?>
                            </div>
                            <?php 
                                if( !empty($banner_item['banner_contactform_enable']) && !empty($banner_item['banner_contactform_shortcode']) ){
                            ?>
                            <div class="banner-email">
                                <?php echo do_shortcode($banner_item['banner_contactform_shortcode']); ?>
                            </div>
                            <?php } ?>
                        </div>
                    </div>
                </div>
            </div>
            <?php } ?>
        </div>
    </div>

    <div class="banner-navi">
        <?php 
        if(wp_is_mobile()){ ?>

        <div class="swiper-pagination"></div>

        <?php
        }else{ ?>

        <div class="swiper-prev">
            <img src="<?php echo get_site_url() ?>/template/assets/images/slider-icon2.svg" alt="">
        </div>
        <div class="swiper-next">
            <img src="<?php echo get_site_url() ?>/template/assets/images/slider-icon2.svg" alt="">
        </div>

        <?php }
        ?>
    </div>
</div>

<?php } ?>