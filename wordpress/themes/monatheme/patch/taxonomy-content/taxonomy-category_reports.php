<?php 
$obz = get_queried_object(); 
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

    <section class="section resources news about no-border" data-aos="fade-up">
        <div class="container">

            <h2 class="sec-tt resources-tt">
                <?php echo $obz->name; ?>
            </h2>
            <div class="sec-desc resources-desc">
                <?php echo $obz->description; ?>
            </div>


            <?php 
                
                if( have_posts() ){
                    
            ?>
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
                <p><?php echo __( 'Content is being update', 'monamedia' ) ?></p>
            </div>

            <?php
            } wp_reset_query(); ?>
        </div>
    </section>

    <?php 
        /*
        ** GET
        ** TEMPLATE PART
        ** global Section Stay in touch
        */
        $slug_part = 'patch/global-content/section';
        $name_part = 'stay-in-touch';
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