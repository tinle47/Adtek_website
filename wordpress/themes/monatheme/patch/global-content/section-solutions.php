<?php 
    $mona_solutions = get_field('mona_solutions');
    $mona_solution_background = get_field('mona_solution_background');
    if( empty($mona_solution_background) ){
        $classBg = ' no-bg';
    }else{
        $classBg = '';
    }
    if( !empty($mona_solutions) ){
?>
<section class="section solution mona_solutions_section<?php echo $classBg; ?>">
    <div class="container">
        <div class="solution-list">
            <?php 
                foreach ($mona_solutions as $key => $solution_id) {
                    $title                      = get_field('title_solution', $solution_id);
                    if( empty($title) ){
                        $title                  = get_the_title( $solution_id );
                    }
                    $description                = get_field('description_solution', $solution_id);
                    $img                        = get_the_post_thumbnail( $solution_id , '570x345' );
                    $list_solution_attribute    = get_field('list_solution_attribute', $solution_id);
                    $contactform_shortcode__solution    = get_field('contactform_shortcode__solution', $solution_id);
                    $id_contactform = sanitize_title($title);
            ?>
            <div class="solution-item" data-aos="fade-up">
                <div class="solution-img">
                    <?php echo $img; ?>
                </div>
                <div class="solution-text">
                    <h2 class="sec-tt">
                        <?php echo $title; ?>
                    </h2>
                    <div class="sec-desc solution-desc mona-content">
                        <?php echo $description; ?>
                    </div>
                    <?php if( !empty($list_solution_attribute) ){ ?>
                    <ul class="solution-attr">
                        <?php foreach ($list_solution_attribute as $key_list_solution_attribute => $list_solution_attribute_item) { ?>
                        <li class="solution-attr-item">
                            <?php echo $list_solution_attribute_item['solution_attribute_detail'] ?>
                        </li>
                        <?php
                            } ?>
                    </ul>
                    <?php } ?>
                    <div class="solution-btn">
                        <a href="<?php echo get_the_permalink( $solution_id ) ?>" class="btn">
                            <?php echo __('Explore','monamedia'); ?>
                            <img src="<?php echo get_site_url() ?>/template/assets/images/btn-arrow.svg" alt="">
                        </a>
                    </div>
                </div>
            </div>
            <?php } ?>
        </div>
    </div>
</section>
<?php } ?>