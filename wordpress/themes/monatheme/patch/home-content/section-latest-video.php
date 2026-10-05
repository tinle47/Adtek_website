<?php 
    $mona_videos = get_field('mona_videos');
    if( !empty($mona_videos['youtube_link']) ){
?>
<section class="section latest-video">
    <div class="latest-video-bg" data-aos="fade-up">
        <?php echo wp_get_attachment_image($mona_videos['background'], 'full'); ?>
    </div>
    <div class="container">
        <div class="latest-video-ctn">
            <div class="latest-video-img" data-aos="fade-down">
                <a href="<?php echo $mona_videos['youtube_link'] ?>" class="latest-video-wrap popup-youtube">

                    <?php
                    if( !empty($mona_videos['youtube_thumb']) ){ 
                        echo wp_get_attachment_image($mona_videos['youtube_thumb'], 'full');
                    }else{ ?>
                    <img src="<?php echo get_site_url() ?>/template/assets/images/check-video.png" alt="">
                    <?php } ?>
                    <div class="latest-video-play">
                        <img src="<?php echo get_site_url() ?>/template/assets/images/play.png" alt="">
                    </div>
                </a>
            </div>
            <h2 class="sec-tt latest-video-tt" data-aos="fade-up">
                <?php echo $mona_videos['title']; ?>
            </h2>
            <div class="sec-desc latest-video-desc mona-content" data-aos="fade-up">
                <?php echo $mona_videos['description']; ?>
            </div>
            <?php if( !empty($mona_videos['link']) ){ ?>
            <div class="latest-video-btn" data-aos="fade-up">
                <a href="<?php echo $mona_videos['link']; ?>" class="btn btn-red">
                    <?php echo __('Contact us','monamedia'); ?>
                </a>
            </div>
            <?php } ?>
        </div>
    </div>
</section>
<?php } ?>