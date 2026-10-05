<?php 
    global $post;
    $post_ID = $post->ID;
?>
<div class="blog-item" data-aos="fade-up">
    <div class="blog-item-wrap">
		<?php if ( has_post_thumbnail( $post_ID ) ) { ?>
        <a href="<?php echo get_the_permalink($post_ID); ?>" class="blog-item-img">
            <?php echo get_the_post_thumbnail($post_ID, '870x362'); ?>
        </a>
		<?php } ?>
        <div class="blog-item-body <?php echo has_post_thumbnail( $post_ID ) ? 'item-br' : 'item-br-t' ?>">
            <h2 class="sec-tt blog-item-tt">
                <a href="<?php echo get_the_permalink($post_ID); ?>">
                    <?php echo get_the_title($post_ID); ?>
                </a>
            </h2>
            <div class="news-time-ctn">
                <div class="news-time news-detail-time">
                    <img src="<?php echo get_site_url() ?>/template/assets/images/calendar.svg" alt="">
                    <?php echo get_the_date('F d, Y', $post_ID) ?>
                </div>
                <div class="news-time news-detail-time">
                    <img src="<?php echo get_site_url() ?>/template/assets/images/document-2.svg" alt="">
                    <?php echo get_the_author(); ?>
                </div>
            </div>
            <div class="blog-item-desc">
                <?php echo get_the_excerpt($post_ID); ?>
            </div>
            <div class="share">
                <div class="share-text"><?php echo __('Share','monamedia'); ?></div>
                <div class="share-social">
                    <a href="https://www.facebook.com/sharer/sharer.php?u=<?php echo urlencode(get_the_permalink($post_ID)); ?>&t=<?php echo get_the_title($post_ID); ?>"
                        onclick="javascript:window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=500');
                        return false;">
                        <img src="<?php echo get_site_url() ?>/template/assets/images/share-fb.svg" alt="">
                    </a>

                    <a href="http://www.twitter.com/share?url=<?php echo urlencode(get_the_permalink()); ?>"
                        class="item twitter" onclick="javascript:window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=500');
                        return false;">
                        <img src="<?php echo get_site_url() ?>/template/assets/images/share-tw.svg" alt="">
                    </a>

                    <a href="https://www.linkedin.com/cws/share?url=<?php echo urlencode(get_the_permalink()); ?>&title=<?php the_title(); ?>"
                        onclick="javascript:window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=500');
                        return false;">
                        <img src="<?php echo get_site_url() ?>/template/assets/images/share-in.svg" alt="">
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>