<?php

/**
 * Template name: Order Home Page
 * @author : Hy Hý
 */
get_header();
while (have_posts()) :
    the_post();
?>
    <main class="main">
        <?php
        get_template_part('patch/home-order/banner');
        get_template_part('patch/home-order/intro');
        get_template_part('patch/home-order/noti');
        get_template_part('patch/home-order/market');
        get_template_part('patch/home-order/brand');
        get_template_part('patch/home-order/client');
        get_template_part('patch/home-order/blog');
        get_template_part('patch/home-order/review');
        get_template_part('patch/home-order/form');
        ?>
    </main>
<?php
endwhile;
get_footer();
?>