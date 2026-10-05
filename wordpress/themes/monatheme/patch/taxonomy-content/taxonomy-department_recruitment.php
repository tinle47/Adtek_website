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

    <section class="section recruitment news about no-border">
        <div class="container">
            <?php 
                if( have_posts() ){
                    
            ?>
            <div class="recruitment-list news-list" data-aos="fade-up">
                <?php 
                    while (have_posts()) {
                        the_post();
                ?>

                <?php 
                    /*
                    ** GET
                    ** TEMPLATE PART
                    ** Box Recruitment
                    */
                    $slug_part = 'patch/loop/box';
                    $name_part = 'recruitment';
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
                <p><?php echo __( 'Content is being update', 'monamedia' ) ?></p>
            </div>

            <?php
            } wp_reset_query(); ?>
        </div>
    </section>
</main>