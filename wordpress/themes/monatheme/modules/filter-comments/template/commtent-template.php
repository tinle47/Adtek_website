<div class="blog-comment">
    <div class="comment-form" data-aos="fade-up">
        <?php
        $comment_form = array(
            'title_reply' => __( 'Leave a Comment', 'monamedia' ),
            'comment_notes_before' => '',
            'comment_notes_after' => '',
            'comment_field' => '<div class="f-r"><div class="f-c">
                <textarea id="comment" name="comment" class="form-text" placeholder="'.__( 'Write comment', 'monamedia' ).'"></textarea>
            </div></div>',
            'fields'        => array(
                  'author'    => '<div class="f-r w-50"><div class="f-c">
                                      <input type="text" id="author" name="author" placeholder="'.__( 'Your name *', 'monamedia' ).'">
                                  </div></div>',
                  'email'     =>    '<div class="f-r w-50"><div class="f-c">
                                      <input type="text" id="email" name="email" placeholder="'.__( 'Your email *', 'monamedia' ).'">
                                  </div></div>',
                  'url'       =>  '',
                  'cookies'   =>  '',
            ),
            'class_form'    => '',
            'label_submit'  => '',
            'logged_in_as'  => '',
            'submit_button' => '<div class="f-r"><div class="f-c">
                                  <button type="submit" id="submit-comment" class="btn">'. __( 'Submit comment','monamedia' ) . '</button>
                              </div></div>',
        );

        comment_form( $comment_form );
        ?>
    </div>
    <div class="comment-list">
        <?php
        $comments = get_comments(
            [
                'post_id' => get_the_ID(),
                'post_type' => get_post_type(),
            ]
        );
        if ( ! empty( $comments ) && count( $comments ) > 0 ) {
            $args_list = array(
                'walker'            => null,
                'max_depth'         => '',
                'style'             => 'li',
                'short_ping'        => true,
                'avatar_size'       => 40,
                'callback'          => 'mona_filter_comment_items',
                'type'              => 'all',
                'reply_text'        => __('Comment', 'monamedia'),
                'page'              => '',
                'per_page'          => '',
                'reverse_top_level' => null,
                'reverse_children'  => ''
            );
            wp_list_comments($args_list, $comments);
        } else {
            $comment_text = '<div class="mona-mess-empty commtent-empty">';
            $comment_text .= __( 'There are currently no reviews yet', 'monamedia' );
            $comment_text .= '</div>';
            echo $comment_text;
        }
        ?>
    </div>
</div>
