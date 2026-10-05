<?php
/**
 * Template name: Resources Report Page
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

    <section class="section resources news about no-border" data-aos="fade-up">
        <div class="container">
            <?php 
                $mona_reports = get_field('mona_reports');
                if( !empty($mona_reports) ){
            ?>
            <h2 class="sec-tt resources-tt">
                <?php echo $mona_reports['title']; ?>
            </h2>
            <div class="sec-desc resources-desc">
                <?php echo $mona_reports['description']; ?>
            </div>
            <?php } ?>
            <div class="filter-form">
                <form action="<?php echo get_the_permalink(); ?>">
                    <div class="f-r">
                        <div class="f-c">
                            <?php 
                                $category_reports = get_terms(
                                    array(
                                        'taxonomy' => 'category_reports',
                                        'parent' => 0,
                                        'hide_empty' => true,
                                    )
                                );
                            ?>
                            <select class="select2 form-control" name="category_reports" id="category_reports">
                                <option value="">
                                    <?php echo __('Select Region','monamedia'); ?></option>
                                <?php 
                                    if( !empty($category_reports) ){
                                        foreach ($category_reports as $key => $item) { ?>
                                <option value="<?php echo $item->slug; ?>"
                                    <?php echo mona_selected(@$_GET['category_reports'], $item->slug);  ?>>
                                    <?php echo $item->name; ?>
                                </option>
                                <?php   
                                    }   }
                                ?>
                            </select>
                        </div>
                        <div class="f-c">
                            <?php 
                                $field_reports = get_terms(
                                    array(
                                        'taxonomy' => 'field_reports',
                                        'parent' => 0,
                                        'hide_empty' => true,
                                    )
                                );
                            ?>
                            <select class="select2 form-control" name="field_reports" id="field_reports">
                                <option value="">
                                    <?php echo __('Select Field','monamedia'); ?></option>
                                <?php 
                                    if( !empty($field_reports) ){
                                        foreach ($field_reports as $key => $item) { ?>
                                <option value="<?php echo $item->slug; ?>"
                                    <?php echo mona_selected(@$_GET['field_reports'], $item->slug);  ?>>
                                    <?php echo $item->name; ?>
                                </option>
                                <?php   
                                    }   }
                                ?>
                            </select>
                        </div>
                        <div class="f-c">
                            <?php 
                                $year_reports = get_terms(
                                    array(
                                        'taxonomy' => 'year_reports',
                                        'parent' => 0,
                                        'hide_empty' => true,
                                    )
                                );
                            ?>
                            <select class="select2 form-control" name="year_reports" id="year_reports">
                                <option value="">
                                    <?php echo __('Select Year','monamedia'); ?></option>
                                <?php 
                                    if( !empty($year_reports) ){
                                        foreach ($year_reports as $key => $item) { ?>
                                <option value="<?php echo $item->slug; ?>"
                                    <?php echo mona_selected(@$_GET['year_reports'], $item->slug);  ?>>
                                    <?php echo $item->name; ?>
                                </option>
                                <?php   
                                    }   }
                                ?>
                            </select>
                        </div>
                        <div class="f-c">
                            <button type="submit" class="btn">
                                <?php echo __('Search','monamedia'); ?>
                                <img src="<?php echo get_site_url() ?>/template/assets/images/search.svg" alt="">
                            </button>
                        </div>
                    </div>
                </form>
            </div>
            <?php 
                $post_per_page = 9;
                $paged = max( 1, get_query_var('paged') );
                $offset = ( $paged - 1 ) * $post_per_page;
                $order = 'DESC';
                $args = array(
                    'post_type' => 'mona_reports',
                    'post_status' => 'publish',
                    'posts_per_page' => $post_per_page,
                    'paged' => $paged,
                    'offset' => $offset,
                    'order' => $order,
                    'order' => 'DESC',
                    'meta_query' => [
                        'relation' => 'AND',
                    ],
                    'tax_query' => [
                        'relation'=>'AND',
                    ]
                );

                if( isset($_GET['category_reports']) && $_GET['category_reports'] != '' ){
                    $args['tax_query'][] = [
                        'taxonomy' => 'category_reports',
                        'field' => 'slug',
                        'terms' => @$_GET['category_reports'],
                    ];
                }

                if( isset($_GET['field_reports']) && $_GET['field_reports'] != '' ){
                    $args['tax_query'][] = [
                        'taxonomy' => 'field_reports',
                        'field' => 'slug',
                        'terms' => @$_GET['field_reports'],
                    ];
                }

                if( isset($_GET['year_reports']) && $_GET['year_reports'] != '' ){
                    $args['tax_query'][] = [
                        'taxonomy' => 'year_reports',
                        'field' => 'slug',
                        'terms' => @$_GET['year_reports'],
                    ];
                }
                           
                $loop = new WP_Query($args);
                if( $loop->have_posts() ){
                    
            ?>
            <div class="news-list">
                <?php 
                    while ($loop->have_posts()) {
                        $loop->the_post();
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
                <?php echo mona_page_navi($loop); ?>
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
<?php
endwhile;
get_footer();
?>