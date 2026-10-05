<?php
/**
 * Class chỉnh sửa lại form comment theo post type
 * define
 */
define( 'MODULE_COMMTENT_FOLDER', 'modules/filter-comments' );

require_once( get_template_directory() . '/modules/filter-comments/function.php' );

class MComments_Template {

    /**
     * Undocumented function
     */
    public function __construct() {

        add_filter( 'comments_template', [ $this, 'mona_filter_commtent_template' ] );
        add_filter( 'avatar_defaults', [ $this, 'mona_filter_avatar_defaults' ], 10, 1 );
        add_action( 'wp_enqueue_scripts', [$this, 'mona_commtent_add_style'] );

    }

    /**
     * Undocumented function
     *
     * @param [type] $comment_template
     * @return void
     */
    public function mona_filter_commtent_template( string $comment_template ) {

        global $post;

        if ( ! ( is_singular() && ( have_comments() || 'open' == $post->comment_status ) ) ) {
            return;
        }

        $post_allows = $this->mona_comment_post_types();

        $commtent_file_path = locate_template( MODULE_COMMTENT_FOLDER . '/template/commtent-template.php' );

        if ( in_array( $post->post_type, $post_allows ) && file_exists ( $commtent_file_path ) ) {


            $comment_template = $commtent_file_path;
        }

        return $comment_template;

    }

    public function mona_filter_avatar_defaults( array $avatar_defaults ) {

        $custommer_commtent_file_path = locate_template( MODULE_COMMTENT_FOLDER . '/images/cmt-avt2.png' );

        if ( file_exists ( $custommer_commtent_file_path ) ) {

            $avatar_defaults[$custommer_commtent] = __( 'Custommer Commtent', 'monamedia' );
        }

        return $avatar_defaults;

    }

    /**
     * Undocumented function
     *
     * @return void
     */
    public function mona_comment_post_types() {

        $args = array(
            'post',
        );

        return (array)$args;

    }

    /**
     * Undocumented function
     *
     * @return void
     */
    public function mona_commtent_add_style() {

        // loading css
        wp_enqueue_style( 'mona-filter-commtent-style', get_template_directory_uri() .'/'. MODULE_COMMTENT_FOLDER . '/css/style-commtent.css', array(), false );
    }

}

if ( class_exists( 'MComments_Template' ) ) {
    new MComments_Template();
}
