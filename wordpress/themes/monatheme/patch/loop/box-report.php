<?php 
    global $post;
    $post_ID = $post->ID;
?>
<div class="news-item">
    <a href="<?php echo get_the_permalink($post_ID); ?>" class="news-wrap">
        <div class="news-img">
            <?php echo get_the_post_thumbnail($post_ID, '370x250'); ?>
        </div>
        <div class="news-body">
            <div class="news-time">
                <img src="<?php echo get_site_url() ?>/template/assets/images/calendar.svg" alt="">
                <?php echo get_the_date('F d, Y', $post_ID) ?>
            </div>
            <div class="news-name">
                <?php echo get_the_title($post_ID); ?>
            </div>
            <div class="news-desc"><?php echo get_the_excerpt($post_ID); ?></div>
            <div class="news-view">
                <?php echo __('View Report','monamedia'); ?>
            </div>
        </div>
    </a>
</div>