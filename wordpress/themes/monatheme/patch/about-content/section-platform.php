<?php 
    $mona_aboutus_platform = get_field('mona_aboutus_platform');
    $platforms = $mona_aboutus_platform['platforms'];
    $stackTab = [];
    $stackFilter = [];
    foreach ($platforms as $key => $platform_item) {
        $platform_title_sanitize = sanitize_title($platform_item['platform_title']);
        $temp = [
            'label'=>$platform_item['platform_title'],
            'filter'=>$platform_title_sanitize
        ];
      
        if( !in_array($platform_title_sanitize,$stackFilter) ){
            array_push($stackFilter, $platform_title_sanitize);
            array_push($stackTab, $temp);
        }
    }
?>
<?php 
    if( !empty($stackFilter) && !empty($stackTab) && !empty($platforms) ){
?>
<section class="section platform">
    <div class="container">
        <div class="platform-header" data-aos="fade-down">
            <h2 class="sec-tt platform-tt">
                <?php echo $mona_aboutus_platform['title']; ?>
            </h2>
            <div class="platform-tab">
                <div class="platform-tab-item active" data-filter="*"><?php echo __('All','monamedia'); ?></div>
                <?php foreach ($stackTab as $key => $tab) { ?>
                <div class="platform-tab-item" data-filter="<?php echo $tab['filter']; ?>">
                    <?php echo $tab['label']; ?>
                </div>
                <?php } ?>
            </div>
        </div>
        <div class="platform-isotope" id="lightgallery">
            <div class="platform-isotope-item">
                <div class="platform-list">
                    <?php foreach ($platforms as $key => $platform_item) { ?>
                    <div class="platform-item"
                        data-filter="<?php echo sanitize_title($platform_item['platform_title']); ?>">
                        <div class="item">
                            <div class="img lightgallery-selector"
                                data-src="<?php echo wp_get_attachment_image_url( $platform_item['platform_image'], 'full'); ?>">
                                <?php echo wp_get_attachment_image( $platform_item['platform_image'], $platform_item['platform_size']); ?>
                            </div>
                        </div>
                    </div>
                    <?php } ?>
                </div>
            </div>
        </div>
    </div>
</section>
<?php } ?>