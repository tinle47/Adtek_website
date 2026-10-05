<?php
/**
 * Class Mona Custom Widget
 */
class Render_Field_Image {

    /**
     * Undocumented function
     *
     * @param array $field_args
     * @return void
     */
    public function render( $field_args = [] ) {

        $output = '';

        if ( isset ( $field_args['title'] ) ) {
            $widget_title = $field_args['title'];
        } else {
            $widget_title = __( 'Hình ảnh', 'monamedia' );
        }

        if ( isset ( $field_args['id'] ) ) {
            $for = 'for="'.$field_args['id'].'"';
        } else {
            $for = 'for="'.$field_args['name'].'"';
        }

        if ( ! empty ( $field_args['id'] ) ) {
            $id = 'id="'.$field_args['id'].'"';
        } else {
            $id = 'id="'.$field_args['name'].'"';
        }

        if ( isset ( $field_args['class'] ) ) {
            $class = 'class="mona-custom-widget ref-field-image '.esc_attr( $field_args['class'] ).'"';
        } else {
            $class = 'class="mona-custom-widget ref-field-image"';
        }

        if ( isset ( $field_args['name'] ) ) {
            $name = 'name="'.$field_args['name'].'"';
        } else {
            $name = 'name=""';
        }

        if ( isset( $field_args['value'] ) && ! empty ( $field_args['value'] ) ) {
            $value = 'value="'.$field_args['value'].'"';
        } else {
            $value = 'value=""';
        }

        if ( isset( $field_args['value'] ) && ! empty ( $field_args['value'] ) ) {
            $image_src = wp_get_attachment_image_url( $this->get_image_id_by_url( $field_args['value'] ), 'full' );
        } else {
            $image_src = '';
        }

        if ( isset( $field_args['placeholder'] ) ) {
            $placeholder = 'placeholder="'.esc_attr( $field_args['placeholder'] ).'"';
        } else {
            $placeholder = '';
        }

        if ( isset( $field_args['width'] ) ) {
            $width = esc_attr( $field_args['width'] );
        } else {
            $width = '325';
        }

        $output .= '<div class="mona-widget-items render-field box-field-image">';
        $output .= '<div class="box-field-title">';
        $output .= '<label '.$for.' class="txt-label field-text-label">';
        $output .=  $widget_title;
        $output .= '</label>';
        $output .= '</div>';
        $output .= '<div class="box-field-content">';
        $output .= '<input type="hidden" '.$class.' '.$id.' '.$name.' '.$value.' '.$placeholder.' />';
        $output .= '<img style="width:auto; height:auto; max-width:'.$width.'px;"" src="'.$image_src.'" class="w-image-review"/>';
        $output .= '<div class="box-image-button">';
        $output .= '<button class="upload_image_button button button-primary">'.__( 'Chọn ảnh', 'monamedia' ).'</button>';
        if ( ! empty ( $field_args['value'] ) ) {
            $output .= '<button class="remove_image_button button button-danger">'.__( 'Xóa ảnh', 'monamedia' ).'</button>';
        }
        $output .= '</div>';
        $output .= '</div>';
        $output .= '</div>';

        echo $output;

    }

    public function get_image_id_by_url( $image_url = '' ) {

        global $wpdb;

        if ( empty ( $image_url ) ) {
            return;
        }

        $attachment = $wpdb->get_col( $wpdb->prepare( "SELECT ID FROM $wpdb->posts WHERE guid='%s';", $image_url ) );

        if ( ! empty ( $attachment ) ) {

            return $attachment[0];

        } else {

            return false;

        }
    }

    /**
     * Undocumented function
     *
     * @return void
     */
    public function get_docs() {
        ?>
        <pre>
            <code>
            // Kiểm tra
            if ( isset( $instance[ 'image' ] ) ) {
                $image = $instance[ 'image' ];
            } else {
                $image = '';
            }

            // Gọi hàm
            $this->Mona_Widgets->create_field(
                [
                    'type'         => 'image',
                    'name'         => $this->get_field_name( 'image' ),
                    'id'           => $this->get_field_id( 'image' ),
                    'value'        => $image,
                    'title'        => __( 'Image', 'monamedia' ),
                    'placeholder'  => __( 'Chọn hình ảnh', 'monamedia' ),
                    'width'        => 325,
                    'docs'         => false,
                ]
            );

            // Cập nhật
            $instance['image'] = $this->Mona_Widgets->update_field( $new_instance['image'] );
            </code>
            </pre>
        <?php
    }

}
