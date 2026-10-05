<?php
$title = get_field('m_page_home_leader_title');
$list = get_field('m_page_home_leader_list');
if (!empty($list)) {
?>

    <div class="hu-lead sc-pd4">
        <div class="container">
            <h3 class="title" data-aos="fade-up">
                <?php echo $title; ?>
            </h3>

            <div class="hu-lead-wr">
                <div class="swiper-container" data-aos="fade-up">
                    <div class="swiper-wrapper">
                        <?php foreach ($list as $list) {
                            $name = $list['m_page_home_leader_list_name'];
                            $img = $list['m_page_home_leader_list_image'];
                            $infor = $list['m_page_home_leader_list_infor'];
                        ?>
                            <div class="swiper-slide">
                                <div class="hu-lead-it">
                                    <div class="inner">
                                        <div class="img">
                                            <div class="img-inner">
                                                <?php if (!empty($img)) {
                                                    echo wp_get_attachment_image($img, 'larger');
                                                } else {
                                                    echo  '<img src="' . get_site_url() . '/template/assets/images/default-image.jpg" alt="">';
                                                }
                                                ?>
                                            </div>
                                        </div>
                                        <div class="info">
                                            <h4>
                                                <p class="info-tt">
                                                    <?php echo $name; ?>
                                                </p>
                                            </h4>
                                            <p class="desc">
                                                <?php echo $infor; ?>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        <?php } ?>
                    </div>
                </div>
            </div>
        </div>
    </div>
<?php } ?>