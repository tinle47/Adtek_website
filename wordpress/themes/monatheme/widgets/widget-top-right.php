<?php
/**
 * Undocumented class
 * Create widget
 */
class M_Widget_topright extends WP_Widget {

    public $Mona_Widgets;

    /**
     * Undocumented function
     */
    function __construct() {

        parent::__construct(
            'm_topright',
            __('Mona - Socialnetwork', 'monamedia'),
            [
                'description' => __( 'Display socialnetwork', 'monamedia' ),
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
        $socialnetwork  = isset( $instance['socialnetwork'] ) ? $instance['socialnetwork'] : '';
        ?>

<?php if( !empty($socialnetwork) ){ ?>
<ul class="social <?php if( wp_is_mobile() ){ echo 'phone'; } ?>">
    <?php foreach ($socialnetwork as $key => $socialnetwork_item) { ?>
    <li>
        <a href="<?php echo $socialnetwork_item['item_link']; ?>"
            class="<?php echo $socialnetwork_item['item_class'] ?>" target="_blank">
            <img src="<?php echo $socialnetwork_item['item_icon']; ?>" alt="">
        </a>
    </li>
    <?php } ?>
</ul>
<?php } ?>

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


        if ( isset( $instance[ 'socialnetwork' ] ) ) {
            $socialnetwork = $instance[ 'socialnetwork' ];
        } else {
            $socialnetwork = '';
        }

        $this->Mona_Widgets->create_field(
            [
                'type'   => 'repeater',
                'name'   => $this->get_field_name( 'socialnetwork' ),
                'id'     => $this->get_field_id( 'socialnetwork' ),
                'value'  => $socialnetwork,
                'title'  => __( 'Social Network', 'monamedia' ),
                'fields' => [
                    'item_icon' => [
                        'type'        => 'image',
                        'title'       => __( 'Icon', 'monamedia' ),
                    ],
                    'item_link' => [
                        'type'        => 'text',
                        'title'       => __( 'Link', 'monamedia' ),
                    ],
                    'item_class' => [
                        'type'        => 'text',
                        'title'       => __( 'Class', 'monamedia' ),
                    ]
                ],
                'docs'   => false,
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
        $instance['socialnetwork']    = $this->Mona_Widgets->update_field( $new_instance['socialnetwork'] );
        return $instance;

    }

}

/**
 * Undocumented function
 *
 * Register and load the widget
 * @return void
 */
function Register_Widget_topright() {
    register_widget( 'M_Widget_topright' );
}
add_action( 'widgets_init', 'Register_Widget_topright' );