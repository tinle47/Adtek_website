  <?php
    $title = get_field('m_page_home_form_title');
    $content = get_field('m_page_home_form_content');
    $email = get_field('m_page_home_form_list_email');
    $phone = get_field('m_page_home_form_list_phone');
    $banner = get_field('m_page_home_form_banner');
    $form = get_field('m_page_home_form_code_form');
    ?>
  <div class="hu-ct sc-pd4" id="form-cta">
      <div class="bg">
          <?php if (!empty($banner)) {
                echo wp_get_attachment_image($banner, 'full');
            } else {
                echo  '<img src="' . get_site_url() . '/template/assets/images/default-image.jpg" alt="">';
            }
            ?>
      </div>
      <div class="container">
          <div class="hu-ct-wr">
              <h3 class="title" data-aos="fade-up">
                  <?php echo $title; ?>
              </h3>
              <div class="dnor">
                  <div class="dnor-item">
                      <div class="hu-ct-inner">
                          <p class="hu-ct-desc" data-aos="fade-up">
                              <?php echo $content; ?>
                          </p>
                          <div class="hu-ct-method" data-aos="fade-up">
                              <?php if (!empty($email)) { ?>
                                  <a href="mailto:<?php echo $email['m_page_home_form_list_email_infor']; ?>" class="hu-ct-link">
                                      <span class="icon">
                                          <?php if (!empty($email['m_page_home_form_list_email_icon'])) {
                                                echo wp_get_attachment_image($email['m_page_home_form_list_email_icon'], 'medium');
                                            } else {
                                                echo  '<img src="' . get_site_url() . '/template/assets/images/default-image.jpg" alt="">';
                                            }
                                            ?>
                                      </span>
                                      <span class="txt">
                                          <span class="txt-name">
                                              <?php echo $email['m_page_home_form_list_email_title']; ?>
                                          </span>
                                          <span class="txt-desc">
                                              <?php echo $email['m_page_home_form_list_email_infor']; ?>
                                          </span>
                                      </span>
                                  </a>
                              <?php
                                } ?>

                              <?php if (!empty($phone)) { ?>
                                  <a href="tel:<?php echo $phone['m_page_home_form_list_phone_infor']; ?>" class="hu-ct-link">
                                      <span class="icon">
                                          <?php if (!empty($phone['m_page_home_form_list_phone_icon'])) {
                                                echo wp_get_attachment_image($phone['m_page_home_form_list_phone_icon'], 'medium');
                                            } else {
                                                echo  '<img src="' . get_site_url() . '/template/assets/images/default-image.jpg" alt="">';
                                            }
                                            ?>
                                      </span>
                                      <span class="txt">
                                          <span class="txt-name">
                                              <?php echo $phone['m_page_home_form_list_phone_title']; ?>
                                          </span>
                                          <span class="txt-desc">
                                              <?php echo $phone['m_page_home_form_list_phone_infor']; ?>
                                          </span>
                                      </span>
                                  </a>
                              <?php } ?>
                          </div>
                      </div>
                  </div>
                  <div class="dnor-item">
                      <div class="hu-ct-form">
                          <?php echo do_shortcode($form); ?>
                      </div>
                  </div>
              </div>
          </div>
      </div>
  </div>