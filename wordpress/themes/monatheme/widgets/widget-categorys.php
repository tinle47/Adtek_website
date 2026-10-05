<?php
/**
 * Undocumented class
 * Create widget
 */
class M_Widget_categorys extends WP_Widget {

    public $Mona_Widgets;

    /**
     * Undocumented function
     */
    function __construct() {

        parent::__construct(
            'm_categorys',
            __('Mona - Categorys', 'monamedia'),
            [
                'description' => __( 'Hiển thị danh sách chuyên mục theo tùy chọn', 'monamedia' ),
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
            <?php
            $categorys = get_terms(
                [
                    'taxonomy' => $options,
                    'hide_empty' => false,
                ]
            );
            if ( ! empty ( $categorys ) ) {
            ?>
            <ul class="blog-aside-cate">
                <?php
                foreach ( $categorys as $key => $term ) {

                    if ( is_tax() && get_queried_object_id() == $term->term_id ) {

                        echo '<li class="current"><a href="'.get_term_link( $term->term_id ).'">'.$term->name.'</a></li>';
                    } else {

                        echo '<li><a href="'.get_term_link( $term->term_id ).'">'.$term->name.'</a></li>';
                    }
                }
                ?>
            </ul>
            <?php } ?>
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
                'title'       => __( 'Title', 'monamedia' ),
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
                'placeholder' => __( 'Chọn loại chuyên mục', 'monamedia' ),
                'docs'        => false,
                'select'      => [
                    'category' => __( 'Category Post', 'monamedia' )
                ]
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
function Register_Widget_Categorys() {
    register_widget( 'M_Widget_categorys' );
}
add_action( 'widgets_init', 'Register_Widget_Categorys' );
