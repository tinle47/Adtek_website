<?php
/**
 * Class Mona Custom Widget
 */
class Render_Field_Select {

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
            $widget_title = __( 'Select', 'monamedia' );
        }

        if ( isset ( $field_args['id'] ) ) {
            $for = 'for="'.$field_args['id'].'"';
        } else {
            $for = 'for="'.$field_args['name'].'"';
        }

        if ( isset ( $field_args['id'] ) ) {
            $id = 'id="'.$field_args['id'].'"';
        } else {
            $id = 'id="'.$field_args['name'].'"';
        }

        if ( isset ( $field_args['class'] ) ) {
            $class = 'class="mona-custom-widget ref-field-select '.esc_attr( $field_args['class'] ).'"';
        } else {
            $class = 'class="mona-custom-widget ref-field-select"';
        }

        if ( isset ( $field_args['name'] ) ) {
            $name = 'name="'.$field_args['name'].'"';
        } else {
            $name = 'name=""';
        }

        if ( isset( $field_args['value'] ) && ! empty ( $field_args['value'] ) ) {
            $value = esc_attr( $field_args['value'] );
        } else {
            $value = '';
        }

        $output .= '<div class="mona-widget-items render-field box-field-select">';
        $output .= '<div class="box-field-title">';
        $output .= '<label '.$for.' class="txt-label field-text-label">';
        $output .=  $widget_title;
        $output .= '</label>';
        $output .= '</div>';
        $output .= '<div class="box-field-content">';
        $output .= '<select '.$class.' '.$id.' '.$name.'>';
        if ( isset ( $field_args['placeholder'] ) ) {
            $output .= '<option>'.esc_attr( $field_args['placeholder'] ).'</option>';
        }
        if ( isset ( $field_args['select'] ) && ! empty ( $field_args['select'] ) ) {
            foreach ( $field_args['select'] as $key => $item ) {
                if ( sanitize_title( $value ) == sanitize_title( $key ) ) {
                    $output .= '<option value="'.esc_attr( $key ).'" selected>'.esc_attr( $item ).'</option>';
                } else {
                    $output .= '<option value="'.esc_attr( $key ).'">'.esc_attr( $item ).'</option>';
                }
            }
        }
        $output .= '</select>';
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
            if ( isset( $instance[ 'select' ] ) ) {
                $select = $instance[ 'select' ];
            } else {
                $select = '';
            }

            // Gọi hàm
            $this->Mona_Widgets->create_field(
                [
                    'type'         => 'select',
                    'name'         => $this->get_field_name( 'select' ),
                    'id'           => $this->get_field_id( 'select' ),
                    'value'        => $select,
                    'title'        => __( 'Select', 'monamedia' ),
                    'placeholder'  => __( 'Chọn giá trị', 'monamedia' ),
                    'select' => [
                        'select_1' => __( 'Giá trị 1', 'monamedia' ),
                        'select_2' => __( 'Giá trị 2', 'monamedia' ),
                        'select_3' => __( 'Giá trị 3', 'monamedia' ),
                    ],
                    'docs'         => false,
                ]
            );

            // Cập nhật
            $instance['select'] = $this->Mona_Widgets->update_field( $new_instance['select'] );
            </code>
        </pre>
        <?php
    }

}
