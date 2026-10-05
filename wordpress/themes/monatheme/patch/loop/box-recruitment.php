<?php 
    global $post;
    $post_ID = $post->ID;
    $department = get_post_term_ids($post_ID, 'department_recruitment');
    $level      = get_post_term_ids($post_ID, 'level_recruitment');
    $city      = get_post_term_ids($post_ID, 'city_recruitment');
?>
<div class="recruitment-item news-item">
    <a href="<?php echo get_the_permalink($post_ID); ?>" class="news-wrap">
        <div class="news-img">
            <?php echo get_the_post_thumbnail( $post_ID, '370x250' ); ?>
        </div>
        <div class="news-body">
            <div class="news-time">
                <img src="<?php echo get_site_url() ?>/template/assets/images/calendar.svg" alt="">
                <?php echo get_the_date('d F, Y', $post_ID); ?>
            </div>
            <div class="news-name"><?php echo get_the_title($post_ID); ?></div>
            <div class="recruitment-info">
                <?php 
                    if( !empty($department) ){
                ?>
                <div class="recruitment-info-item">
                    <div class="title"><?php echo __('Department','monamedia'); ?></div>
                    <div class="detail">
                        <?php 
                        foreach ($department as $key => $id) {
                            $obj = get_term_by('id',  $id, 'department_recruitment');
                            if( empty($department[$key+1]) ){
                                echo $obj->name;
                            }else{
                                echo $obj->name . ' - ';
                            }
                        } 
                        ?>
                    </div>
                </div>
                <?php } ?>

                <?php 
                    if( !empty($level) ){
                ?>
                <div class="recruitment-info-item">
                    <div class="title"><?php echo __('Level','monamedia'); ?></div>
                    <div class="detail">
                        <?php 
                        foreach ($level as $key => $id) {
                            $obj = get_term_by('id',  $id, 'level_recruitment');
                            if( empty($level[$key+1]) ){
                                echo $obj->name;
                            }else{
                                echo $obj->name . ' - ';
                            }
                        } 
                        ?>
                    </div>
                </div>
                <?php } ?>

                <?php 
                    if( !empty($city) ){
                ?>
                <div class="recruitment-info-item">
                    <div class="title"><?php echo __('City','monamedia'); ?></div>
                    <div class="detail">
                        <?php 
                        foreach ($city as $key => $id) {
                            $obj = get_term_by('id',  $id, 'city_recruitment');
                            if( empty($city[$key+1]) ){
                                echo $obj->name;
                            }else{
                                echo $obj->name . ' - ';
                            }
                        } 
                        ?>
                    </div>
                </div>
                <?php } ?>
            </div>
            <div class="news-view">
                <?php echo __('View Report','monamedia'); ?>
            </div>
        </div>
    </a>
</div>