<?php
/**
 * Template name: Contact Page
 * @author : Hy Hý
 */
get_header();
while (have_posts()):
    the_post();
    ?>
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

    <?php 
        $contact_information_group = get_field('contact_information_group');
        if( !empty($contact_information_group['contact_information_list']) ){
    ?>
    <section class="section lets-talk contact">
        <div class="contact-header" data-aos="fade-down">
            <div class="container">
                <h1 class="sec-tt contact-tt"><?php echo $contact_information_group['title'] ?></h1>
                <div class="sec-desc lets-talk-desc" data-aos="fade-up">
                    <?php echo $contact_information_group['description']; ?>
                </div>
                <div class="contact-tab">

                    <?php foreach ($contact_information_group['contact_information_list'] as $key_contact_information_list => $contact_information_list_item) { ?>
                    <div class="tab <?php echo $key_contact_information_list==0?'active':''; ?>"
                        data-office_information="<?php echo sanitize_title($contact_information_list_item['contact_information_title']) ?>">
                        <?php echo $contact_information_list_item['contact_information_title']; ?>
                    </div>
                    <?php } ?>

                </div>
            </div>
        </div>
        <div class="contact-panel" data-aos="fade-up">
            <?php foreach ($contact_information_group['contact_information_list'] as $key_contact_information_list => $contact_information_list_item) { ?>
            <div class="tab-panel <?php echo $key_contact_information_list==0?'active':''; ?> maps 
                <?php echo sanitize_title($contact_information_list_item['contact_information_title']) ?>">
                <div class="container">
                    <div class="lets-talk-ctn">
                        <div class="lets-talk-text">
                            <?php if( !empty($contact_information_list_item['contact_information']) ){ ?>
                            <div class="lets-talk-list">
                                <?php foreach ($contact_information_list_item['contact_information'] as $key => $contact_information_item) {
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
                            $contact_form = $contact_information_list_item['contact_form'];
                            if( !empty($contact_form['shortcode_contact_form']) ){
                        ?>
                        <div class="lets-talk-form">
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
                <?php if( !empty($contact_information_list_item['contact_map']) ){ ?>

                <div class="map" data-aos="fade-up">
                    <?php echo $contact_information_list_item['contact_map']; ?>
                </div>

                <?php } ?>
            </div>
            <?php } ?>
        </div>
    </section>
    <?php } ?>
</main>
<?php
endwhile;
get_footer();
?>