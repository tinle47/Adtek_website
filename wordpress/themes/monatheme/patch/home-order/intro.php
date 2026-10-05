<?php
$title_sec = get_field('m_page_home_banner_intro_title');
$content_sec = get_field('m_page_home_banner_intro_content');
$list = get_field('m_page_home_banner_intro_list_intro');
?>
<div class="hu-sol">
    <div class="container">
        <div class="hu-sol-wr">
            <h3 class="title" data-aos="fade-up">
                <?php echo $title_sec; ?>
            </h3>
            <p class="hu-sol-desc" data-aos="fade-up">
                <?php echo $content_sec; ?>
            </p>
        </div>
    </div>
    <?php if (!empty($list)) { ?>
        <div class="hu-sol-block">
            <?php foreach ($list as $list_item) {
                $title = $list_item['m_page_home_banner_intro_list_intro_title'];
                $content = $list_item['m_page_home_banner_intro_list_intro_content'];
                $link = $list_item['m_page_home_banner_intro_list_intro_link'];
                $image = $list_item['m_page_home_banner_intro_list_intro_image'];
            ?>
                <div class="hu-sol-item">
                    <div class="container">
                        <div class="dnor">
                            <div class="dnor-item hu-sol-content">
                                <h4 class="tt" data-aos="fade-up">
                                    <?php echo $title; ?>
                                </h4>
                                <p class="desc" data-aos="fade-up">
                                    <?php echo $content; ?>
                                </p>
                                <?php if ($link['url']) { ?>
                                    <a href="  <?php echo $link['url']; ?>" class="btn-second" data-aos="fade-up">
                                        <span class="txt"> <?php echo $link['title']; ?></span>
                                    </a>
                                <?php } ?>
                            </div>
                            <div class="dnor-item hu-sol-img" data-aos="zoom-in">
                                <div class="inner">
                                    <?php if (!empty($image)) {
                                        echo wp_get_attachment_image($image, 'larger');
                                    } else {
                                        echo  '<img src="' . get_site_url() . '/template/assets/images/default-image.jpg" alt="">';
                                    }
                                    ?>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            <?php } ?>
        </div>
    <?php } ?>
</div>