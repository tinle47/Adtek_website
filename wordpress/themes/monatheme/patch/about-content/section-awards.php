<?php 
    $mona_aboutus_awards = get_field('mona_aboutus_awards');
    if( !empty($mona_aboutus_awards['awards']) ){
?>
<section class="section awards">
    <div class="container">
        <h2 class="sec-tt awards-tt" data-aos="fade-down"><?php echo $mona_aboutus_awards['title']; ?></h2>
        <div class="sec-desc awards-desc" data-aos="fade-up">
            <?php echo $mona_aboutus_awards['description']; ?>
        </div>
        <div class="awards-slide" data-aos="fade-up">
            <div class="swiper-container">
                <div class="swiper-wrapper">
                    <?php  foreach ($mona_aboutus_awards['awards']  as $key => $id) {?>
                    <div class="swiper-slide awards-item">
                        <div class="awards-img">
                            <?php echo wp_get_attachment_image( $id, 'full'); ?>
                        </div>
                    </div>
                    <?php } ?>
                </div>
            </div>
            <div class="awards-pagin">
                <div class="swiper-pagination"></div>
            </div>
        </div>
    </div>
</section>
<?php } ?>