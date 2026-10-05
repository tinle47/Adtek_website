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
            <div class="blog-ctn">
                <div class="blog-main">
                    <div class="blog-dt" data-aos="fade-up">
                        <h1 class="sec-tt blog-item-tt">
                            <?php the_title() ?>
                        </h1>
                        <div class="news-time-ctn">
                            <div class="news-time news-detail-time">
                                <img src="<?php echo get_site_url() ?>/template/assets/images/calendar.svg" alt="">
                                <?php echo get_the_date() ?>
                            </div>
                            <div class="news-time news-detail-time">
                                <img src="<?php echo get_site_url() ?>/template/assets/images/document-2.svg" alt="">
                                <?php the_author() ?>
                            </div>
                        </div>

                        <?php
                        $mona_post_detail_image = get_field('mona_post_detail_image');
                        if ( $mona_post_detail_image ) {
                        ?>
                        <div class="blog-item-img">
                            <?php echo wp_get_attachment_image( $mona_post_detail_image, 'full' ) ?>
                        </div>
                        <?php } ?>

                        <div class="blog-dt-content mona-content">
                            <?php the_content() ?>
                        </div>
                        <div class="share">
                            <div class="share-text">
                                <?php echo __( 'Share', 'monamedia' ) ?>
                            </div>
                            <div class="share-social">
                                <a onclick="javascript:window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=500');return false;"
                                    href="https://www.facebook.com/sharer/sharer.php?u=<?php echo urlencode(get_the_permalink()); ?>&t=<?php the_title(); ?>">
                                    <img src="<?php echo get_site_url() ?>/template/assets/images/share-fb.svg" alt="">
                                </a>
                                <a onclick="javascript:window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=500');return false;"
                                    href="http://www.twitter.com/share?url=<?php echo urlencode(get_the_permalink()); ?>">
                                    <img src="<?php echo get_site_url() ?>/template/assets/images/share-tw.svg" alt="">
                                </a>
                                <a onclick="javascript:window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=500');return false;"
                                    href="https://www.linkedin.com/cws/share?url=<?php echo urlencode(get_the_permalink()); ?>&title=<?php the_title(); ?>">
                                    <img src="<?php echo get_site_url() ?>/template/assets/images/share-in.svg" alt="">
                                </a>
                            </div>
                        </div>
                    </div>
                    <?php
                    echo comments_template();
                    ?>
                </div>
                <div class="blog-aside" data-aos="fade-up">
                    <?php if (!function_exists('dynamic_sidebar') || !dynamic_sidebar('sidebar_post')) : ?><?php endif; ?>
                </div>
            </div>
        </div>
    </section>

    <?php 
        /*
        ** GET
        ** TEMPLATE PART
        ** Global section related post
        */
        $slug_part = 'patch/global-content/section';
        $name_part = 'related-post';
        get_template_part($slug_part, $name_part);
    ?>
</main>