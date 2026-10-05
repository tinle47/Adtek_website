<?php
    $mona_partners = get_field('mona_partners');
    if( !empty($mona_partners) ){
?>
<section class="section partners" data-aos="fade-up">
    <div class="container">
        <div class="partners-slide tab-panel active">
            <div class="swiper-container">
                <div class="swiper-wrapper partners-list">
                    <?php foreach ($mona_partners as $key => $partner_id) { ?>
                    <div class="swiper-slide partners-item">
                        <div class="partners-img">
                            <?php echo wp_get_attachment_image( $partner_id, 'full'); ?>
                        </div>
                    </div>
                    <?php } ?>
                </div>
            </div>

            <!-- <div class="partners-pagin">
                <div class="swiper-pagination"></div>
            </div> -->
        </div>
    </div>
</section>
<?php } ?>
