<?php
/**
 * Undocumented class
 * Create widget
 */
class M_Widget_default extends WP_Widget {

    public $Mona_Widgets;

    /**
     * Undocumented function
     */
    function __construct() {

        parent::__construct(
            'm_default_text',
            __('Mona - Default Text', 'monamedia'),
            [
                'description' => __( 'Hiển thị ô nhập giá trị văn bản ngắn', 'monamedia' ),
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
        $title = isset( $instance['title'] ) ? $instance['title'] : '';
        ?>
        <div class="mona-ft-text-default">
            <p><?php echo esc_attr( $title ) ?></p>
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

        $instance['title'] = $this->Mona_Widgets->update_field( $new_instance['title'] );

        return $instance;

    }

}

/**
 * Undocumented function
 *
 * Register and load the widget
 * @return void
 */
function Register_Widget_Default_Text() {
    register_widget( 'M_Widget_default' );
}
add_action( 'widgets_init', 'Register_Widget_Default_Text' );
