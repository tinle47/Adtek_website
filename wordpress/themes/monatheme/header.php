<?php

/**
 * The Header for our theme
 *
 * Displays all of the <head> section and everything up till <div id="main">
 *
 * @author : monamedia
 */
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<!--[if IE 7]>
<html class="ie ie7" <?php language_attributes(); ?>>
<![endif]-->
<!--[if IE 8]>
<html class="ie ie8" <?php language_attributes(); ?>>
<![endif]-->
<!--[if !(IE 7) & !(IE 8)]><!-->
<html <?php language_attributes(); ?>>
<!--<![endif]-->

<head>
    <!-- Meta
                ================================================== -->
		<!-- Google Tag Manager -->
	<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
	new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
	j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
	'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
	})(window,document,'script','dataLayer','GTM-WDKPXZR');</script>
	<!-- End Google Tag Manager -->
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no, width=device-width">
    <?php wp_site_icon(); ?>
    <link rel="pingback" href="<?php bloginfo('pingback_url'); ?>" />
    <link rel="stylesheet" href="<?php echo get_site_url() ?>/template/css/style.css" />
    <link rel="stylesheet" href="<?php echo get_site_url() ?>/template/css/backdoor.css" />
    <link rel="stylesheet" href="<?php echo get_site_url() ?>/template/css/hu.css" />
    <script src="<?php echo get_site_url() ?>/template/js/libs/jquery/jquery.min.js"></script>
    <?php wp_head(); ?>
</head>
<?php
if (wp_is_mobile()) {
    $body = 'mobile-detect';
} else {
    $body = 'desktop-detect';
}
$information_time   = mona_get_option('information_time');
$information_phone  = mona_get_option('information_phone');
$information_email  = mona_get_option('information_email');
$information_faq    = mona_get_option('information_faq');
?>

<body <?php body_class($body); ?>>
    <header class="hd">
        <div class="hd-top">
            <div class="container">
                <div class="hd-top-ctn">
                    <div class="hd-top-left">
                        <!--<div class="hd-lang">
                            <div class="hd-lang-current">
                                <img src="<?php echo get_site_url() ?>/template/assets/images/lang-en.svg" alt="">
                                English
                                <img src="<?php echo get_site_url() ?>/template/assets/images/lang-dropdown.svg" alt=""
                                    class="dropdown">
                            </div>
                            <ul class="hd-lang-list">
                                <li>
                                    <a href="#">
                                        <img src="<?php echo get_site_url() ?>/template/assets/images/lang-vi.png"
                                            alt="">
                                        Vietnamese
                                    </a>
                                </li>
                                <li>
                                    <a href="#">
                                        <img src="<?php echo get_site_url() ?>/template/assets/images/lang-en.svg"
                                            alt="">
                                        English
                                    </a>
                                </li>
                            </ul>
                        </div>-->
                        <div class="hd-language">
                            <?php
                            $langs = icl_get_languages('skip_missing=N&orderby=KEY&order=DIR&link_empty_to=str');
                            if (is_array($langs)) {
                                foreach ($langs as $item) {
                                    if ($item['active'] == 1) {
                                        echo ' <span><img src="' . $item['country_flag_url'] . '" alt="' . $item['native_name'] . '">' . $item['native_name'] . '</span>';
                                    }
                                }
                            }
                            ?>

                            <ul>
                                <?php
                                if (is_array($langs)) {
                                    foreach ($langs as $item) {
                                        if ($item['active'] != 1) {
                                            echo '<li><a href="' . $item['url'] . '"><img src="' . $item['country_flag_url'] . '" alt="' . $item['native_name'] . '">' . $item['native_name'] . '</a></li>';
                                        }
                                    }
                                }
                                ?>

                            </ul>
                        </div>
                        <?php if (!empty($information_faq)) { ?>
                            <div class="hd-faq">
                                <a href="<?php echo $information_faq; ?>"><?php echo __('FAQ', 'monamedia'); ?></a>
                            </div>
                        <?php } ?>
                        <?php if (!empty($information_phone)) { ?>
                            <div class="hd-contact">
                                <a href="<?php echo mona_replace_tel($information_phone); ?>">
                                    <img src="<?php echo get_site_url() ?>/template/assets/images/phone.svg" alt="">
                                    <?php echo $information_phone; ?>
                                </a>
                            </div>
                        <?php } ?>
                    </div>

                    <div class="hd-top-right">
                        <?php if (!empty($information_time)) { ?>
                            <div class="hd-active">
                                <?php echo $information_time; ?>
                            </div>
                        <?php } ?>

                        <?php if (!function_exists('dynamic_sidebar') || !dynamic_sidebar('header_topright')) : ?>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        </div>

        <div class="hd-bot">
            <div class="container">
                <div class="hd-bot-ctn">
                    <div class="hd-logo">
                        <?php echo get_custom_logo(); ?>
                    </div>

                    <div class="hd-menu">
                        <div class="menu">
                            <div class="menu-wrap">

                                <?php
                                wp_nav_menu(array(
                                    'container' => false,
                                    'container_class' => 'menu-list',
                                    'menu_id' => 'menu-primary-menu',
                                    'menu_class' => 'menu-list',
                                    'theme_location' => 'primary-menu',
                                    'before' => '',
                                    'after' => '',
                                    'link_before' => '',
                                    'link_after' => '',
                                    'fallback_cb' => false,
                                    'walker' => new Mona_Custom_Walker_Nav_Menu,
                                ));
                                ?>

                                <div class="more-info phone">
                                    <?php if (!empty($information_time)) { ?>
                                        <div class="more-info-item">
                                            <i class="far fa-clock icon"></i>
                                            <a href="javascript:;">
                                                <?php echo $information_time; ?>
                                            </a>
                                        </div>
                                    <?php } ?>

                                    <?php if (!empty($information_phone)) { ?>
                                        <div class="more-info-item">
                                            <i class="fas fa-mobile-alt icon"></i>
                                            <a href="<?php echo mona_replace_tel($information_phone); ?>">
                                                <?php echo $information_phone; ?>
                                            </a>
                                        </div>
                                    <?php } ?>

                                    <?php if (!empty($information_email)) { ?>
                                        <div class="more-info-item">
                                            <i class="far fa-envelope icon"></i>
                                            <a href="mailto:<?php echo $information_email; ?>">
                                                <?php echo $information_email; ?>
                                            </a>
                                        </div>
                                    <?php } ?>

                                    <?php if (!empty($information_faq)) { ?>
                                        <div class="more-info-item">
                                            <i class="far fa-question-circle icon"></i>
                                            <a href="<?php echo $information_faq; ?>">
                                                <?php echo __('FAQ', 'monamedia'); ?>
                                            </a>
                                        </div>
                                    <?php } ?>
                                </div>

                                <div class="more-phone">
                                    <?php if (!function_exists('dynamic_sidebar') || !dynamic_sidebar('header_topright')) : ?>
                                    <?php endif; ?>
                                </div>
                            </div>
                        </div>

                        <!--<div class="hd-lang-phone">
                            <div class="hd-lang">
                                <div class="hd-lang-current">
                                    <img src="<?php echo get_site_url() ?>/template/assets/images/lang-en.svg" alt="">
                                    <img src="<?php echo get_site_url() ?>/template/assets/images/lang-dropdown.svg"
                                        alt="" class="dropdown">
                                </div>
                                <ul class="hd-lang-list">
                                    <li>
                                        <a href="#">
                                            <img src="<?php echo get_site_url() ?>/template/assets/images/lang-vi.png">
                                        </a>
                                    </li>
                                    <li>
                                        <a href="#">
                                            <img src="<?php echo get_site_url() ?>/template/assets/images/lang-en.svg">
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </div>-->
                        <div class="hd-language1">
                            <?php
                            $langs = icl_get_languages('skip_missing=N&orderby=KEY&order=DIR&link_empty_to=str');
                            if (is_array($langs)) {
                                foreach ($langs as $item) {
                                    if ($item['active'] == 1) {
                                        echo ' <span><img src="' . $item['country_flag_url'] . '" alt="' . $item['native_name'] . '">' . '</span>';
                                    }
                                }
                            }
                            ?>

                            <ul>
                                <?php
                                if (is_array($langs)) {
                                    foreach ($langs as $item) {
                                        if ($item['active'] != 1) {
                                            echo '<li><a href="' . $item['url'] . '"><img src="' . $item['country_flag_url'] . '" alt="' . $item['native_name'] . '">' . '</a></li>';
                                        }
                                    }
                                }
                                ?>

                            </ul>
                        </div>
                        <div class="hd-search">
                            <div class="hd-search-icon">
                                <img src="<?php echo get_site_url() ?>/template/assets/images/search.svg" alt="">
                            </div>

                            <div class="form-search">
                                <div class="container">
                                    <form class="form" method="get" id="searchform" action="<?php echo esc_url(home_url('/')); ?>">
                                        <div class="f-r">
                                            <?php echo get_custom_logo(); ?>
                                            <div class="f-c">
                                                <input type="search" name="s" value="<?php echo get_search_query('s'); ?>" id="s" placeholder="<?php echo __('Enter search keywords ...', 'monamedia'); ?>">
                                                <button type="submit">
                                                    <img src="<?php echo get_site_url() ?>/template/assets/images/search.svg">
                                                </button>
                                            </div>
                                            <div class="form-close">
                                                <div class="close"></div>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>

                        <div class="bars-wrap">
                            <div class="bars">
                                <span class="bars-line"></span>
                                <span class="bars-line"></span>
                                <span class="bars-line"></span>
                            </div>
                        </div>
                        <div class="hd-bg"></div>
                    </div>
                </div>
            </div>
        </div>
    </header>