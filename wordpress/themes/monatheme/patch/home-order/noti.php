<?php
$title = get_field('m_page_home_noti_title');
$content = get_field('m_page_home_noti_content');
$link = get_field('m_page_home_noti_link');
$img = get_field('m_page_home_noti_image');

?>
<div class="hu-fee">
    <div class="bg">
        <?php if (!empty($img)) {
            echo wp_get_attachment_image($img, 'full');
        } else {
            echo  '<img src="' . get_site_url() . '/template/assets/images/default-image.jpg" alt="">';
        }
        ?>
    </div>
    <div class="container">
        <div class="hu-fee-wr">
            <h3 class="title white" data-aos="zoom-in">
                <?php echo $title; ?>
            </h3>
            <p class="desc" data-aos="zoom-in">
                <?php echo $content; ?>
            </p>
            <?php
            if (!empty($link['url'])) {
            ?>
                <a href="<?php echo $link['url']; ?>" class="btn-second" data-aos="zoom-in">
                    <span class="txt"><?php echo $link['title']; ?></span>
                </a>
            <?php } ?>
        </div>
    </div>
</div>