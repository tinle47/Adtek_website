<?php
/**
 * Undocumented class
 * Create widget
 */
class M_Widget_recent_posts extends WP_Widget {

    public $Mona_Widgets;

    /**
     * Undocumented function
     */
    function __construct() {

        parent::__construct(
            'm_recent_posts',
            __('Mona - Recent Posts', 'monamedia'),
            [
                'description' => __( 'Hiển thị danh sách bài viết gần đây', 'monamedia' ),
            ]
        );

        $this->Mona_Widgets = new Mona_Exs_Widgets();
    }

    /**
     * Undocumented function
     *
     * @param [type] $args
     * @param [type] $instance
     * @return void
     */
    public function widget( $args, $instance ) {

        $widget_id = $args['widget_id'];
        $icon    = isset( $instance['icon'] ) ? $instance['icon'] : '';
        $title   = isset( $instance['title'] ) ? $instance['title'] : '';
        $options = isset( $instance['options'] ) ? $instance['options'] : '';
        ?>
<div class="blog-aside-item">
    <div class="blog-aside-tt">
        <img src="<?php echo esc_url( $icon ) ?>" alt="">
        <?php echo esc_attr( $title ) ?>
    </div>
    <div class="blog-posts">
        <?php
                $args_posts = [
                    'post_type' => $options ? $options : 'post',
                    'post_ststus' => 'publish',
                    'posts_per_page' => 5,
                    'post__not_in' => [get_the_ID()],
                ];
                $query_posts = new WP_Query( $args_posts );
                if ( $query_posts->have_posts() ) {
                    while ( $query_posts->have_posts() ) :
                         $query_posts->the_post();
                ?>
        <div class="posts-item">
            <a href="<?php the_permalink() ?>" class="posts-item-wrap">
                <div class="posts-img">
                    <?php the_post_thumbnail( '140x120' ) ?>
                </div>
                <div class="posts-body">
                    <div class="posts-tt">
                        <?php the_title() ?>
                    </div>
                    <div class="posts-time news-time">
                        <img src="<?php echo get_site_url() ?>/template/assets/images/calendar.svg" alt="">
                        <?php echo get_the_date() ?>
                    </div>
                </div>
            </a>
        </div>
        <?php
                endwhile;
                wp_reset_query();
                } else { ?>
        <div class="mona-mess-empty">
            <p><?php echo __( 'Content is being update!', 'monamedia' ) ?></p>
        </div>
        <?php } ?>
    </div>
</div>
<?php

    }

    /**
     * Undocumented function
     *
     * Widget Backend
     * @param [type] $instance
     * @return void
     */
    public function form( $instance ) {

        if ( isset( $instance[ 'icon' ] ) ) {
            $icon = $instance[ 'icon' ];
        } else {
            $icon = '';
        }

        $this->Mona_Widgets->create_field(
            [
                'type'        => 'image',
                'name'        => $this->get_field_name( 'icon' ),
                'id'          => $this->get_field_id( 'icon' ),
                'value'       => $icon,
                'title'       => __( 'Icon', 'monamedia' ),
                'placeholder' => '',
                'docs'        => false,
            ]
        );

        if ( isset( $instance[ 'title' ] ) ) {
            $title = $instance[ 'title' ];
        } else {
            $title = '';
        }

        $this->Mona_Widgets->create_field(
            [
                'type'        => 'text',
                'name'        => $this->get_field_name( 'title' ),
                'id'          => $this->get_field_id( 'title' ),
                'value'       => $title,
                'title'       => __( 'Text', 'monamedia' ),
                'placeholder' => __( 'Nhập nội dung văn bản', 'monamedia' ),
                'docs'        => false,
            ]
        );

        if ( isset( $instance[ 'options' ] ) ) {
            $options = $instance[ 'options' ];
        } else {
            $options = '';
        }

        $this->Mona_Widgets->create_field(
            [
                'type'        => 'select',
                'name'        => $this->get_field_name( 'options' ),
                'id'          => $this->get_field_id( 'options' ),
                'value'       => $options,
                'title'       => __( 'Select', 'monamedia' ),
                'placeholder' => __( 'Chọn loại bài viết', 'monamedia' ),
                'docs'        => false,
                'select'      => [
                    'post' => __( 'Posts', 'monamedia' )
                ]
            ]
        );

        if ( isset( $instance[ 'count' ] ) ) {
            $title = $instance[ 'title' ];
        } else {
            $title = '';
        }

        $this->Mona_Widgets->create_field(
            [
                'type'        => 'text',
                'name'        => $this->get_field_name( 'title' ),
                'id'          => $this->get_field_id( 'title' ),
                'value'       => $title,
                'title'       => __( 'Text', 'monamedia' ),
                'placeholder' => __( 'Nhập nội dung văn bản', 'monamedia' ),
                'docs'        => false,
            ]
        );

    }

    /**
     * Undocumented function
     *
     * Updating widget replacing old instances with new
     * @param [type] $new_instance
     * @param [type] $old_instance
     * @return void
     */
    public function update( $new_instance, $old_instance ) {

        $instance = [];

        $instance['title']    = $this->Mona_Widgets->update_field( $new_instance['title'] );
        $instance['icon']     = $this->Mona_Widgets->update_field( $new_instance['icon'] );
        $instance['options']  = $this->Mona_Widgets->update_field( $new_instance['options'] );

        return $instance;

    }

}

/**
 * Undocumented function
 *
 * Register and load the widget
 * @return void
 */
function Register_Widget_Recent_Posts() {
    register_widget( 'M_Widget_recent_posts' );
}
add_action( 'widgets_init', 'Register_Widget_Recent_Posts' );