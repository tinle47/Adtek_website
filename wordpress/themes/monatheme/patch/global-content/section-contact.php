<?php 
    $mona_aboutus_contact = get_field('mona_aboutus_contact');
    if( empty($mona_aboutus_contact) ){
        $mona_aboutus_contact = get_field('mona_aboutus_contact', MONA_PAGE_HOME);
    }
    if( !empty($mona_aboutus_contact) ){
?>
<section class="section lets-talk">
    <div class="container">
        <div class="lets-talk-ctn">
            <div class="lets-talk-text">
                <h2 class="sec-tt lets-talk-tt" data-aos="fade-down">
                    <?php echo $mona_aboutus_contact['title']; ?>
                </h2>
                <div class="sec-desc lets-talk-desc" data-aos="fade-up">
                    <?php echo $mona_aboutus_contact['description']; ?>
                </div>
                <?php if( !empty($mona_aboutus_contact['contact_information']) ){ ?>
                <div class="lets-talk-list" data-aos="fade-up">
                    <?php foreach ($mona_aboutus_contact['contact_information'] as $key => $contact_information_item) {
                        $information_select = $contact_information_item['information_select'];
                        $information_detail = $contact_information_item['information_detail'];
                        $icon = $contact_information_item['icon'];
                        $title = $contact_information_item['title'];
                        if( $information_select == 'value_text' ){
                            $action = 'javascript:;';
                        }elseif ( $information_select == 'value_email' ) {
                            $action = 'mailto:'.$information_detail;
                        }elseif ( $information_select == 'value_tel' ) {
                            $action = mona_replace_tel($information_detail);
                        }elseif( $information_select == 'value_link' ){
                            $action = esc_url($information_detail);
                        }
                    ?>
                    <a href="<?php echo $action; ?>" class="lets-talk-item">
                        <div class="icon">
                            <?php echo wp_get_attachment_image( $icon, '50x50'); ?>
                        </div>
                        <div class="text">
                            <div class="text-tt"><?php echo $title; ?></div>
                            <div class="text-desc">
                                <?php echo $information_detail; ?>
                            </div>
                        </div>
                    </a>
                    <?php } ?>
                </div>
                <?php } ?>
            </div>

            <?php 
                $contact_form = $mona_aboutus_contact['contact_form'];
                if( !empty($contact_form['shortcode_contact_form']) ){
            ?>
            <div class="lets-talk-form" data-aos="fade-up">
                <div class="form">
                    <div class="form-tt">
                        <?php echo $contact_form['title_contact_form']; ?>
                    </div>
                    <div class="form-desc">
                        <?php echo $contact_form['description_contact_form']; ?>
                    </div>
                    <?php echo do_shortcode($contact_form['shortcode_contact_form']); ?>
                </div>
            </div>
            <?php } ?>
        </div>
    </div>
</section>

<?php if( !empty($mona_aboutus_contact['contact_map']) ){ ?>
<section class="maps">
    <div class="map" data-aos="fade-up">
        <?php echo $mona_aboutus_contact['contact_map']; ?>
    </div>
</section>
<?php } ?>

<?php } ?>