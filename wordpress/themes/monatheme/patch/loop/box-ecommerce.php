<?php 
    global $post;
    $post_ID = $post->ID;
    $web_traffic_per_month          = get_field('web_traffic_per_month', $post_ID);
    $ranking_ios                    = get_field('ranking_ios', $post_ID);
    $ranking_android                = get_field('ranking_android', $post_ID);
    $web_traffic_per_social_network = get_field('web_traffic_per_social_network', $post_ID);
    // PHP 8: tránh lỗi khi nhóm trường mạng xã hội để trống.
    if( !is_array($web_traffic_per_social_network) ){
        $web_traffic_per_social_network = [];
    }
    $web_traffic_per_social_network += ['youtube' => '', 'instagram' => '', 'facebook' => ''];
    $web_traffic_width              = get_field('web_traffic_width', $post_ID);
    $ecommerce_title                = get_field('ecommerce_title', $post_ID);
    if( empty($ecommerce_title) ){
        $ecommerce_title = get_the_title($post_ID);
    }
    
    $all_traffic        = intval(preg_replace('/[^0-9_ -]/s', '', $web_traffic_per_month));
    $youtube_traffic    = intval(preg_replace('/[^0-9_ -]/s', '', $web_traffic_per_social_network['youtube']));
    $instagram_traffic  = intval(preg_replace('/[^0-9_ -]/s', '', $web_traffic_per_social_network['instagram']));
    $facebook_traffic   = intval(preg_replace('/[^0-9_ -]/s', '', $web_traffic_per_social_network['facebook']));
?>
<div class="infographic-data-item">
    <div class="item">
        <div class="item-wrap">
            <div class="img">
                <?php echo get_the_post_thumbnail($post_ID, '50x50'); ?>
            </div>
            <div class="name"><?php echo $ecommerce_title; ?></div>
        </div>
    </div>
    <div class="item">
        <p class="percent" style="width: <?php echo $web_traffic_width?$web_traffic_width:'0'; ?>%;"></p>
        <div class="item-value">
            <?php echo $web_traffic_per_month?$web_traffic_per_month:__('n/a','monamedia'); ?>
        </div>
    </div>
    <div class="item">
        <span>
            <?php echo $ranking_ios?$ranking_ios:__('n/a','monamedia'); ?>
        </span>
    </div>
    <div class="item">
        <span>
            <?php echo $ranking_android?$ranking_android:__('n/a','monamedia'); ?>
        </span>
    </div>
    <div class="item">
        <?php 
        if( $all_traffic > 0 && $youtube_traffic <= $all_traffic){
            $percent = $youtube_traffic*100/$all_traffic;
        ?>

        <p class="percent" style="width: <?php echo $percent; ?>%;"></p>
        <div class="item-value">
            <?php echo $web_traffic_per_social_network['youtube'] ?>
        </div>
        <?php
        }else{ ?>

        <p class="percent" style="width: 0%;"></p>
        <div class="item-value">
            <?php echo __('n/a','monamedia'); ?>
        </div>
        <?php } ?>

    </div>
    <div class="item">
        <?php 
        if( $all_traffic > 0 && $instagram_traffic <= $all_traffic){ 
            $percent = $instagram_traffic*100/$all_traffic;
        ?>
        <p class="percent" style="width: <?php echo $percent; ?>%;"></p>
        <div class="item-value">
            <?php echo $web_traffic_per_social_network['instagram'] ?>
        </div>
        <?php
        }else{ ?>

        <p class="percent" style="width: 0%;"></p>
        <div class="item-value">
            <?php echo __('n/a','monamedia'); ?>
        </div>

        <?php } ?>
    </div>
    <div class="item">
        <?php 
        if( $all_traffic > 0 && $facebook_traffic <= $all_traffic){ 
            $percent = $facebook_traffic*100/$all_traffic;
        ?>
        <p class="percent" style="width: <?php echo $percent; ?>%;"></p>
        <div class="item-value">
            <?php echo $web_traffic_per_social_network['facebook'] ?>
        </div>
        <?php
        }else{ ?>

        <p class="percent" style="width: 0%;"></p>
        <div class="item-value">
            <?php echo __('n/a','monamedia'); ?>
        </div>

        <?php } ?>
    </div>
</div>