<?php
/**
 * Undocumented function
 *
 * @param [type] $comment
 * @param [type] $args
 * @param [type] $depth
 * @return void
 */
function mona_filter_comment_items( $comment, $args, $depth ) {

    $obz = get_queried_object();
	$GLOBALS['comment'] = $comment;
    $meta_rating_count = get_comment_meta( $comment->comment_ID, 'rating', true );
    ?>
    <li class="comment-item" <?php comment_class('cf'); ?> id="li-comment-<?php comment_ID() ?>" data-aos="fade-up">
        <div class="comment-avt">
            <img src="<?php echo esc_url( get_option( 'avatar_default', true ) ) ?>" alt="custommer-avatar">
        </div>
        <div class="comment-body">
            <div class="comment-name">
                <?php echo $comment->comment_author; ?>
            </div>
            <div class="comment-content">
                <?php comment_text() ?>
            </div>
        </div>
    <?php
}
