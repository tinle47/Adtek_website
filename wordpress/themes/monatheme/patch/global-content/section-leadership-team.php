<?php 
    $mona_aboutus_leadership_team = get_field('mona_aboutus_leadership_team');
    if( empty($mona_aboutus_leadership_team) ){
        $mona_aboutus_leadership_team = get_field('mona_aboutus_leadership_team', MONA_PAGE_HOME);
    }
    if( !empty($mona_aboutus_leadership_team['team']) ){
?>
<section class="section team about">
    <div class="container">
        <h2 class="sec-tt team-tt" data-aos="fade-down"><?php echo $mona_aboutus_leadership_team['title']; ?></h2>
        <div class="sec-desc team-desc" data-aos="fade-up">
            <?php echo $mona_aboutus_leadership_team['description']; ?>
        </div>

        <div class="team-box">
            <div class="swiper-container team-slide">
                <div class="swiper-wrapper team-list">
                    <?php 
                        $delayAOS_team = 100;
                        foreach ( $mona_aboutus_leadership_team['team'] as $key_team => $team_item) {
                            $position       = get_field('position',$team_item);
                            $social_network = get_field('social_network',$team_item);
							$description_information = get_field('description_information',$team_item);
                    ?>
                    <div class="swiper-slide team-item" data-aos="fade-up"
                        data-aos-delay="<?php echo $delayAOS_team; ?>">
                        <div class="team-wrap">
                            <div class="team-img">
                                <?php echo get_the_post_thumbnail($team_item, '270x295'); ?>
                            </div>
                            <div class="team-body">
                                <div class="team-title"><?php echo $position; ?></div>
								<div class="team-name"><?php echo get_the_title($team_item); ?></div>
								<div class="team-description"><?php echo $description_information; ?></div>
                                <?php 
                                    if( !empty($social_network) ){
                                ?>
                                <div class="team-social">
                                    <?php foreach ($social_network as $key => $social_network_item) { ?>
                                    <a href="<?php echo $social_network_item['link']; ?>" class="team-social-item"
                                        target="_blank">
                                        <?php echo wp_get_attachment_image( $social_network_item['icon'], '50x50'); ?>
                                    </a>
                                    <?php } ?>
                                </div>
                                <?php } ?>
                            </div>
                        </div>
                    </div>
                    <?php 
                        $delayAOS_team+=200;
                    } ?>
                </div>
            </div>
            <div class="team-navi">
                <div class="swiper-prev">
                    <img src="<?php echo get_site_url() ?>/template/assets/images/navi-arrow.svg" alt="">
                </div>
                <div class="swiper-next">
                    <img src="<?php echo get_site_url() ?>/template/assets/images/navi-arrow.svg" alt="">
                </div>
            </div>
        </div>
    </div>
</section>
<?php } ?>