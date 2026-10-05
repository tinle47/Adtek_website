<?php
$title_sec = get_field('m_page_solution_banner_intro_title');
$content_sec = get_field('m_page_solution_banner_intro_content');
$list = get_field('m_page_solution_banner_intro_list_intro');
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
    <?php
    $post_per = 6;
    $argsPost = array(
        'post_type' => 'mona_solution',
        'post_status' => 'publish',
        'posts_per_page' => $post_per,
        // 'order' => $order,


    );
    if (!empty($rel)) {
        $argsPost['post__in'] = $rel;
    }
    $loop = new WP_Query($argsPost);
    if ($loop->have_posts()) {
    ?>
        <div class="hu-sol-slide">
            <div class="container">
                <div class="swiper-container">
                    <div class="swiper-wrapper">
                        <?php
                        while ($loop->have_posts()) :
                            $loop->the_post();
                            global $post;
                            $post_ID = $post->ID;
                        ?>
                            <div class="swiper-slide">
                                <div class="hu-sol-card">
                                    <div class="inner">
                                        <div class="img">
                                            <a href="<?php the_permalink(); ?>" class="img-inner">
                                                <?php the_post_thumbnail(); ?>
                                            </a>
                                        </div>
                                        <div class="info">
                                            <h4>
                                                <a href="<?php the_permalink(); ?>" class="info-tt">
                                                    <?php the_title(); ?>
                                                </a>
                                            </h4>
                                            <div class="desc">
                                                <?php the_excerpt(); ?>
                                            </div>
                                            <a href="<?php the_permalink(); ?>" class="btn-four">
                                                <span class="txt">
                                                    <?php _e('Xem thêm', 'monamedia'); ?>
                                                </span>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        <?php
                        endwhile;
                        wp_reset_query();
                        ?>
                    </div>
                    <div class="swiper-pagination"></div>
                </div>
                <div class="swiper-button-prev"></div>
                <div class="swiper-button-next"></div>
            </div>
        </div>
    <?php } ?>
    <?php if (!empty($list)) { ?>
        <div class="hu-sol-block">
            <?php foreach ($list as $list_item) {
                $title = $list_item['m_page_solution_banner_intro_list_intro_title'];
                $content = $list_item['m_page_solution_banner_intro_list_intro_content'];
                $link = $list_item['m_page_solution_banner_intro_list_intro_link'];
                $image = $list_item['m_page_solution_banner_intro_list_intro_image'];
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