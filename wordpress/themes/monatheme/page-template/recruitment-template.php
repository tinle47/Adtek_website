<?php
/**
 * Template name: Recruitment Page
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

    <section class="section recruitment news about no-border">
        <div class="container">
            <?php adtek_page_heading( get_the_title() ); ?>
            <div class="filter-form" data-aos="fade-down">
                <form action="<?php echo get_the_permalink(); ?>" id="filterRecruitment" class="is-loading-group2">
                    <div class="f-r">
                        <div class="f-c">
                            <input type="hidden" id="slug_city_action" name="slug_city_action"
                                value="<?php echo @$_GET['city_recruitment']; ?>">
                            <?php
                                $city_recruitment = get_terms(
                                    array(
                                        'taxonomy' => 'city_recruitment',
                                        'parent' => 0,
                                        'hide_empty' => true,
                                    )
                                );
                            ?>
                            <select class="select2 form-control" name="country_recruitment" id="country_recruitment">
                                <option selected="true" disabled="disabled">
                                    <?php echo __('Select Country','monamedia'); ?></option>
                                <?php
                                    if( !empty($city_recruitment) ){
                                        foreach ($city_recruitment as $key => $city_recruitment_item) { ?>
                                <option value="<?php echo $city_recruitment_item->slug; ?>"
                                    <?php echo mona_selected(@$_GET['country_recruitment'], $city_recruitment_item->slug);  ?>>
                                    <?php echo $city_recruitment_item->name; ?>
                                </option>
                                <?php
                                    }   }
                                ?>
                            </select>
                        </div>
                        <div class="f-c">
                            <select class="select2 form-control" name="city_recruitment" id="city_recruitment">
                                <option selected="true" disabled="disabled"><?php echo __('Select City','monamedia'); ?>
                                </option>
                            </select>
                        </div>
                        <?php
                            $department_recruitment = get_terms(
                                array(
                                    'taxonomy' => 'department_recruitment',
                                    'hide_empty' => true,
                                )
                            );
                        ?>
                        <div class="f-c">
                            <select class="select2 form-control" name="department_recruitment"
                                id="department_recruitment">
                                <option selected="true" disabled="disabled">
                                    <?php echo __('Select Department','monamedia'); ?></option>
                                <?php
                                    if( !empty($department_recruitment) ){
                                        foreach ($department_recruitment as $key => $department_recruitment_item) { ?>
                                <option value="<?php echo $department_recruitment_item->slug; ?>"
                                    <?php echo mona_selected(@$_GET['department_recruitment'], $department_recruitment_item->slug);  ?>>
                                    <?php echo $department_recruitment_item->name; ?>
                                </option>
                                <?php
                                    } }
                                ?>
                            </select>
                        </div>

                        <?php
                            $level_recruitment = get_terms(
                                array(
                                    'taxonomy' => 'level_recruitment',
                                    'hide_empty' => true,
                                )
                            );
                        ?>
                        <div class="f-c">
                            <select class="select2 form-control" id="level_recruitment" name="level_recruitment">
                                <option selected="true" disabled="disabled">
                                    <?php echo __('Select Level','monamedia'); ?></option>
                                <?php
                                if( !empty($level_recruitment) ){
                                    foreach ($level_recruitment as $key => $level_recruitment_item) { ?>
                                <option value="<?php echo $level_recruitment_item->slug; ?>"
                                    <?php echo mona_selected(@$_GET['level_recruitment'], $level_recruitment_item->slug);  ?>>
                                    <?php echo $level_recruitment_item->name; ?>
                                </option>
                                <?php
                                    }   }
                                ?>
                            </select>
                        </div>
                        <div class="f-c">
                            <button type="submit" class="btn">
                                <?php echo __( 'Search', 'monamedia' ) ?>
                                <img src="<?php echo get_site_url() ?>/template/assets/images/search.svg" alt="">
                            </button>
                        </div>
                    </div>
                </form>
            </div>

            <?php
                $post_per_page = 6;
                $paged = max( 1, get_query_var('paged') );
                $offset = ( $paged - 1 ) * $post_per_page;
                $order = 'DESC';
                $args = array(
                    'post_type' => 'mona_recruitment',
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

                if( isset($_GET['country_recruitment']) && $_GET['country_recruitment'] != '' ){
                    $args['tax_query'][] = [
                        'taxonomy' => 'city_recruitment',
                        'field' => 'slug',
                        'terms' => @$_GET['country_recruitment'],
                    ];
                }

                if( isset($_GET['city_recruitment']) && $_GET['city_recruitment'] != '' ){
                    $args['tax_query'][] = [
                        'taxonomy' => 'city_recruitment',
                        'field' => 'slug',
                        'terms' => @$_GET['city_recruitment'],
                    ];
                }

                if( isset($_GET['department_recruitment']) && $_GET['department_recruitment'] != '' ){
                    $args['tax_query'][] = [
                        'taxonomy' => 'department_recruitment',
                        'field' => 'slug',
                        'terms' => @$_GET['department_recruitment'],
                    ];
                }

                if( isset($_GET['level_recruitment']) && $_GET['level_recruitment'] != '' ){
                    $args['tax_query'][] = [
                        'taxonomy' => 'level_recruitment',
                        'field' => 'slug',
                        'terms' => @$_GET['level_recruitment'],
                    ];
                }

                $loop = new WP_Query($args);
                if( $loop->have_posts() ){

            ?>
            <div class="recruitment-list news-list" data-aos="fade-up">
                <?php
                    while ($loop->have_posts()) {
                        $loop->the_post();
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