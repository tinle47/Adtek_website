<?php

/**
 * Template name: Home V2 Page
 * @author : Hoàng Phát
 */
get_header('2');
while (have_posts()):
    the_post();
?>
    <style>
        .home #footer {
            display: none;
        }
    </style>
    <?php 
	    if (!function_exists('content_exists')) {
	        function content_exists($content_args = [])
	        {
            if (! empty($content_args)) {
                $done  = 0;
                foreach ($content_args as $value) {
                    if (! is_array($value) && $value != '' || is_array($value) && content_exists($value)) {
                        $done++;
                    }
                }
                return ($done > 0);
            }
            return false;
	        }
	    }
        if (!function_exists('mona_homev2_render_button')) {
            function mona_homev2_render_button($button_text = '', $link = '')
            {
                if (empty($button_text)) {
                    return;
                }

                $link = is_string($link) ? trim($link) : '';
                $is_cf7_shortcode = $link && strpos($link, '[contact-form-7') !== false;

                if ($is_cf7_shortcode) {
                    $popup_id = 'mona-cf7-popup-' . uniqid();
                    ?>
                    <button type="button" class="btn js-mona-cf7-popup-open" data-popup-target="#<?php echo esc_attr($popup_id); ?>">
                        <span class="txt"><?php echo esc_html($button_text); ?></span>
                        <span class="icon">
                            <img src="<?php echo esc_url(get_site_url() . '/template-v2/assets/images/ver2/ic-arrow.svg'); ?>" alt="">
                        </span>
                    </button>
                    <div id="<?php echo esc_attr($popup_id); ?>" class="mona-cf7-popup" aria-hidden="true">
                        <div class="mona-cf7-popup__overlay" data-mona-cf7-popup-close></div>
                        <div class="mona-cf7-popup__content" role="dialog" aria-modal="true">
                            <button type="button" class="mona-cf7-popup__close" data-mona-cf7-popup-close aria-label="<?php esc_attr_e('Close', 'monamedia'); ?>">×</button>
                            <?php echo do_shortcode($link); ?>
                        </div>
                    </div>
                    <?php
                    return;
                }
                ?>
                <a href="<?php echo esc_url($link); ?>" class="btn">
                    <span class="txt"><?php echo esc_html($button_text); ?></span>
                    <span class="icon">
                        <img src="<?php echo esc_url(get_site_url() . '/template-v2/assets/images/ver2/ic-arrow.svg'); ?>" alt="">
                    </span>
                </a>
                <?php
            }
        }
	    ?>
    <main class="main page-homever2">
        <div id="fullpage">
            <?php /* --- SECTION BANNER --- */ ?>
            <?php $mona_home_banner = get_field('mona_home_banner');
            if (content_exists($mona_home_banner)) { ?>
                <section class="sec-homever2-bn section " id="section-banner">
                    <div class="homever2-bn">
                        <div class="bg">
                            <?php echo wp_get_attachment_image($mona_home_banner['image'], 'full'); ?>
                        </div>
                        <div class="container">
                            <div class="homever2-bn-ctn">
                                <h1 class="homever2-bn-tt"><?php echo $mona_home_banner['title']; ?></h1>
                                <p class="homever2-bn-des"><?php echo $mona_home_banner['content']; ?></p>
	                                <div class="btn-box">
	                                    <?php mona_homev2_render_button($mona_home_banner['btn'], $mona_home_banner['link']); ?>
	                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            <?php } ?>

            <?php /* --- SECTION SERVICES --- */ ?>
            <?php $mona_home_service = get_field('mona_home_service');
            if (content_exists($mona_home_service)) {
                $mona_home_service_sub = get_field('mona_home_service_sub');
                foreach ($mona_home_service as $key => $value) {
            ?>
                    <section class="sec-homever2-brand homever2-slide-it section" id="section<?php echo $key + 1; ?>">
                        <?php if ($key == 0) : ?>
                            <div class="homever2-heading" id="element<?php echo $key + 1; ?>">
                                <div class="container">
                                    <h2 class="tt"><?php echo $mona_home_service_sub ?></h2>
                                </div>
                            </div>
                        <?php endif; ?>
                        <div class="homever2-brand ss-pd">
                            <div class="recontainer">
                                <div class="homever2-brand-flex">
                                    <div class="homever2-brand-ctn">
                                        <div class="wrapper">
                                            <h3 class="homever2-tt"><?php echo $value['title']; ?></h3>
                                            <p class="homever2-des"><?php echo $value['content']; ?></p>
                                            <?php if (!empty($value['repeater'])) { ?>
                                                <div class="homever2-boxs">
                                                    <p class="text"><?php _e('Dịch vụ bao gồm:', 'moanmedia') ?></p>
                                                    <div class="homever2-its">
                                                        <?php foreach ($value['repeater'] as $item) { ?>
                                                            <div class="homever2-it">
                                                                <div class="inner">
                                                                    <?php echo wp_get_attachment_image($item['image'], 'full'); ?>
                                                                    <span class="txt"><?php echo $item['content']; ?></span>
                                                                </div>
                                                            </div>
                                                        <?php } ?>
                                                    </div>
                                                </div>
                                            <?php } ?>
	                                            <div class="btn-box">
	                                                <?php mona_homev2_render_button($value['btn'], $value['link']); ?>
	                                            </div>
                                        </div>
                                    </div>
                                    <div class="homever2-brand-img">
                                        <div class="wrapper">
                                            <h3 class="homever2-tt tt-mobille "><?php echo $value['title']; ?></h3>
                                            <div class="img">
                                                <div class="img-inner">
                                                    <?php for ($i = 1; $i <= 3; $i++): $img_key = ($i == 1) ? 'image' : "image_$i"; ?>
                                                        <?php if (!empty($value[$img_key])): ?>
                                                            <div class="part<?php echo $i; ?>">
                                                                <?php echo wp_get_attachment_image($value[$img_key], 'full'); ?>
                                                            </div>
                                                        <?php endif; ?>
                                                    <?php endfor; ?>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>
            <?php } } ?>

            <?php /* --- SECTION ĐỘI NGŨ --- */ ?>
            <?php $mona_home_doingu = get_field('mona_home_doingu');
            if (content_exists($mona_home_doingu)) { ?>
                <section class="sec-homever2-hand section fp-auto-height" id="section-hand">
                    <div class="homever2-hand">
                        <div class="bg"><?php echo wp_get_attachment_image($mona_home_doingu['image'], 'full'); ?></div>
                        <div class="container">
                            <div class="homever2-hand-wrap">
                                <div class="ctn">
                                    <h3 class="homever2-tt"><?php echo $mona_home_doingu['title']; ?></h3>
                                    <div class="homever2-des"><?php echo $mona_home_doingu['content']; ?></div>
	                                    <div class="btn-box">
	                                        <?php mona_homev2_render_button($mona_home_doingu['btn'], $mona_home_doingu['link']); ?>
	                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            <?php } ?>

            <?php /* --- SECTION VỀ CHÚNG TÔI --- */ ?>
            <?php $mona_home_vechungtoi = get_field('mona_home_vechungtoi');
            if (content_exists($mona_home_vechungtoi)) { ?>
                <section class="sec-homever2-rocket section" id="section-rocket">
                    <div class="homever2-rocket ss-pd">
                        <div class="cloud"><img src="<?php echo get_site_url() ?>/template-v2/assets/images/ver2/cloud.png" alt=""></div>
                        <div class="container">
                            <div class="homever2-sub"><?php echo $mona_home_vechungtoi['sub']; ?></div>
                            <div class="homever2-rocket-flex">
                                <div class="homever2-rocket-img">
                                    <div class="wrapper">
                                        <div class="img" data-aos="fade-up">
                                            <div class=" img-inner"><?php echo wp_get_attachment_image($mona_home_vechungtoi['image'], 'full'); ?></div>
                                        </div>
                                    </div>
                                </div>
                                <div class="homever2-rocket-ctn">
                                    <div class="ctn">
                                        <h3 class="homever2-tt"><?php echo $mona_home_vechungtoi['title']; ?></h3>
                                        <div class="homever2-des"><?php echo $mona_home_vechungtoi['content']; ?></div>
	                                        <div class="btn-box">
	                                            <?php mona_homev2_render_button($mona_home_vechungtoi['btn'], $mona_home_vechungtoi['link']); ?>
	                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                </section>
            <?php } ?>

            <?php /* --- SECTION ĐỐI TÁC --- */ ?>
            <?php $mona_home_doitac = get_field('mona_home_doitac');
            if (content_exists($mona_home_doitac)) { ?>
                <section class="sec-homever2-partner section fp-auto-height" id="section-partner">
                    <div class="homever2-heading center">
                        <div class="container">
                            <h2 class="tt"><?php echo $mona_home_doitac['title']; ?></h2>
                        </div>
                    </div>
                    <?php if (!empty($mona_home_doitac['repeater'])) { ?>
                        <div class="homever2-partner-tab tabJS">
                            <div class="homever2-partner-head">
                                <div class="contaier">
                                    <div class="homever2-partner-btns scrollContainer">
                                        <?php foreach ($mona_home_doitac['repeater'] as $key => $item) { ?>
                                            <div class="homever2-partner-btn tabBtn buttons <?php echo $key == 0 ? 'active' : ''; ?>">
                                                <?php echo $item['title']; ?>
                                            </div>
                                        <?php } ?>
                                    </div>
                                </div>
                            </div>
                            <div class="container">
                                <div class="homever2-partner-panels">
                                    <?php foreach ($mona_home_doitac['repeater'] as $key => $item) { ?>
                                        <div class="homever2-partner-panel tabPanel <?php echo $key == 0 ? 'open' : ''; ?>">
                                            <div class="homever2-partner-flex swiper row gap-res">
                                                <div class="swiper-wrapper">
                                                    <?php if(!empty($item['album'])) foreach ($item['album'] as $value) { ?>
                                                        <div class="swiper-slide col">
                                                            <div class="homever2-partner-it">
                                                                <div class="img">
                                                                    <a href="javascript:void(0)" class="img-inner"><?php echo wp_get_attachment_image($value, 'full'); ?></a>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    <?php } ?>
                                                </div>
                                            </div>
                                        </div>
                                    <?php } ?>
                                </div>
                            </div>
                        </div>
                    <?php } ?>
                </section>
            <?php } ?>

            <?php /* --- SECTION BÀI VIẾT MỚI NHẤT --- */ ?>
            <?php
            // WPML tự lọc theo ngôn ngữ trang: /en/ chưa có bài thì khối tự ẩn.
            $mona_home_news = new WP_Query([
                'post_type'           => 'post',
                'post_status'         => 'publish',
                'posts_per_page'      => 3,
                'ignore_sticky_posts' => true,
                'no_found_rows'       => true,
            ]);
            // Dấu để kiểm tra từ xa: file mới đã chạy chưa, lấy được mấy bài.
            echo '<!-- adtek-home-news v1: ' . (int) $mona_home_news->post_count . ' -->';
            if ($mona_home_news->have_posts()) {
                $is_en = apply_filters('wpml_current_language', null) === 'en';
                $news_blog_id = (int) get_option('page_for_posts');
                $news_blog_url = $news_blog_id ? get_permalink($news_blog_id) : home_url('/blog/');
            ?>
                <style>
                    .homever2-news { padding: 0 0 6rem; }
                    .homever2-news-list { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 2.4rem; margin-top: 3.2rem; }
                    .homever2-news-it { display: flex; flex-direction: column; border: 0.1rem solid var(--cl-bd); border-radius: 1.6rem; overflow: hidden; background: #fff; transition: 0.4s; }
                    .homever2-news-it:hover { box-shadow: 0 1.2rem 3rem rgba(3, 13, 66, 0.1); }
                    .homever2-news-img { display: block; aspect-ratio: 1200 / 630; overflow: hidden; background: #f3f4f8; }
                    .homever2-news-img img { width: 100%; height: 100%; object-fit: cover; transition: 0.4s; }
                    .homever2-news-it:hover .homever2-news-img img { transform: scale(1.04); }
                    .homever2-news-body { display: flex; flex-direction: column; gap: 1rem; padding: 2rem 2.4rem 2.4rem; flex: 1; }
                    .homever2-news-meta { font-size: 1.3rem; color: var(--color-second); font-weight: 500; }
                    .homever2-news-tt { font-size: 1.8rem; line-height: 1.4; font-weight: 600; color: var(--color-pri); display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
                    .homever2-news-tt a { color: inherit; }
                    .homever2-news-tt a:hover { color: var(--color-second); }
                    html:has(.page-homever2) .sec-homever2-news .btn-box { margin: 3.2rem auto 0; }
                    @media screen and (max-width: 1024px) {
                        .homever2-news-list { gap: 1.6rem; }
                        .homever2-news-body { padding: 1.6rem; }
                        .homever2-news-tt { font-size: 1.6rem; }
                    }
                    /* Mobile: carousel vuốt ngang, thẻ rộng 85% để thẻ kế tiếp ló ra; scroll-snap giữ thẻ đứng ngay ngắn sau khi thả tay. */
                    @media screen and (max-width: 768px) {
                        .homever2-news .container { padding-right: 0; }
                        .homever2-news-list { display: flex; gap: 1.6rem; overflow-x: auto; scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch; scrollbar-width: none; padding-right: 1.6rem; }
                        .homever2-news-list::-webkit-scrollbar { display: none; }
                        .homever2-news-it { flex: 0 0 85%; scroll-snap-align: start; }
                    }
                </style>
                <section class="sec-homever2-news section fp-auto-height" id="section-news">
                    <div class="homever2-heading center">
                        <div class="container">
                            <h2 class="tt"><?php echo $is_en ? 'Latest insights' : 'Bài viết mới nhất'; ?></h2>
                        </div>
                    </div>
                    <div class="homever2-news">
                        <div class="container">
                            <div class="homever2-news-list">
                                <?php while ($mona_home_news->have_posts()) : $mona_home_news->the_post();
                                    $news_cats = get_the_category();
                                ?>
                                    <article class="homever2-news-it">
                                        <?php if (has_post_thumbnail()) { ?>
                                            <a href="<?php the_permalink(); ?>" class="homever2-news-img">
                                                <?php the_post_thumbnail('medium_large', ['loading' => 'lazy']); ?>
                                            </a>
                                        <?php } ?>
                                        <div class="homever2-news-body">
                                            <div class="homever2-news-meta">
                                                <?php echo esc_html(get_the_date('d/m/Y')); ?>
                                                <?php if (!empty($news_cats)) echo ' · ' . esc_html($news_cats[0]->name); ?>
                                            </div>
                                            <h3 class="homever2-news-tt">
                                                <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                                            </h3>
                                        </div>
                                    </article>
                                <?php endwhile; ?>
                            </div>
                            <div class="btn-box">
                                <?php mona_homev2_render_button($is_en ? 'View all articles' : 'Xem tất cả bài viết', $news_blog_url); ?>
                            </div>
                        </div>
                    </div>
                </section>
            <?php }
            // Trả lại bài của trang chủ cho các trường ACF bên dưới (Footer).
            wp_reset_postdata(); ?>

            <?php /* --- SECTION FOOTER --- */ ?>
            <?php $mona_home_footer = get_field('mona_home_footer');
            if (content_exists($mona_home_footer)) { ?>
                <section class="ft section fp-auto-height" id="section-footer">
                    <div class="ft-wrapper">
                        <div class="bg">
                            <img src="<?php echo get_site_url() ?>/template-v2/assets/images/ver2/ft-bg.jpg" alt="">
                        </div>
                        <div class="container">
                            <div class="ft-box">
                                <div class="ft-logo">
                                    <a href="<?php echo home_url(); ?>">
                                        <?php echo wp_get_attachment_image($mona_home_footer['logo'], 'full'); ?>
                                    </a>
                                </div>
                                <div class="social">
                                    <div class="social-list">
                                        <?php if(!empty($mona_home_footer['repeater'])) foreach ($mona_home_footer['repeater'] as $value) { ?>
                                            <a href="<?php echo $value['link']; ?>" target="_blank" class="social-link">
                                                <?php echo wp_get_attachment_image($value['image'], 'full'); ?>
                                            </a>
                                        <?php } ?>
                                    </div>
                                </div>
                                <div class="ft-flex row">
                                    <div class="ft-it col">
                                        <div class="wrapper">
                                            <p class="tt"><?php echo $mona_home_footer['title']; ?></p>
                                            <div class="des"><?php echo $mona_home_footer['content']; ?></div>
                                        </div>
                                    </div>
                                    <div class="ft-it col">
                                        <div class="wrapper">
                                            <p class="tt"><?php echo $mona_home_footer['title_2']; ?></p>
                                            <?php if (!empty($mona_home_footer['repeater_2'])) { ?>
                                                <div class="lines">
                                                    <?php foreach ($mona_home_footer['repeater_2'] as $value) { ?>
                                                        <a href="<?php echo $value['link']; ?>" class="line"><?php echo $value['content']; ?></a>
                                                    <?php } ?>
                                                </div>
                                            <?php } ?>
                                        </div>
                                    </div>

                                    <?php 
                                    // Danh sách các location menu cần hiển thị
                                    $menu_locations = ['footer-menu', 'footer-menu-2'];
                                    foreach ($menu_locations as $location) : 
                                        // Kiểm tra nếu location này đã được gán menu trong Admin thì mới hiển thị
                                        if ( has_nav_menu( $location ) ) :
                                            $menu_name = wp_get_nav_menu_name($location);
                                    ?>
                                        <div class="ft-it col">
                                            <div class="wrapper">
                                                <p class="tt"><?php echo esc_html($menu_name); ?></p>
                                                <?php
                                                wp_nav_menu(array(
                                                    'container' => false,
                                                    'theme_location' => $location,
                                                    'menu_class' => 'menu-list',
                                                    'fallback_cb' => false,
                                                    'walker' => new Mona_Custom2_Walker_Nav_Menu,
                                                ));
                                                ?>
                                            </div>
                                        </div>
                                    <?php 
                                        endif; 
                                    endforeach; 
                                    ?>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            <?php } ?>
        </div>
    </main>
<?php
endwhile;
get_footer('2');
?>