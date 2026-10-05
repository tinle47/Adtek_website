<?php
/**
 * Class Mona Custom Widget
 */
class Render_Field_Checkbox {

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
            $widget_title = __( 'Checkbox', 'monamedia' );
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
            $class = 'class="mona-custom-widget ref-field-checkbox '.$field_args['class'].'"';
        } else {
            $class = 'class="mona-custom-widget ref-field-checkbox"';
        }

        if ( isset( $field_args['value'] ) && ! empty ( $field_args['value'] ) ) {
            $checkbox = $field_args['value'];
        } else {
            $checkbox = '';
        }

        if ( isset( $field_args['placeholder'] ) ) {
            $placeholder = 'placeholder="'.esc_attr( $field_args['placeholder'] ).'"';
        } else {
            $placeholder = '';
        }

        if ( isset ( $field_args['column'] ) && $field_args['column'] == 1 ) {
            $style_clss = 'style="width: 100%;"';
        } elseif ( isset ( $field_args['column'] ) && $field_args['column'] == 2 ) {
            $style_clss = 'style="width: 50%;"';
        } elseif ( isset ( $field_args['column'] ) && $field_args['column'] == 3 ) {
            $style_clss = 'style="width: 33.3333%;"';
        } elseif ( isset ( $field_args['column'] ) && $field_args['column'] == 4 ) {
            $style_clss = 'style="width: 25%;"';
        } elseif ( isset ( $field_args['column'] ) && $field_args['column'] == 5 ) {
            $style_clss = 'style="width: 20%;"';
        } else {
            $style_clss = 'style="width: 25%;"';
        }

        $output .= '<div class="mona-widget-items render-field box-field-checkbox">';
        $output .= '<div class="box-field-title">';
        $output .= '<label '.$for.' class="txt-label field-text-label">';
        $output .=  $widget_title;
        $output .= '</label>';
        $output .= '</div>';
        $output .= '<div class="box-field-content">';
        if ( isset ( $field_args['checkbox'] ) && ! empty ( $field_args['checkbox'] ) ) {
            foreach ( $field_args['checkbox'] as $key => $item ) {

                if ( isset ( $field_args['id'] ) ) {
                    $for = $field_args['id'].'-'.sanitize_title( $item );
                } else {
                    $for = $field_args['name'].'-'.sanitize_title( $item );
                }

                $name = 'name="'.$field_args['name'].'['.$key.']"';

                $output .= '<div class="field-checkbox-item" '.$style_clss.'>';
                $output .= '<div class="checkbox-text">';
                if ( ! empty ( $checkbox ) && $this->is_checked( $key, $checkbox ) ) {
                    $output .= '<input type="checkbox" '.$class.' id="'.$for.'" '.$name.' value="'.esc_attr( $key ).'" '.$placeholder.' checked="checked" />';
                } else {
                    $output .= '<input type="checkbox" '.$class.' id="'.$for.'" '.$name.' value="'.esc_attr( $key ).'" '.$placeholder.' />';
                }
                $output .= '<label for="'.$for.'" class="txt-label item-text-label">'.esc_attr( $item ).'</label>';
                $output .= '</div>';
                $output .= '</div>';
            }
        }
        $output .= '</div>';
        $output .= '</div>';

        echo $output;

    }

    /**
     * Undocumented function
     *
     * @param string $value
     * @param array $args_checkbox
     * @return boolean
     */
    public function is_checked( $value = '', $args_checkbox = [] ) {
        $check = false;
        if ( empty( $value ) || empty( $args_checkbox ) ) {
            $check = false;
            return $check;
        }
        if ( is_array( $args_checkbox ) ) {
            foreach ( $args_checkbox as $key => $item ) {
                if ( sanitize_title( $value ) == sanitize_title( $item ) ) {
                    $check = true;
                    return $check;
                }
            }
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
            if ( isset( $instance[ 'checkbox' ] ) ) {
                $checkbox = $instance[ 'checkbox' ];
            } else {
                $checkbox = '';
            }

            // Gọi hàm
            $this->Mona_Widgets->create_field(
                [
                    'type'         => 'checkbox',
                    'name'         => $this->get_field_name( 'checkbox' ),
                    'id'           => $this->get_field_id( 'checkbox' ),
                    'value'        => $checkbox,
                    'title'        => __( 'Checkbox', 'monamedia' ),
                    'placeholder'  => __( 'Chọn giá trị', 'monamedia' ),
                    'checkbox' => [
                        'checkbox_1'  => __( 'Giá trị 1', 'monamedia' ),
                        'checkbox_2'  => __( 'Giá trị 2', 'monamedia' ),
                        'checkbox_3'  => __( 'Giá trị 3', 'monamedia' ),
                    ],
                    'column'       => 4, // max 5
                    'docs'         => false,
                ]
            );

            // Cập nhật
            $instance['checkbox'] = $this->Mona_Widgets->update_field( $new_instance['checkbox'] );
            </code>
        </pre>
        <?php
    }

}
