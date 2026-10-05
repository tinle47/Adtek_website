<?php
get_header();
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


    <section class="section blog">
        <div class="container">
            <?php adtek_page_heading( is_home() ? get_the_title( get_option( 'page_for_posts' ) ) : wp_get_document_title() ); ?>
            <div class="blog-ctn">
                <div class="blog-main">
                    <?php if( have_posts() ){ ?>
                    <div class="blog-list">
                        <?php
                            while (have_posts()) {
                                the_post();
                        ?>
                        <?php 
                            /*
                            ** GET
                            ** TEMPLATE PART
                            ** About Box News
                            */
                            $slug_part = 'patch/loop/box';
                            $name_part = 'news-blog';
                            get_template_part($slug_part, $name_part);
                        ?>
                        <?php } ?>
                    </div>
                    <nav class="pagination" data-aos="fade-up">
                        <?php mona_page_navi(); ?>
                    </nav>
                    <?php } wp_reset_query(); ?>
                </div>
                <div class="blog-aside" data-aos="fade-up">
                    <?php if (!function_exists('dynamic_sidebar') || !dynamic_sidebar('sidebar_post')) : ?><?php endif; ?>
                </div>
            </div>
        </div>
    </section>
</main>
<?php get_footer();