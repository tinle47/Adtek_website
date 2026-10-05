<div class="move-to-top moveToTop">
    <div class="pyramid"></div>
    <div class="pyramid"></div>
    <div class="pyramid"></div>
</div>

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