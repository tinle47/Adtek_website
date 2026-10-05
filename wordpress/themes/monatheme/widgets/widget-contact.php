<?php
/**
 * Undocumented class
 * Create widget
 */
class M_Widget_contacts extends WP_Widget {

    public $Mona_Widgets;

    /**
     * Undocumented function
     */
    function __construct() {

        parent::__construct(
            'm_contact',
            __('Mona - Contact', 'monamedia'),
            [
                'description' => __( 'Display contact information', 'monamedia' ),
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
        $title   = isset( $instance['title'] ) ? $instance['title'] : '';
        $contact_information = isset( $instance['contact_information'] ) ? $instance['contact_information'] : '';
        ?>

<div class="menu-title"><?php echo $title; ?></div>
<ul class="menu-list widget-contact">
    <?php 
    foreach ($contact_information as $key => $contact_information_item) { 
        ?>
    <li class="menu-item">
        <?php    
        if( $contact_information_item['item_select'] == 'value_text'){
            echo '<p>';
            echo '<img src="'.$contact_information_item['item_icon'].'" alt="">';
            echo '<span>'.$contact_information_item['item_information'].'</span></p>';
            
        }elseif ($contact_information_item['item_select'] == 'value_email') {
            echo '<a href="mailto:'.$contact_information_item['item_information'].'">';
            echo '<img src="'.$contact_information_item['item_icon'].'" alt="">';
            echo '<span>'.$contact_information_item['item_information'].'</span></a>';

        }elseif ($contact_information_item['item_select'] == 'value_tel') {
            echo '<a href="'.mona_replace_tel($contact_information_item['item_information']).'">';
            echo '<img src="'.$contact_information_item['item_icon'].'" alt="">';
            echo '<span>'.$contact_information_item['item_information'].'</span></a>';

        }elseif ($contact_information_item['item_select'] == 'value_link') {
            echo '<a href="'.$contact_information_item['item_information'].'" target="_blank">';
            echo '<img src="'.$contact_information_item['item_icon'].'" alt="">';
            echo $contact_information_item['item_information'].'</a>';
        }
    ?>
    </li>
    <?php } ?>
</ul>

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
                'title'       => __( 'Title', 'monamedia' ),
                'placeholder' => __( 'Nhập nội dung văn bản', 'monamedia' ),
                'docs'        => false,
            ]
        );

        if ( isset( $instance[ 'contact_information' ] ) ) {
            $contact_information = $instance[ 'contact_information' ];
        } else {
            $contact_information = '';
        }

        $this->Mona_Widgets->create_field(
            [
                'type'   => 'repeater',
                'name'   => $this->get_field_name( 'contact_information' ),
                'id'     => $this->get_field_id( 'contact_information' ),
                'value'  => $contact_information,
                'title'  => __( 'Social Network', 'monamedia' ),
                'fields' => [
                    'item_icon' => [
                        'type'              => 'image',
                        'title'             => __( 'Icon', 'monamedia' ),
                    ],
                    'item_information'      => [
                        'type'              => 'text',
                        'title'             => __( 'Information', 'monamedia' ),
                    ],
                    'item_select'           => [
                        'type'              => 'select',
                        'title'             => __( 'Type', 'monamedia' ),
                        'placeholder'       => __( 'Select Information Type', 'monamedia' ),
                        'select' => [
                            'value_text'    => __( 'Text', 'monamedia' ),
                            'value_email'   => __( 'Email', 'monamedia' ),
                            'value_tel'     => __( 'Tel', 'monamedia' ),
                            'value_link'    => __( 'Link', 'monamedia' ),
                        ],
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

        $instance['title']    = $this->Mona_Widgets->update_field( $new_instance['title'] );
        $instance['contact_information']  = $this->Mona_Widgets->update_field( $new_instance['contact_information'] );

        return $instance;

    }

}

/**
 * Undocumented function
 *
 * Register and load the widget
 * @return void
 */
function Register_Widget_contacts() {
    register_widget( 'M_Widget_contacts' );
}
add_action( 'widgets_init', 'Register_Widget_contacts' );