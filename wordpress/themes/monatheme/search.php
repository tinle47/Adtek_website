<?php
get_header();
?>

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

<section class="section resources news about no-border" data-aos="fade-up">
    <div class="container">

        <h2 class="sec-tt resources-tt">
            <?php echo __('Results: ') . get_search_query('s'); ?>
        </h2>

        <?php if( have_posts() ){?>
        <div class="news-list">
            <?php 
                while (have_posts()) {
                    the_post();
            ?>

            <?php 
                /*
                ** GET
                ** TEMPLATE PART
                ** Box Report
                */
                $slug_part = 'patch/loop/box';
                $name_part = 'report';
                get_template_part($slug_part, $name_part);
            ?>

            <?php }
                ?>
        </div>
        <nav class="pagination" data-aos="fade-up">
            <?php echo mona_page_navi(); ?>
        </nav>
        <?php }else{ ?>

        <div class="mona-mess-empty">
            <p><?php echo __( 'No matching results were found', 'monamedia' )  ?></p>
        </div>

        <?php } 
        wp_reset_query(); ?>
    </div>
</section>

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

<?php get_footer(); ?>