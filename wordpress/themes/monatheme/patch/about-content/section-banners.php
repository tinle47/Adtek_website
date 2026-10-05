<?php 
    $mona_aboutus_banners = get_field('mona_aboutus_banners');
    if( !empty($mona_aboutus_banners['banner']) ){
        if(wp_is_mobile()){
            $banner_url = wp_get_attachment_image_url( $mona_aboutus_banners['banner_mobile'] , '474x474');
        }else{
            $banner_url = wp_get_attachment_image_url( $mona_aboutus_banners['banner'] , 'full');
        }

?>
<div class="banner-s">
    <div class="banner-s-item" style="background-image: url(<?php echo $banner_url; ?>);">
        <div class="banner-s-text">
            <div class="container">
                <?php if( !empty($mona_aboutus_banners['title']) ){ ?>
                <h1 class="banner-s-tt" data-aos="fade-down">
                    <?php echo $mona_aboutus_banners['title']; ?>
                </h1>
                <?php } ?>

                <?php if( !empty($mona_aboutus_banners['description']) ){ ?>
                <p class="banner-s-desc" data-aos="fade-up">
                    <?php echo $mona_aboutus_banners['description']; ?>
                </p>
                <?php } ?>

                <?php if( !empty($mona_aboutus_banners['statistical_information']['statistical_list']) ){ ?>
                <div class="statistical">
                    <div class="statistical-wrap" data-aos="fade-up">
                        <div class="statistical-text">
                            <?php echo $mona_aboutus_banners['statistical_information']['statistical_title']; ?>
                        </div>
                        <div class="statistical-list">
                            <?php foreach ($mona_aboutus_banners['statistical_information']['statistical_list'] as $key_statistical => $statistical_item) { ?>
                            <div class="statistical-item">
                                <div class="statistical-item-wrap">
                                    <div class="statistical-icon">
                                        <?php echo wp_get_attachment_image( $statistical_item['icon'], '50x50'); ?>
                                    </div>
                                    <div class="statistical-number">
                                        <p class="countNum"><?php echo  $statistical_item['number']; ?></p>
                                    </div>
                                    <div class="statistical-desc"><?php echo  $statistical_item['description']; ?>
                                    </div>
                                </div>
                            </div>
                            <?php } ?>
                        </div>
                    </div>
                </div>
                <?php } ?>
            </div>
        </div>
    </div>
</div>
<?php } ?>