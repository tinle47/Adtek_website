<?php 
    $mona_stayintouch = get_field('mona_stayintouch');
    if( empty($mona_stayintouch) ){
        $mona_stayintouch = get_field('mona_stayintouch', MONA_PAGE_HOME);
    }
    if( !empty($mona_stayintouch) ){
?>
<section class="section touch">
    <div class="container">
        <h2 class="sec-tt touch-tt" data-aos="fade-down">
            <?php echo $mona_stayintouch['title']; ?>
        </h2>
        <div class="sec-desc touch-desc" data-aos="fade-up">
            <?php echo $mona_stayintouch['description']; ?>
        </div>
        <div class="touch-subscribe" data-aos="fade-up">
            <?php 
                if( !empty($mona_stayintouch['link']) ){
            ?>
            <div class="touch-subscribe-btn">
                <a href="<?php echo $mona_stayintouch['link']; ?>" class="btn">
                    <?php echo $mona_stayintouch['label']; ?>
                </a>
            </div>
            <?php } ?>

            <?php 
                if( !empty($mona_stayintouch['social_network']) ){
            ?>
            <div class="touch-subscribe-social">
                <?php foreach ($mona_stayintouch['social_network'] as $key => $item) { ?>
                <a href="<?php echo $item['social_network_link']; ?>" class="social-item">
                    <?php echo wp_get_attachment_image( $item['social_network_icon'], 'full'); ?>
                </a>
                <?php } ?>
            </div>
            <?php } ?>
        </div>
    </div>
</section>
<?php } ?>