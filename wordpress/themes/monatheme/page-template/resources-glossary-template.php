<?php
/**
 * Template name: Resources Glossary Page
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
        $category_glossary = get_terms(array(
            'taxonomy'      =>'category_glossary',
            // 'order'         => 'ASC',
            'hide_empty'    => true
        ));
    ?>
    <section class="section resources-glossary" data-aos="fade-up">
        <div class="container">
            <?php adtek_page_heading( get_the_title() ); ?>
            <div class="resources-glossary-ctn">
                <div class="glossary-alpha">
                    <?php 
                    $first = true;
                    foreach ($category_glossary as $key => $category_glossary_obj) {
                        $post_per_page = -1;
                        $args = array(
                            'post_type' => 'mona_glossary',
                            'post_status' => 'publish',
                            'posts_per_page' => $post_per_page,
                            'orderby'=> 'title',
                            // 'starts_with' => $letter,
                            'order'   => 'ASC',
                            'meta_query' => [
                                'relation' => 'AND',
                            ],
                            'tax_query' => [
                                'relation'=>'AND',
                                array (
                                    'taxonomy' => $category_glossary_obj->taxonomy,
                                    'field' => 'id',
                                    'terms' => $category_glossary_obj->term_id,
                                )
                            ]
                        );
              
                        $loop = new WP_Query($args);
                        if( $loop->have_posts() ){
                    ?>
                    <div class="glossary-alpha-item <?php echo $first?'current':''; ?>"
                        data-value="<?php echo strtoupper($category_glossary_obj->name); ?>">
                        <?php echo strtoupper($category_glossary_obj->name); ?>
                    </div>
                    <?php 
                        $first = false;
                    }  }?>
                </div>

                <div class="glossary-box">
                    <?php 
                    $first = true;
                    foreach ($category_glossary as $key => $category_glossary_obj) {
                        $post_per_page = -1;
                        $args = array(
                            'post_type' => 'mona_glossary',
                            'post_status' => 'publish',
                            'posts_per_page' => $post_per_page,
                            'orderby'=> 'title',
                            // 'starts_with' => $letter,
                            'order'   => 'ASC',
                            'meta_query' => [
                                'relation' => 'AND',
                            ],
                            'tax_query' => [
                                'relation'=>'AND',
                                array (
                                    'taxonomy' => $category_glossary_obj->taxonomy,
                                    'field' => 'id',
                                    'terms' => $category_glossary_obj->term_id,
                                )
                            ]
                        );
              
                        $loop = new WP_Query($args);
                        if( $loop->have_posts() ){
                    ?>
                    <div class="glossary-wrap <?php echo $first?'current':''; ?>"
                        data-value="<?php echo strtoupper($category_glossary_obj->name); ?>">
                        <div class="glossary-tt"><?php echo strtoupper($category_glossary_obj->name); ?></div>
                        <ul class="glossary-list">
                            <?php 
                                while ($loop->have_posts()) {
                                    $loop->the_post();
                            ?>
                            <li class="glossary-item">
                                <a href="<?php echo get_the_permalink(); ?>">
                                    <?php echo get_the_title(); ?>
                                </a>
                            </li>
                            <?php }
                            ?>
                        </ul>
                    </div>
                    <?php 
                            $first = false;
                        }
                    } ?>
                </div>
            </div>
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

</main>

<?php
endwhile;
get_footer();
?>