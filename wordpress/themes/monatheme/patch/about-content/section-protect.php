<?php 
    $mona_aboutus_protect = get_field('mona_aboutus_protect');
    if( !empty($mona_aboutus_protect) ){
?>
<section class="protect">
    <div class="protect-item"
        style="background-image: url('<?php echo wp_get_attachment_image_url( $mona_aboutus_protect['background'] , 'full'); ?>');">
        <div class="container">
            <div class="protect-text">
                <h2 class="sec-tt protect-tt" data-aos="fade-down">
                    <?php echo $mona_aboutus_protect['title']; ?>
                </h2>
                <?php if( !empty($mona_aboutus_protect['link']) ){ ?>
                <div class="protect-btn" data-aos="fade-up">
                    <a href="<?php echo $mona_aboutus_protect['link']; ?>" class="btn">
                        <?php echo __('Explore','monamedia'); ?>
                        <img src="<?php echo get_site_url() ?>/template/assets/images/btn-arrow.svg" alt="">
                    </a>
                </div>
                <?php } ?>
            </div>
        </div>
    </div>
</section>
<?php } ?>