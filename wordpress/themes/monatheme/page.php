<?php
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
    <section class="section blog">
        <div class="container">
            <?php if ( false === stripos( get_post_field( 'post_content', get_the_ID() ), '<h1' ) ) { adtek_page_heading( get_the_title() ); } ?>
            <div class="blog-ctn">
                <div class="blog-main-default mona-content">
                    <?php the_content(); ?>
                </div>
            </div>
        </div>
    </section>

</main>

<?php
endwhile;
get_footer();
?>