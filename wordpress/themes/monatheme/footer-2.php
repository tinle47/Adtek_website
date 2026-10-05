<?php 
$mona_home_footer = get_field('mona_home_footer', MONA_PAGE_HOME);
if (content_exists($mona_home_footer)) : 
?>
    <section class="ft section fp-auto-height" id="footer">
        <div class="ft-wrapper">
            <div class="bg">
                <img src="<?php echo get_site_url(); ?>/template-v2/assets/images/ver2/ft-bg.jpg" alt="Footer Background">
            </div>
            <div class="container">
                <div class="ft-box">
                    <div class="ft-logo">
                        <a href="<?php echo home_url(); ?>">
                            <?php echo wp_get_attachment_image($mona_home_footer['logo'], 'full'); ?>
                        </a>
                    </div>

                    <?php if (!empty($mona_home_footer['repeater'])) : ?>
                        <div class="social">
                            <div class="social-list">
                                <?php foreach ($mona_home_footer['repeater'] as $value) : ?>
                                    <a href="<?php echo esc_url($value['link']); ?>" target="_blank" class="social-link">
                                        <?php echo wp_get_attachment_image($value['image'], 'full'); ?>
                                    </a>
                                <?php endforeach; ?>
                            </div>
                        </div>
                    <?php endif; ?>

                    <div class="ft-flex row">
                        <div class="ft-it col">
                            <div class="wrapper">
                                <p class="tt"><?php echo esc_html($mona_home_footer['title']); ?></p>
                                <div class="des"><?php echo wp_kses_post($mona_home_footer['content']); ?></div>
                            </div>
                        </div>

                        <div class="ft-it col">
                            <div class="wrapper">
                                <p class="tt"><?php echo esc_html($mona_home_footer['title_2']); ?></p>
                                <?php if (!empty($mona_home_footer['repeater_2'])) : ?>
                                    <div class="lines">
                                        <?php foreach ($mona_home_footer['repeater_2'] as $value) : ?>
                                            <a href="<?php echo esc_url($value['link']); ?>" class="line">
                                                <?php echo esc_html($value['content']); ?>
                                            </a>
                                        <?php endforeach; ?>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <?php 
                        /**
                         * LOGIC QUAN TRỌNG: Chỉ hiển thị khi có Menu ID được gán thực tế
                         */
                        $actual_locations = get_nav_menu_locations();
                        $target_locs = ['footer-menu', 'footer-menu-2'];

                        foreach ($target_locs as $loc) :
                            // Kiểm tra: Phải có ID gán cho location này và ID đó phải khác 0
                            if ( isset($actual_locations[$loc]) && $actual_locations[$loc] > 0 ) :
                                $menu_obj = wp_get_nav_menu_object($actual_locations[$loc]);
                                
                                // Nếu menu tồn tại thực tế trong hệ thống
                                if ($menu_obj && !is_wp_error($menu_obj)) :
                        ?>
                                    <div class="ft-it col">
                                        <div class="wrapper">
                                            <p class="tt"><?php echo esc_html($menu_obj->name); ?></p>
                                            <?php
                                            wp_nav_menu([
                                                'container'      => false,
                                                'menu_class'     => 'menu-list',
                                                'theme_location' => $loc,
                                                'fallback_cb'    => false, // TUYỆT ĐỐI KHÔNG TỰ HIỆN MENU KHÁC
                                                'walker'         => new Mona_Custom2_Walker_Nav_Menu,
                                            ]);
                                            ?>
                                        </div>
                                    </div>
                        <?php 
                                endif;
                            endif;
                        endforeach; 
                        ?>
                    </div>
                </div>
            </div>
        </div>
    </section>
<?php endif; ?>

<?php 
/**
 * Tối ưu nạp Scripts
 */
$scripts = [
    'jquery/jquery.js',
    'swiper/swiper-bundle.min.js',
    'aos/aos.js',
    'select2/select2.min.js',
    'jquery/jquery-migrate.js',
    'smoothscroll/SmoothScroll.min.js',
    'fancybox/fancybox.umd.js',
    'gsap/gsap.min.js',
    'gsap/ScrollTrigger.min.js',
    'fullpage/fullpage.min.js',
];
$js_path = get_site_url() . '/template-v2/js/libs/home-ver2-lib/';
foreach ($scripts as $script) {
    echo '<script src="' . $js_path . $script . '"></script>' . "\n";
}
?>
<script src="<?php echo get_site_url(); ?>/template-v2/js/home-ver2.js" type="module"></script>
<?php wp_footer(); ?>
</body>
</html>