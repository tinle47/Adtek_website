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
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport"
        content="initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no, width=device-width">
    <?php wp_site_icon(); ?>
    <link rel="pingback" href="<?php bloginfo('pingback_url'); ?>" />
    <link rel="stylesheet" href="<?php echo get_site_url() ?>/template/css/style.css" />
    <link rel="stylesheet" href="<?php echo get_site_url() ?>/template/css/backdoor.css" />
    <link rel="stylesheet" href="<?php echo get_site_url() ?>/template-v2/css/home-ver2.css">
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
        <div class="container">
            <div class="hd-wr">
                <div class="hd-flex">
                    <div class="hd-left">
                        <div class="hd-logo">
                            <?php echo get_custom_logo(); ?>
                        </div>
                        <!-- <div class="hd-lg">
                            <div class="hd-lg-item"> <img src="<?php echo get_site_url() ?>/template-v2/assets/images/ver2/ic-vn.svg" alt="" /><span
                                    class="txt">VIE</span><span class="ic"><i class="fas fa-chevron-down"></i></span>
                            </div>
                            <div class="hd-lg-drop">
                                <a class="hd-lg-item" href="">
                                    <img src="<?php echo get_site_url() ?>/template-v2/assets/images/ver2/ic-en.svg" alt="" />
                                    <span class="txt">ENG</span>
                                </a>
                            </div>
                        </div> -->
                        <div class="hd-lg">
    <div class="hd-lg-item">
        <?php 
        $langs = icl_get_languages('skip_missing=N&orderby=KEY&order=DIR&link_empty_to=str'); 
        if (is_array($langs)) {
            foreach ($langs as $item) {
                if ($item['active'] == 1) {
                    echo '<img src="' . $item['country_flag_url'] . '" alt="' . $item['native_name'] . '" />';
                    echo '<span class="txt">' . strtoupper($item['language_code']) . '</span>';
                }
            }
        }
        ?>
        <span class="ic"><i class="fas fa-chevron-down"></i></span>
    </div>
    <div class="hd-lg-drop">
        <?php 
        if (is_array($langs)) {
            foreach ($langs as $item) {
                if ($item['active'] != 1) {
                    echo '<a class="hd-lg-item" href="' . $item['url'] . '">';
                    echo '<img src="' . $item['country_flag_url'] . '" alt="' . $item['native_name'] . '" />';
                    echo '<span class="txt">' . strtoupper($item['language_code']) . '</span>';
                    echo '</a>';
                }
            }
        }
        ?>
    </div>
</div>



                        <a href="tel:<?php echo $information_phone; ?>" class="hd-contact">
                            <img src="<?php echo get_site_url() ?>/template-v2/assets/images/ver2/ic-phone.svg" alt="">
                            <span class="txt">
                                <?php echo  $information_phone  ?>
                            </span>
                        </a>

                    </div>

                    <div class="hd-nav">
                        <div class="menu-nav">
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
                                'walker' => new Mona_Custom2_Walker_Nav_Menu,
                            ));
                            ?>
                        </div>
                    </div>
                    <div class="hd-act">
                        <div class="burger">
                            <div class="hamburger" id="hamburger">
                                <svg class="ham" viewbox="0 0 100 100" width="40">
                                    <path class="line top"
                                        d="m 30,33 h 40 c 0,0 9.044436,-0.654587 9.044436,-8.508902 0,-7.854315 -8.024349,-11.958003 -14.89975,-10.85914 -6.875401,1.098863 -13.637059,4.171617 -13.637059,16.368042 v 40">
                                    </path>
                                    <path class="line middle" d="m 30,50 h 40"></path>
                                    <path class="line bottom"
                                        d="m 30,67 h 40 c 12.796276,0 15.357889,-11.717785 15.357889,-26.851538 0,-15.133752 -4.786586,-27.274118 -16.667516,-27.274118 -11.88093,0 -18.499247,6.994427 -18.435284,17.125656 l 0.252538,40">
                                    </path>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="mobile-overlay"></div>
        <div class="mobile">
            <div class="mobile-con">
                <div class="mobile-wr">
                    <div class="mobile-nav">
                        <div class="menu-nav">
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
                                'walker' => new Mona_Custom2_Walker_Nav_Menu,
                            ));
                            ?>
                        </div>
                        <?php $mona_home_footer = get_field('mona_home_footer', get_option('page_on_front', true));
                        if (!empty($mona_home_footer['repeater'])) { ?>
                            <div class="mobile-content">
                                <div class="social">
                                    <div class="social-list">
                                        <?php foreach ($mona_home_footer['repeater'] as $key => $value) { ?>
                                            <a href="<?php echo $value['link']; ?>" target="_blank" class="social-link">
                                                <?php echo wp_get_attachment_image($value['image'], 'full'); ?>
                                            </a>
                                        <?php } ?>

                                    </div>
                                </div>
                            </div>
                        <?php } ?>
                    </div>
                </div>
            </div>
        </div>
    </header>