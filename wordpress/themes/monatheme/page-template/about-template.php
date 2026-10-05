<?php
/**
 * Template name: About Us Page
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
        ** Breadcrumb
        */
        $slug_part = 'patch/breadcrumb';
        $name_part = '';
        get_template_part($slug_part, $name_part);
    ?>

    <?php 
        /*
        ** GET
        ** TEMPLATE PART
        ** About Section Banners
        */
        $slug_part = 'patch/about-content/section';
        $name_part = 'banners';
        get_template_part($slug_part, $name_part);
    ?>

    <?php 
        /*
        ** GET
        ** TEMPLATE PART
        ** global Section Description
        */
        $slug_part = 'patch/global-content/section';
        $name_part = 'description';
        get_template_part($slug_part, $name_part);
    ?>

    <?php 
        /*
        ** GET
        ** TEMPLATE PART
        ** About Section Protect
        */
        $slug_part = 'patch/about-content/section';
        $name_part = 'protect';
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
        ** About Section Awards
        */
        $slug_part = 'patch/about-content/section';
        $name_part = 'awards';
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
    ** About Section Platform
    */
    $slug_part = 'patch/about-content/section';
    $name_part = 'platform';
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