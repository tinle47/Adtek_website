 <?php
    $title = get_field('m_page_home_growth_title');
    $number = get_field('m_page_home_growth_list_number');
    $list = get_field('m_page_home_growth_list');

    ?>
 <div class="hu-mkt sc-pd4">
     <div class="container">
         <h3 class="hu-mkt-tt" data-aos="fade-left">
             <?php echo $title; ?>
         </h3>
         <?php if (!empty($list)) { ?>
             <div class="hu-mkt-block">
                 <?php foreach ($list as $list) {
                        $rep = $list['m_page_home_growth_list_infor'];
                        $img = $list['m_page_home_growth_list_image'];
                    ?>
                     <div class="hu-mkt-item">
                         <div class="dnor">
                             <div class="hu-mkt-content dnor-item" data-aos="fade-up">
                                 <h4 class="title">
                                     <?php echo $list['m_page_home_growth_list_title']; ?>
                                 </h4>
                                 <div class="desc mona-content">
                                     <?php echo $list['m_page_home_growth_list_content']; ?>
                                 </div>
                             </div>

                             <div class="hu-mkt-img dnor-item" data-aos="flip-right">
                                 <div class="inner">
                                     <?php if (!empty($img)) {
                                            echo wp_get_attachment_image($img, 'larger');
                                        } else {
                                            echo  '<img src="' . get_site_url() . '/template/assets/images/default-image.jpg" alt="">';
                                        }
                                        ?>
                                 </div>
                                 <?php if (!empty($list['m_page_home_growth_list_name'])) { ?>
                                     <p class="name">
                                         <?php echo $list['m_page_home_growth_list_name']; ?>
                                     </p>
                                     <?php if (!empty($rep)) { ?>
                                         <ul class="list">
                                             <?php foreach ($rep as $rep) { ?>
                                                 <li class="lis-it">
                                                     <?php echo $rep['m_page_home_growth_list_infor_text']; ?>
                                                 </li>
                                             <?php } ?>
                                         </ul>
                                     <?php } ?>
                                 <?php } ?>
                             </div>

                         </div>
                     </div>
                 <?php } ?>
             </div>
         <?php } ?>
     </div>
 </div>
 <?php
    $number = get_field('m_page_home_growth_list_number');
    if (!empty($number)) {
    ?>
     <div class="hu-countup">
         <div class="container">
             <div class="hu-countup-wr">
                 <div class="dnor">
                     <?php foreach ($number as $number) { ?>
                         <div class="dnor-item">
                             <div class="hu-countup-it">
                                 <p class="num">
                                     <span class="num-inner countNum"><?php echo $number['m_page_home_growth_list_number_number']; ?></span>
                                     <span class="num-plus">+</span>
                                 </p>
                                 <p class="txt">
                                     <?php echo $number['m_page_home_growth_list_number_text']; ?>
                                 </p>
                             </div>
                         </div>
                     <?php } ?>
                 </div>
             </div>
         </div>
     </div>
 <?php } ?>