 <?php
    $title = get_field('m_page_solution_client_title');
    $gallery = get_field('m_page_solution_client_image_client');
    if (!empty($gallery)) {
    ?>
     <div class="hu-brand sc-pd4">
         <div class="container">
             <h3 class="title" data-aos="fade-up">
                 <?php echo $title; ?>
             </h3>
             <div class="hu-brand-wr" data-aos="fade-up">
                 <div class="swiper-container">
                     <div class="swiper-wrapper">
                         <?php foreach ($gallery as $gallery) { ?>
                             <div class="swiper-slide">
                                 <div class="hu-brand-inner">
                                     <span class="hu-brand-it">
                                         <?php if (!empty($gallery)) {
                                                echo wp_get_attachment_image($gallery, 'medium');
                                            }
                                            ?>
                                     </span>
                                 </div>
                             </div>
                         <?php } ?>
                     </div>
                 </div>
                 <div class="hu-brand-ctrl">
                     <div class="btn-prev">
                         <img src="<?php echo get_site_url() ?>/template/assets/images/hu/prev.svg" alt="">
                     </div>
                     <div class="btn-next">
                         <img src="<?php echo get_site_url() ?>/template/assets/images/hu/next.svg" alt="">
                     </div>
                 </div>
             </div>
         </div>
     </div>
 <?php } ?>