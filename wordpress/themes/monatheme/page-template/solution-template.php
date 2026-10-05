<?php

/**
 * Template name: Solution Page
 * @author : Hy Hý
 */
get_header();
while (have_posts()) :
    the_post();
?>
    <main class="main">
        <?php
        get_template_part('patch/solution/banner');
        get_template_part('patch/solution/intro');
        get_template_part('patch/solution/client');
        get_template_part('patch/solution/form');
        ?>
    </main>
<?php
endwhile;
get_footer();
?>