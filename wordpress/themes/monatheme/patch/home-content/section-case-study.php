<?php 
        $mona_casestudy = get_field('mona_casestudy');
        if( !empty($mona_casestudy) ){
    ?>
<section class="section case-study">
    <div class="case-study-list">
        <?php foreach ($mona_casestudy as $key => $casestudy_item) { ?>
        <div class="case-study-item">
            <div class="case-study-img" data-aos="zoom-in">
                <?php echo wp_get_attachment_image($casestudy_item['img'], '960x534'); ?>
            </div>
            <div class="case-study-text" data-aos="zoom-in">
                <h2 class="sec-tt case-study-tt">
                    <?php echo $casestudy_item['title']; ?>
                </h2>
                <div class="sec-desc case-study-desc mona-content">
                    <?php echo $casestudy_item['description']; ?>
                </div>

                <?php if( !empty($casestudy_item['list_casestudy_attribute']) ){ ?>
                <div class="case-study-attr">
                    <?php foreach ( $casestudy_item['list_casestudy_attribute'] as $key_casestudy_attr => $casestudy_attr_item ) { ?>
                    <div class="case-study-attr-item">
                        <div class="case-study-attr-icon">
                            <?php echo wp_get_attachment_image($casestudy_attr_item['casestudy_attribute_icon'], '30x30'); ?>

                        </div>
                        <div class="case-study-attr-number">
                            <div class="countNum">
                                <?php echo $casestudy_attr_item['casestudy_attribute_title']; ?>
                            </div>
                            <?php if( !empty($casestudy_attr_item['casestudy_attribute_title_decor']) ){ ?>
                            <span><?php echo $casestudy_attr_item['casestudy_attribute_title_decor']; ?></span>
                            <?php } ?>
                        </div>
                        <div class="case-study-attr-desc">
                            <?php echo $casestudy_attr_item['casestudy_attribute_description']; ?>
                        </div>
                    </div>
                    <?php } ?>
                </div>
                <?php } ?>
            </div>
        </div>
        <?php } ?>
    </div>
</section>
<?php } ?>