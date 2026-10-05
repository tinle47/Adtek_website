<?php
/**
 * Template name: Home Page
 * @author : Hy Hý
 */
get_header();
while (have_posts()):
    the_post();
    ?>
<main class="main">

    <?php
        /*
        ** GET
        ** TEMPLATE PART
        ** Home Section banners
        */
        $slug_part = 'patch/home-content/section';
        $name_part = 'banners';
        get_template_part($slug_part, $name_part);
    ?>

    <?php
        /*
        ** GET
        ** TEMPLATE PART
        ** Home Section banners
        */
        $slug_part = 'patch/home-content/section';
        $name_part = 'partners';
        get_template_part($slug_part, $name_part);
    ?>

    <?php
        /*
        ** GET
        ** TEMPLATE PART
        ** Global Section Description
        */
        $slug_part = 'patch/global-content/section';
        $name_part = 'description';
        get_template_part($slug_part, $name_part);
    ?>

    <?php
        /*
        ** GET
        ** TEMPLATE PART
        ** Global Section Solutions
        */
        $slug_part = 'patch/global-content/section';
        $name_part = 'solutions';
        get_template_part($slug_part, $name_part);
    ?>

    <?php
        /*
        ** GET
        ** TEMPLATE PART
        ** Home Section Latest-Video
        */
        $slug_part = 'patch/home-content/section';
        $name_part = 'latest-video';
        get_template_part($slug_part, $name_part);
    ?>

    <?php
        /*
        ** GET
        ** TEMPLATE PART
        ** Home Section Case Study
        */
        $slug_part = 'patch/home-content/section';
        $name_part = 'case-study';
        get_template_part($slug_part, $name_part);
    ?>

    <?php
        /*
        ** GET
        ** TEMPLATE PART
        ** Home Section Feedbacks
        */
        $slug_part = 'patch/home-content/section';
        $name_part = 'feedbacks';
        get_template_part($slug_part, $name_part);
    ?>

    <?php
        /*
        ** GET
        ** TEMPLATE PART
        ** global Section Leadership Team
        */
        $slug_part = 'patch/global-content/section';
        $name_part = 'leadership-team';
        get_template_part($slug_part, $name_part);
    ?>

    <?php
        /*
        ** GET
        ** TEMPLATE PART
        ** global Section News
        */
        $slug_part = 'patch/global-content/section';
        $name_part = 'news';
        get_template_part($slug_part, $name_part);
    ?>

    <?php
        /*
        ** GET
        ** TEMPLATE PART
        ** global Section Contact
        */
        $slug_part = 'patch/global-content/section';
        $name_part = 'contact';
        get_template_part($slug_part, $name_part);
    ?>

</main>
<?php
endwhile;
get_footer();
?>
