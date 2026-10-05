 <?php
    $banner = get_field('m_page_home_banner_rep');
    if (!empty($banner)) {
    ?>
     <div class="hu-bn">
         <div class="swiper-container">
             <div class="swiper-wrapper">
                 <?php foreach ($banner as $banner_item) {
                        $img_banner = $banner_item['m_page_home_banner_rep_image_banner'];
                        $img_banner_mb = $banner_item['m_page_home_banner_rep_image_banner_mb'];
                        $img_in_banner = $banner_item['m_page_home_banner_rep_image_in_banner'];
                        $title = $banner_item['m_page_home_banner_rep_title'];
                        $content = $banner_item['m_page_home_banner_rep_content'];
                        $link = $banner_item['m_page_home_banner_rep_link'];

                    ?>
                     <div class="swiper-slide">
                         <div class="hu-bn-inner">
                             <div class="bg">
                                 <?php
                                    if (wp_is_mobile()) {
                                        if (!empty($img_banner_mb)) {
                                            echo wp_get_attachment_image($img_banner_mb, 'medium');
                                        } else {
                                            echo  '<img src="' . get_site_url() . '/template/assets/images/hu/hu-bn.jpg" alt="">';
                                        }
                                    } else {
                                        if (!empty($img_banner)) {
                                            echo wp_get_attachment_image($img_banner, '1920x600');
                                        } else {
                                            echo  '<img src="' . get_site_url() . '/template/assets/images/hu/hu-bn.jpg" alt="">';
                                        }
                                    }
                                    ?>
                             </div>
                             <div class="hu-bn-content">
                                 <div class="container">
                                     <div class="dnor">
                                         <div class="dnor-item hu-bn-left">
                                             <p class="title white" data-aos="fade-up"><?php echo $title; ?></p>
                                             <p class="desc" data-aos="fade-up" data-aos-delay="300">
                                                 <?php echo $content; ?>
                                             </p>
                                             <?php
                                                if (!empty($link['url'])) {
                                                ?>
                                                 <a href="#form-cta" class="btn-second" data-aos="fade-up" data-aos-delay="500">
                                                     <span class="txt"><?php echo $link['title']; ?></span>
                                                 </a>
                                             <?php } ?>
                                         </div>
                                         <?php if (!empty($img_in_banner)) { ?>
                                             <div class="dnor-item hu-bn-right">
                                                 <div class="hu-bn-img" data-aos="zoom-in">
                                                     <div class="inner">
                                                         <?php if (!empty($img_in_banner)) {
                                                                echo wp_get_attachment_image($img_in_banner, 'larger');
                                                            }
                                                            ?>
                                                     </div>
                                                 </div>
                                             </div>
                                         <?php } ?>
                                     </div>
                                 </div>
                             </div>
                         </div>
                     </div>
                 <?php } ?>
             </div>
             <!-- <div class="swiper-button-next"></div>
             <div class="swiper-button-prev"></div> -->
         </div>
     </div>
 <?php } ?>