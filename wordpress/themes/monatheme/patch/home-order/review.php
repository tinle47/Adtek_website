 <?php
    $title = get_field('m_page_home_review_infor');
    $content = get_field('m_page_home_review_content');
    $link = get_field('m_page_home_review_link');
    $img = get_field('m_page_home_review_image');
    ?>

 <div class="hu-cpn">
     <div class="bg">
         <?php if (!empty($img)) {
                echo wp_get_attachment_image($img, 'full');
            } else {
                echo  '<img src="' . get_site_url() . '/template/assets/images/default-image.jpg" alt="">';
            }
            ?>
     </div>
     <div class="container">
         <div class="hu-cpn-wr">
             <p class="text" data-aos="zoom-in">
                 <?php
                    echo str_replace(
                        ['[', ']'],
                        ['<span class="text-bold">', '</span>'],
                        $title
                    );
                    ?>
             </p>
             <p class="desc" data-aos="zoom-in">
                 <?php echo $content; ?>
             </p>
             <?php if (!empty($link['url'])) { ?>
                 <a href="<?php echo $link['url']; ?>" class="btn-second" data-aos="zoom-in">
                     <span class="txt"><?php echo $link['title']; ?></span>
                 </a>
             <?php } ?>
         </div>
     </div>
 </div>