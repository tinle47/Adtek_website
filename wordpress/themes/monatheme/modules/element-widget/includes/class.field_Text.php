<?php
/**
 * Class Mona Custom Widget
 */
class Render_Field_Text {

    /**
     * Undocumented function
     *
     * @param array $field_args
     * @return void
     */
    public function render( $field_args = [] ) {

        $output = '';

        if ( isset( $field_args['title'] ) ) {
            $widget_title = $field_args['title'];
        } else {
            $widget_title = __( 'Văn bản ngắn', 'monamedia' );
        }

        if ( isset( $field_args['id'] ) ) {
            $for = 'for="'.$field_args['id'].'"';
        } else {
            $for = 'for="'.$field_args['name'].'"';
        }

        if ( isset( $field_args['id'] ) ) {
            $id = 'id="'.$field_args['id'].'"';
        } else {
            $id = 'id="'.$field_args['name'].'"';
        }

        if ( isset( $field_args['class'] ) ) {
            $class = 'class="mona-custom-widget ref-field-text '.esc_attr( $field_args['class'] ).'"';
        } else {
            $class = 'class="mona-custom-widget ref-field-text"';
        }

        if ( isset( $field_args['name'] ) ) {
            $name = 'name="'.$field_args['name'].'"';
        } else {
            $name = '';
        }

        if ( isset( $field_args['value'] ) ) {
            $value = 'value="'.esc_attr( $field_args['value'] ).'"';
        } else {
            $value = 'value=""';
        }

        if ( isset( $field_args['placeholder'] ) ) {
            $placeholder = 'placeholder="'.esc_attr( $field_args['placeholder'] ).'"';
        } else {
            $placeholder = '';
        }

        $output .= '<div class="mona-widget-items render-field box-field-text">';
        $output .= '<div class="box-field-title">';
        $output .= '<label '.$for.' class="txt-label field-text-label">';
        $output .=  $widget_title;
        $output .= '</label>';
        $output .= '</div>';
        $output .= '<div class="box-field-content">';
        $output .= '<input type="text" '.$class.' '.$id.' '.$name.' '.$value.' '.$placeholder.' />';
        $output .= '</div>';
        $output .= '</div>';

        echo $output;
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
            if ( isset( $instance[ 'text' ] ) ) {
                $text = $instance[ 'text' ];
            } else {
                $text = '';
            }

            // Gọi hàm
            $this->Mona_Widgets->create_field(
                [
                    'type'        => 'text',
                    'name'        => $this->get_field_name( 'text' ),
                    'id'          => $this->get_field_id( 'text' ),
                    'value'       => $text,
                    'title'       => __( 'Text', 'monamedia' ),
                    'placeholder' => __( 'Nhập nội dung văn bản', 'monamedia' ),
                    'docs'        => false,
                ]
            );

            // Cập nhật
            $instance['text'] = $this->Mona_Widgets->update_field( $new_instance['text'] );
            </code>
            </pre>
        <?php
    }

}
