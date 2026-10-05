 <?php
    $title = get_field('m_page_home_blog_title');
    $sel = get_field('m_page_home_blog_select');
    $rel = get_field('m_page_home_blog_post');
    ?>
 <div class="hu-know sc-pd4">
     <div class="container">
         <h3 class="title" data-aos="fade-up">
             <?php echo $title; ?>
         </h3>
         <?php
            $post_per = 6;
            $argsPost = array(
                'post_type' => 'post',
                'post_status' => 'publish',
                'posts_per_page' => $post_per,
                // 'order' => $order,


            );
            if (!empty($rel)) {
                $argsPost['post__in'] = $rel;
            }
            $loop = new WP_Query($argsPost);
            if ($loop->have_posts()) {
            ?>
             <div class="hu-know-list" data-aos="fade-up">
                 <div class="dnor">
                     <?php
                        while ($loop->have_posts()) :
                            $loop->the_post();
                            global $post;
                            $post_ID = $post->ID;
                        ?>
                         <div class="dnor-item">
                             <div class="hu-know-it">
                                 <div class="inner">
                                     <div class="img">
                                         <a href="<?php echo get_the_permalink($post_ID); ?>" class="img-inner">
                                             <?php echo get_the_post_thumbnail($post_ID, '370x250'); ?>
                                         </a>
                                     </div>
                                     <div class="info">
                                         <h4>
                                             <a href="<?php echo get_the_permalink($post_ID); ?>" class="info-tt">
                                                 <?php echo get_the_title($post_ID); ?>
                                             </a>
                                         </h4>
                                         <div class="desc">
                                             <?php echo get_the_excerpt($post_ID); ?>
                                         </div>
                                     </div>
                                 </div>
                             </div>
                         </div>
                     <?php
                        endwhile;
                        wp_reset_query();
                        ?>
                 </div>
             </div>
         <?php } ?>
     </div>
 </div>