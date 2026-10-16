<div class="move-to-top moveToTop">
    <div class="pyramid"></div>
    <div class="pyramid"></div>
    <div class="pyramid"></div>
</div>

<style>
    /* Nền footer giống trang chủ (Home V2): ảnh chuyển màu navy, tím, cam. Dòng pixel sáng ở mép trên ảnh được phủ bằng viền navy. */
    footer.ft {
        background: #161342 url("<?php echo esc_url(get_site_url() . '/template-v2/assets/images/ver2/ft-bg.jpg'); ?>") center bottom / cover no-repeat;
        box-shadow: inset 0 2px 0 #161342;
    }
    /* Link footer giống trang chủ: trắng mờ 60%, rê chuột hoặc trang đang mở thì sáng 100% (bỏ màu đỏ #DD3535 cũ). */
    footer.ft .ft-menu-item .menu-item a,
    footer.ft .ft-menu-item .widget-contact .menu-item > p {
        color: #fff;
        opacity: 0.6;
        transition: opacity 0.4s;
    }
    footer.ft .ft-menu-item .menu-item a:hover,
    footer.ft .ft-menu-item .current-menu-item > a,
    footer.ft .ft-menu-item .current_page_item > a {
        /* !important để thắng quy tắc .current_page_item > a { color: #dd3535 !important } của theme. */
        color: #fff !important;
        opacity: 1;
    }
</style>
<footer class="ft">
    <div class="container">
        <div class="ft-ctn">
            <div class="ft-info">
                <?php 
                    $information_ft_logo = mona_get_option('information_ft_logo');
                    if( !empty($information_ft_logo) ){
                ?>
                <div class="logo">
                    <a href="<?php echo home_url() ?>">
                        <img src="<?php echo $information_ft_logo; ?>">
                    </a>
                </div>
                <?php } ?>

                <?php 
                    $information_desc = mona_get_option('information_desc');
                    if( !empty($information_desc) ){
                ?>
                <div class=" desc">
                    <?php echo $information_desc; ?>
                </div>
                <?php } ?>

                <?php if (!function_exists('dynamic_sidebar') || !dynamic_sidebar('header_topright')) : ?>
                <?php endif; ?>
            </div>

            <div class="ft-menu">
                <div class="ft-menu-wrap">
                    <div class="ft-menu-item">
                        <?php if (!function_exists('dynamic_sidebar') || !dynamic_sidebar('footer_col_1')) : ?>
                        <?php endif; ?>
                    </div>
                    <div class="ft-menu-item">
                        <?php if (!function_exists('dynamic_sidebar') || !dynamic_sidebar('footer_col_2')) : ?>
                        <?php endif; ?>
                    </div>
                    <div class="ft-menu-item">
                        <?php if (!function_exists('dynamic_sidebar') || !dynamic_sidebar('footer_col_3')) : ?>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        </div>
    </div>
</footer>
<!-- Style -->
<script src="<?php echo get_site_url(); ?>/template/js/libs/jquery/jquery.min.js"></script>
<script src="<?php echo get_site_url(); ?>/template/js/libs/swiper/swiper-bundle.min.js"></script>
<script src="<?php echo get_site_url(); ?>/template/js/libs/lightgallery/lightgallery-all.min.js"></script>
<script src="<?php echo get_site_url(); ?>/template/js/libs/magnific/jquery.magnific-popup.min.js"></script>
<script src="<?php echo get_site_url(); ?>/template/js/libs/aos/aos.js"></script>
<script src="<?php echo get_site_url(); ?>/template/js/libs/select2/select2.min.js"></script>
<script src="<?php echo get_site_url(); ?>/template/js/libs/isotope/isotope.pkgd.min.js"></script>
<script src="<?php echo get_site_url(); ?>/template/js/main.js" type="module" defer></script>
<?php wp_footer(); ?>
</body>
</html>