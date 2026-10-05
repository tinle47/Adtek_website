<?php get_header(); ?>
<main class="main">
	 <div class="breadcrumb solution-path" data-aos="fade-right">
		 <div class="container">
			 <div class="breadcrumb-wrap">
				 <ul class="breadcrumb-list">
					 <li class="breadcrumb-item">
						 <a href="<?php echo home_url() ?>"><?php echo mona_get_home_title() ?></a>
					 </li>
					 <li class="breadcrumb-item">
						 <a href="<?php echo get_the_permalink( MONA_PAGE_SOLUTIONS ) ?>">
							 <?php echo get_the_title( MONA_PAGE_SOLUTIONS ) ?>
						 </a>
					 </li>
					 <li class="breadcrumb-item">
						 <a href="javascript:;"><?php the_title() ?></a>
					 </li>
				 </ul>
			 </div>
		 </div>
	</div>
    <?php 
    $solution_slider_items = get_field('mona_solution_slider_items');
    if ( is_array ( $solution_slider_items ) ) {
    ?>
    <section class="banner solution1">
        <div class="swiper-container">
            <div class="swiper-wrapper">
                <?php foreach ( $solution_slider_items as $key => $banner ) { ?>
                <div class="swiper-slide banner-item">
                    <div class="banner-img">
                        <?php 
                        if ( wp_is_mobile() ) {
                            echo wp_get_attachment_image( $banner['image_mobile'], '400x675' );
                        } else {
                            echo wp_get_attachment_image( $banner['image_mobile'], '1920x790' );
                        }
                        ?>
                    </div>
                    <div class="banner-text">
                        <div class="container">
                            <div class="banner-text-wrap">
                                <?php $adtek_tag = $key === array_key_first( $solution_slider_items ) ? 'h1' : 'h2'; ?>
                                <<?php echo $adtek_tag; ?> class="banner-tt"><?php echo $banner['slider_title'] ?></<?php echo $adtek_tag; ?>>
                                <div class="banner-desc">
                                    <?php echo $banner['image_desc'] ?>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <?php } ?>
            </div>
        </div>
    </section>
    <?php } else { ?>
    <div class="container"><?php adtek_page_heading( get_the_title() ); ?></div>
    <?php } ?>
    <?php 
    $solution_abous = get_field('mona_solution_abous');
    if ( ! empty ( $abouts = $solution_abous ) ) {
    ?>
    <section class="social_media">
        <div class="container">
            <div class="social_wrap">
                <div class="sm_gr image-sm" data-aos="fade-right">
                    <?php echo wp_get_attachment_image( $abouts['about_image'], '570x345' ) ?>
                </div>
                <div class="sm_gr text-sm mona-content">
                    <?php echo $abouts['about_desc'] ?>
					<?php 
					$shortcode__solution = get_field('contactform_shortcode__solution');
					if ( ! empty ( $shortcode__solution ) ) { 
						$i_cf = sanitize_title( get_the_title() );
					?>
					<div class="about-ct-button">
						<a data-solution_title="<?php the_title() ?>" data-solution_id_cf="<?php echo $i_cf ?>" data-aos="fade-up" href="#<?php echo $i_cf ?>" class="contact-sm popup-with-zoom-anim">
							<?php echo __( 'Contact consultant', 'monamedia' ) ?>
						</a>
					</div>
					<div id="<?php echo $i_cf ?>" class="solution-popup zoom-anim-dialog mfp-hide">
                        <div class="lets-talk-form">
                            <div class="form">
                                <?php echo do_shortcode( $shortcode__solution ); ?>
                            </div>
                        </div>
                    </div>
					<?php } ?>
                </div>
            </div>
        </div>
    </section>
    <?php } ?>
    <?php 
    $solution_targets = get_field('mona_solution_targets');
    if ( ! empty ( $targets = $solution_targets ) ) {
    ?>
    <section class="target">
        <div class="container">
            <div class="title" data-aos="fade-right">
                <h3><?php echo $targets['target_title'] ?></h3>
            </div>
            <div class="target_wrap">
                <div class="target_gr">
                    <?php 
                    $target_items = $targets['target_items'];
                    if ( ! empty ( $target_items ) ) {
                        foreach ( $target_items as $key => $target ) {
                    ?>
                    <div class="item" data-aos="flip-up" data-aos-duration="<?php echo ( ( $key + 1 ) * 100 ) ?>">
                        <div class="mb_inlibe">
                            <?php echo wp_get_attachment_image( $target['target_item_icon'], '32x32' ) ?>
                            <h5>
                                <?php echo $target['target_item_title'] ?>
                            </h5>
                        </div>
                        <p><?php echo $target['target_item_desc'] ?></p>
                    </div>
                    <?php }} ?>
                </div>
                <div class="target_img" data-aos="zoom-in">
                    <?php echo wp_get_attachment_image( $targets['target_image'], '600x600' ) ?>
                </div>
            </div>
        </div>
    </section>
    <?php } ?>
    <?php 
    $args_posts = [
        'post_type' => 'mona_case_study',
        'post_status' => 'publish',
        'posts_per_page' => 12,
		'order' => 'DESC',
    ];
    $query_posts = new WP_Query( $args_posts );
    if ( $query_posts->have_posts() ) {
    ?>
    <section class="case_study" data-aos="fade-up" data-aos-duration="900">
        <div class="container">
            <div class="title">
                <h3>
                    <?php echo __( 'Case Study', 'monamedia' ) ?>
                </h3>
            </div>
            <div class="swiper-case">
                <div class="swiper-wrapper">
                    <?php 
                    while ( $query_posts->have_posts() ) {
                        $query_posts->the_post();
                    ?>
                    <div class="swiper-slide">
                        <div class="image">
                            <?php the_post_thumbnail( '370x250' ) ?>
                        </div>
                        <div class="info">
                            <div class="date">
                                <span class="icon">
                                    <svg width="10" height="10" viewBox="0 0 10 10" fill="none"
                                        xmlns="http://www.w3.org/2000/svg">
                                        <g clip-path="url(#clip0_326_943)">
                                            <path
                                                d="M8.06932 0.770321H7.69632V0.392892C7.69632 0.177246 7.52151 0.00244141 7.30587 0.00244141C7.09022 0.00244141 6.91542 0.177246 6.91542 0.392892V0.770321H3.08456V0.392892C3.08456 0.177246 2.90976 0.00244141 2.69411 0.00244141C2.47847 0.00244141 2.30366 0.177246 2.30366 0.392892V0.770321H1.93068C0.866099 0.770321 0 1.63642 0 2.70098V8.0673C0 9.13188 0.866099 9.99798 1.93068 9.99798H8.06934C9.1339 9.99798 10 9.13188 10 8.0673V2.70098C10 1.63642 9.1339 0.770321 8.06932 0.770321ZM1.93068 1.55122H2.30366V2.3126C2.30366 2.52825 2.47847 2.70305 2.69411 2.70305C2.90976 2.70305 3.08456 2.52825 3.08456 2.3126V1.55122H6.91544V2.3126C6.91544 2.52825 7.09024 2.70305 7.30589 2.70305C7.52153 2.70305 7.69634 2.52825 7.69634 2.3126V1.55122H8.06934C8.70331 1.55122 9.2191 2.06701 9.2191 2.70098V3.07398H0.780902V2.70098C0.780902 2.06701 1.29669 1.55122 1.93068 1.55122ZM8.06932 9.21708H1.93068C1.29669 9.21708 0.780902 8.70129 0.780902 8.0673V3.85488H9.2191V8.0673C9.2191 8.70129 8.70331 9.21708 8.06932 9.21708ZM3.46851 5.39066C3.46851 5.60631 3.29371 5.78111 3.07806 5.78111H2.31018C2.09454 5.78111 1.91973 5.60631 1.91973 5.39066C1.91973 5.17502 2.09454 5.00021 2.31018 5.00021H3.07806C3.29369 5.00021 3.46851 5.17502 3.46851 5.39066ZM8.08029 5.39066C8.08029 5.60631 7.90548 5.78111 7.68984 5.78111H6.92196C6.70631 5.78111 6.53151 5.60631 6.53151 5.39066C6.53151 5.17502 6.70631 5.00021 6.92196 5.00021H7.68984C7.90546 5.00021 8.08029 5.17502 8.08029 5.39066ZM5.77218 5.39066C5.77218 5.60631 5.59737 5.78111 5.38172 5.78111H4.61384C4.3982 5.78111 4.22339 5.60631 4.22339 5.39066C4.22339 5.17502 4.3982 5.00021 4.61384 5.00021H5.38172C5.59735 5.00021 5.77218 5.17502 5.77218 5.39066ZM3.46851 7.69432C3.46851 7.90997 3.29371 8.08477 3.07806 8.08477H2.31018C2.09454 8.08477 1.91973 7.90997 1.91973 7.69432C1.91973 7.47868 2.09454 7.30387 2.31018 7.30387H3.07806C3.29369 7.30387 3.46851 7.47868 3.46851 7.69432ZM8.08029 7.69432C8.08029 7.90997 7.90548 8.08477 7.68984 8.08477H6.92196C6.70631 8.08477 6.53151 7.90997 6.53151 7.69432C6.53151 7.47868 6.70631 7.30387 6.92196 7.30387H7.68984C7.90546 7.30387 8.08029 7.47868 8.08029 7.69432ZM5.77218 7.69432C5.77218 7.90997 5.59737 8.08477 5.38172 8.08477H4.61384C4.3982 8.08477 4.22339 7.90997 4.22339 7.69432C4.22339 7.47868 4.3982 7.30387 4.61384 7.30387H5.38172C5.59735 7.30387 5.77218 7.47868 5.77218 7.69432Z"
                                                fill="black" />
                                        </g>
                                        <defs>
                                            <clipPath id="clip0_326_943">
                                                <rect width="10" height="10" fill="white" />
                                            </clipPath>
                                        </defs>
                                    </svg>
                                </span>
                                <span class="text">
                                    <?php echo get_the_date() ?>
                                </span>
                            </div>
                            <div class="title">
                                <h5><?php the_title() ?></h5>
                            </div>
                            <div class="text mona-content">
                                <?php the_excerpt() ?>
                            </div>
                        </div>
                    </div>
                    <?php 
                    wp_reset_query();
                    } ?>
                </div>
                <!-- Add Arrows -->
            </div>
            <div class="case-btn case-button-prev">
                <svg width="7" height="9" viewBox="0 0 7 9" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                        d="M5.66577 0.106597C5.79564 0.10374 5.92318 0.14139 6.03066 0.214369C6.13813 0.287349 6.22019 0.392051 6.26544 0.513826C6.31068 0.635601 6.31686 0.768429 6.28312 0.893878C6.24937 1.01933 6.17738 1.13109 6.07714 1.21374L2.25268 4.4901L6.07714 7.76531C6.14648 7.81627 6.20455 7.88096 6.24771 7.9554C6.29087 8.02985 6.3182 8.11242 6.32798 8.19791C6.33776 8.2834 6.32978 8.36998 6.30455 8.45224C6.27932 8.53451 6.23737 8.6107 6.18133 8.676C6.1253 8.74131 6.05638 8.79428 5.97891 8.83172C5.90143 8.86915 5.81705 8.89018 5.73107 8.8935C5.64508 8.89681 5.55934 8.88239 5.47921 8.85104C5.39907 8.81968 5.32628 8.77212 5.26538 8.71133L0.886715 4.96495C0.817953 4.90627 0.762737 4.83343 0.724875 4.75135C0.687014 4.66926 0.667408 4.57992 0.667408 4.48952C0.667408 4.39912 0.687014 4.30978 0.724875 4.22769C0.762737 4.14561 0.817953 4.0727 0.886715 4.01402L5.26538 0.264038C5.37599 0.16579 5.51786 0.109933 5.66577 0.106452V0.106597Z"
                        fill="#193869" />
                </svg>
            </div>
            <div class="case-btn case-button-next">
                <svg width="7" height="9" viewBox="0 0 7 9" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                        d="M1.33423 0.106597C1.20436 0.10374 1.07682 0.14139 0.969343 0.214369C0.861871 0.287349 0.779808 0.392051 0.734562 0.513826C0.689317 0.635601 0.683137 0.768429 0.716883 0.893878C0.750629 1.01933 0.822622 1.13109 0.922856 1.21374L4.74732 4.4901L0.922856 7.76531C0.85352 7.81627 0.795452 7.88096 0.75229 7.9554C0.709128 8.02985 0.681801 8.11242 0.67202 8.19791C0.662239 8.2834 0.670215 8.36997 0.695449 8.45224C0.720683 8.53451 0.762631 8.6107 0.818665 8.676C0.8747 8.74131 0.943615 8.79428 1.02109 8.83172C1.09857 8.86915 1.18295 8.89018 1.26893 8.8935C1.35492 8.89681 1.44066 8.88239 1.52079 8.85104C1.60093 8.81968 1.67372 8.77212 1.73462 8.71133L6.11329 4.96495C6.18205 4.90627 6.23726 4.83343 6.27512 4.75135C6.31299 4.66926 6.33259 4.57992 6.33259 4.48952C6.33259 4.39912 6.31299 4.30978 6.27512 4.22769C6.23726 4.14561 6.18205 4.0727 6.11329 4.01402L1.73462 0.264038C1.62401 0.16579 1.48214 0.109933 1.33423 0.106452V0.106597Z"
                        fill="black" />
                </svg>
            </div>
        </div>
    </section>
    <?php } ?>
    <?php 
    $solution_bottom_infos = get_field('mona_solution_bottom_infos');
    if ( ! empty ( $infos = $solution_bottom_infos ) ) {
    ?>
    <section class="grow">
        <div class="content">
            <div class="grow_item image" data-aos="flip-left">
                <?php echo wp_get_attachment_image( $infos['bottom_info_image'], 'full' ) ?>
            </div>
            <div class="grow_item info">
                <div class="info_wrap mona-content">
                    <?php echo $infos['bottom_info_desc'] ?>
                </div>
            </div>
        </div>
    </section>
    <?php } ?>
    <?php 
    $solution_says = get_field('mona_solution_says');
    if ( ! empty ( $says = $solution_says ) ) {
    ?>
    <section class="section client-say">    
        <div class="container">
            <div class="client-say-ctn">
                <div class="client-say-text">
                    <h2 class="sec-tt client-say-tt" data-aos="fade-down">
                        <?php echo $says['say_title'] ?>
                    </h2>
                    <div class="sec-desc client-say-desc" data-aos="fade-up">
                        <?php echo $says['say_desc'] ?>
                    </div>
                    <div class="client-say-text-bg">
                        <img src="<?php echo get_site_url() ?>/template/assets/images/client-say-bg.svg" alt="">
                    </div>
                </div>
                <?php 
                $say_items = $says['say_items'];
                if ( is_array ( $say_items ) ) {
                ?>
                <div class="client-say-content">
                    <div class="client-say-content-wrap">
                        <div class="swiper-container">
                            <div class="swiper-wrapper">
                                <?php foreach ( $say_items as $key => $say ) { ?>
                                <div class="swiper-slide">
                                    <div class="content-item">
                                        <div class="content-quote">
                                            <img src="<?php echo get_site_url() ?>/template/assets/images/quote.svg"
                                                alt="">
                                        </div>
                                        <div class="content-text">
                                            <div class="desc"><?php echo $say['say_item_desc'] ?></div>
                                            <div class="customer">
                                                <div class="customer-avt">
                                                    <?php echo wp_get_attachment_image( $say['say_item_avatar'], '50x50' ) ?>
                                                </div>
                                                <div class="customer-info">
                                                    <div class="name"><?php echo $say['say_item_name'] ?></div>
                                                    <div class="title"><?php echo $say['say_item_role'] ?></div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <?php } ?>
                            </div>
                        </div>
                    </div>
                    <div class="client-say-navi">
                        <div class="swiper-next">
                            <img src="<?php echo get_site_url() ?>/template/assets/images/navi-arrow.svg" alt="">
                        </div>
                    </div>
                    <div class="swiper-pagination"></div>
                </div>
                <?php } ?>
            </div>
        </div>
    </section>
    <?php } ?>
</main>
<?php get_footer(); ?>