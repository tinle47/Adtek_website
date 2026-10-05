<?php
/**
 * Class Mona Custom Widget
 */
class Render_Field_Group {

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
            $widget_title = __( 'Group', 'monamedia' );
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

        $output .= '<div class="mona-widget-items render-field box-field-group">';
        $output .= '<div class="field-group-head">';
        $output .= '<label '.$for.' class="txt-label field-text-label">';
        $output .= $widget_title;
        $output .= '</label>';
        $output .= '</div>';
        /**
         * Start row clone
         */
        $output .= '<div class="field-group-contents">';
        foreach ( $field_args['fields'] as $key => $item ) {

            if ( isset ( $field_args['id'] ) ) {
                $id = 'id="'.$field_args['id'].'-'.$key.'"';
                $for = 'for="'.$field_args['id'].'-'.$key.'"';
            } else {
                $id = 'id="'.$field_args['name'].'-'.$key.'"';
                $for = 'for="'.$field_args['name'].'-'.$key.'"';
            }

            if ( isset ( $field_args['name'] ) ) {
                $name = 'name="'.$field_args['name'].'['.$key.']"';
            } else {
                $name = '';
            }

            if ( isset ( $item['column'] ) && $item['column'] == 1 ) {
                $style_clss = 'style="width: 100%;"';
            } elseif ( isset ( $item['column'] ) && $item['column'] == 2 ) {
                $style_clss = 'style="width: 50%;"';
            } elseif ( isset ( $item['column'] ) && $item['column'] == 3 ) {
                $style_clss = 'style="width: 33.3333%;"';
            } elseif ( isset ( $item['column'] ) && $item['column'] == 4 ) {
                $style_clss = 'style="width: 25%;"';
            } elseif ( isset ( $item['column'] ) && $item['column'] == 5 ) {
                $style_clss = 'style="width: 20%;"';
            } else {
                $style_clss = 'style="width: 25%;"';
            }

            if ( isset( $item['placeholder'] ) ) {
                $placeholder = 'placeholder="'.esc_attr( $item['placeholder'] ).'"';
            } else {
                $placeholder = '';
            }

            if ( $item['type'] == 'text' ) {

                if ( isset ( $item['title'] ) ) {
                    $item_title = $item['title'];
                } else {
                    $item_title = __( 'Văn bản ngắn', 'monamedia' );
                }

                if ( isset ( $field_args['class'] ) ) {
                    $class = 'class="mona-custom-widget ref-field-text '.esc_attr( $item['class'] ).'"';
                } else {
                    $class = 'class="mona-custom-widget ref-field-text"';
                }

                if ( isset ( $field_args['value'][$key] ) ) {
                    $value = 'value="'.esc_attr( $field_args['value'][$key] ).'"';
                } else {
                    $value = '';
                }

                $output .= '<div class="box-field-item render-item box-field-text">';
                $output .= '<div class="box-field-title">';
                $output .= '<label '.$for.' class="txt-label field-text-label">';
                $output .=  esc_attr( $item_title );
                $output .= '</label>';
                $output .= '</div>';
                $output .= '<div class="box-field-content">';
                $output .= '<input type="text" '.$class.' '.$id.' '.$name.' '.$value.' '.$placeholder.'/>';
                $output .= '</div>';
                $output .= '</div>';

            } elseif ( $item['type'] == 'textarea' ) {

                if ( isset ( $item['title'] ) ) {
                    $item_title = $item['title'];
                } else {
                    $item_title = __( 'Văn bản dài', 'monamedia' );
                }

                if ( isset ( $field_args['class'] ) ) {
                    $class = 'class="mona-custom-widget ref-field-textarea '.esc_attr( $item['class'] ).'"';
                } else {
                    $class = 'class="mona-custom-widget ref-field-textarea"';
                }

                if ( isset ( $item['rows'] ) ) {
                    $rows = 'rows="'.$item['rows'].'"';
                } else {
                    $rows = 'rows="5"';
                }

                if ( isset ( $item['cols'] ) ) {
                    $cols = 'cols="'.$item['cols'].'"';
                } else {
                    $cols = 'cols="10"';
                }

                if ( isset ( $field_args['value'][$key] ) ) {
                    $value = esc_attr( $field_args['value'][$key] );
                } else {
                    $value = '';
                }

                $output .= '<div class="box-field-item render-item box-field-textarea">';
                $output .= '<div class="box-field-title">';
                $output .= '<label '.$for.' class="txt-label field-text-label">';
                $output .=  esc_attr( $item_title );
                $output .= '</label>';
                $output .= '</div>';
                $output .= '<div class="box-field-content">';
                $output .= '<textarea '.$rows.' '.$cols.' '.$class.' '.$id.' '.$name.' '.$placeholder.'>'.$value.'</textarea>';
                $output .= '</div>';
                $output .= '</div>';

            } elseif ( $item['type'] == 'image' ) {

                if ( isset ( $item['title'] ) ) {
                    $item_title = $item['title'];
                } else {
                    $item_title = __( 'Hình ảnh', 'monamedia' );
                }

                if ( isset ( $field_args['class'] ) ) {
                    $class = 'class="mona-custom-widget ref-field-image '.esc_attr( $item['class'] ).'"';
                } else {
                    $class = 'class="mona-custom-widget ref-field-image"';
                }

                if ( isset( $item['width'] ) && ! empty ( $item['width'] ) ) {
                    $width = esc_attr( $item['width'] );
                } else {
                    $width = '325';
                }

                if ( isset ( $field_args['value'][$key] ) ) {
                    $value = 'value="'.esc_attr( $field_args['value'][$key] ).'"';
                } else {
                    $value = '';
                }

                if ( isset( $field_args['value'][$key] ) && ! empty ( $field_args['value'][$key] ) ) {
                    $image_src = wp_get_attachment_image_url( $this->get_image_id_by_url( $field_args['value'][$key] ), 'full' );
                } else {
                    $image_src = '';
                }

                $output .= '<div class="box-field-item render-item box-field-image">';
                $output .= '<div class="box-field-title">';
                $output .= '<label '.$for.' class="txt-label field-text-label">';
                $output .=  esc_attr( $item_title );
                $output .= '</label>';
                $output .= '</div>';
                $output .= '<div class="box-field-content">';
                $output .= '<input type="hidden" '.$class.' '.$id.' '.$name.' '.$value.' '.$placeholder.'/>';
                $output .= '<img style="width:auto; height:auto; max-width:'.$width.'px;" src="'.$image_src.'" class="w-image-review"/>';
                $output .= '<div class="box-image-button">';
                $output .= '<button class="upload_image_button button button-primary">'.__( 'Chọn ảnh', 'monamedia' ).'</button>';
                if ( ! empty ( $field_args['value'][$key] ) ) {
                    $output .= '<button class="remove_image_button button button-danger">'.__( 'Xóa ảnh', 'monamedia' ).'</button>';
                }
                $output .= '</div>';
                $output .= '</div>';
                $output .= '</div>';

            } elseif ( $item['type'] == 'select' ) {

                if ( isset ( $field_args['class'] ) ) {
                    $class = 'class="mona-custom-widget ref-field-select '.esc_attr( $item['class'] ).'"';
                } else {
                    $class = 'class="mona-custom-widget ref-field-select"';
                }

                if ( isset ( $item['title'] ) ) {
                    $item_title = $item['title'];
                } else {
                    $item_title = __( 'Select', 'monamedia' );
                }

                if ( isset( $field_args['value'][$key] ) && ! empty ( $field_args['value'][$key] ) ) {
                    $value = esc_attr( $field_args['value'][$key] );
                } else {
                    $value = '';
                }

                $output .= '<div class="box-field-item render-field box-field-select">';
                $output .= '<div class="box-field-title">';
                $output .= '<label '.$for.' class="txt-label field-text-label">';
                $output .=  esc_attr( $item_title );
                $output .= '</label>';
                $output .= '</div>';
                $output .= '<div class="box-field-content">';
                $output .= '<select '.$class.' '.$id.' '.$name.'>';
                if ( isset ( $item['placeholder'] ) ) {
                    $output .= '<option selected>'.esc_attr( $item['placeholder'] ).'</option>';
                }
                if ( isset ( $item['select'] ) && is_array( $item['select'] ) ) {
                    foreach ( $item['select'] as $options => $option ) {
                        if ( sanitize_title( $value ) == sanitize_title( $options ) ) {
                            $output .= '<option value="'.esc_attr( $options ).'" selected>'.esc_attr( $option ).'</option>';
                        } else {
                            $output .= '<option value="'.esc_attr( $options ).'">'.esc_attr( $option ).'</option>';
                        }
                    }
                }
                $output .= '</select>';
                $output .= '</div>';
                $output .= '</div>';

            } elseif ( $item['type'] == 'radio' ) {

                if ( isset ( $item['title'] ) ) {
                    $item_title = $item['title'];
                } else {
                    $item_title = __( 'Radio', 'monamedia' );
                }

                if ( isset ( $field_args['class'] ) ) {
                    $class = 'class="mona-custom-widget ref-field-radio '.esc_attr( $item['class'] ).'"';
                } else {
                    $class = 'class="mona-custom-widget ref-field-radio"';
                }

                if ( isset( $field_args['value'][$key] ) && ! empty ( $field_args['value'][$key] ) ) {
                    $checked = esc_attr( $field_args['value'][$key] );
                } else {
                    $checked = '';
                }

                $output .= '<div class="box-field-item render-field box-field-radio">';
                $output .= '<div class="box-field-title">';
                $output .= '<label '.$for.' class="txt-label field-text-label">';
                $output .=  esc_attr( $item_title );
                $output .= '</label>';
                $output .= '</div>';
                $output .= '<div class="box-field-content">';
                if ( isset ( $item['radio'] ) && is_array( $item['radio'] ) ) {
                    foreach ( $item['radio'] as $radio => $value ) {

                        if ( isset ( $field_args['id'] ) ) {
                            $for = $field_args['id'].'-'.$key.'-'.sanitize_title( $value );
                        } else {
                            $for = $field_args['name'].'-'.$key.'-'.sanitize_title( $value );
                        }

                        $output .= '<div class="field-radio-item" '.$style_clss.'>';
                        $output .= '<div class="radio-text">';
                        $output .= '<label for="'.$for.'" class="txt-label item-text-label"></label>';
                        if ( ! empty ( $checked ) && sanitize_title( $checked ) == sanitize_title( $radio ) ) {
                            $output .= '<input type="radio" '.$class.' id="'.$for.'" '.$name.' value="'.esc_attr( $radio ).'" '.$placeholder.' checked="checked" />';
                        } else {
                            $output .= '<input type="radio" '.$class.' id="'.$for.'" '.$name.' value="'.esc_attr( $radio ).'" '.$placeholder.' />';
                        }
                        $output .= '<span class="radio-txt">'.esc_attr( $value ).'</span>';
                        $output .= '</div>';
                        $output .= '</div>';
                    }
                }
                $output .= '</div>';
                $output .= '</div>';

            } elseif ( $item['type'] == 'checkbox' ) {

                if ( isset ( $item['title'] ) ) {
                    $item_title = $item['title'];
                } else {
                    $item_title = __( 'Checkbox', 'monamedia' );
                }

                if ( isset ( $field_args['class'] ) ) {
                    $class = 'class="mona-custom-widget ref-field-checkbox '.esc_attr( $item['class'] ).'"';
                } else {
                    $class = 'class="mona-custom-widget ref-field-checkbox"';
                }

                if ( isset( $field_args['value'][$key] ) && ! empty ( $field_args['value'][$key] ) ) {
                    $checkboxs = $field_args['value'][$key];
                } else {
                    $checkboxs = '';
                }

                $output .= '<div class="box-field-item render-field box-field-checkbox">';
                $output .= '<div class="box-field-title">';
                $output .= '<label '.$for.' class="txt-label field-text-label">';
                $output .=  esc_attr( $item_title );
                $output .= '</label>';
                $output .= '</div>';
                $output .= '<div class="box-field-content">';
                if ( isset ( $item['checkbox'] ) && is_array( $item['checkbox'] ) ) {
                    foreach ( $item['checkbox'] as $checkbox => $value ) {

                        if ( isset ( $field_args['id'] ) ) {
                            $for = $field_args['id'].'-'.$key.'-'.sanitize_title( $value );
                        } else {
                            $for = $field_args['name'].'-'.$key.'-'.sanitize_title( $value );
                        }

                        $checkbox_name = 'name="'.$field_args['name'].'['.$key.']['.$checkbox.']"';

                        $output .= '<div class="field-checkbox-item" '.$style_clss.'>';
                        $output .= '<div class="checkbox-text">';
                        $output .= '<label for="'.$for.'" class="txt-label item-text-label"></label>';
                        if ( ! empty ( $checkboxs ) && $this->is_checked( $checkbox, $checkboxs ) ) {
                            $output .= '<input type="checkbox" '.$class.' id="'.$for.'" '.$checkbox_name.' value="'.esc_attr( $checkbox ).'" '.$placeholder.' checked="checked" />';
                        } else {
                            $output .= '<input type="checkbox" '.$class.' id="'.$for.'" '.$checkbox_name.' value="'.esc_attr( $checkbox ).'" '.$placeholder.' />';
                        }
                        $output .= '<span class="radio-txt">'.esc_attr( $value ).'</span>';
                        $output .= '</div>';
                        $output .= '</div>';
                    }
                }
                $output .= '</div>';
                $output .= '</div>';

            } elseif ( $item['type'] == 'gallery' ) {

                if ( isset ( $item['title'] ) ) {
                    $item_title = $item['title'];
                } else {
                    $item_title = __( 'Gallery', 'monamedia' );
                }

                if ( isset ( $item['class'] ) ) {
                    $gallery_class = 'mona-custom-widget ref-field-gallery '.$item['class'].'';
                } else {
                    $gallery_class = 'mona-custom-widget ref-field-gallery';
                }

                if ( isset ( $item['id'] ) ) {
                    $gallery_id = $item['id'].'-'.$key.'';
                } else {
                    $gallery_id = $field_args['name'].'-'.$key.'';
                }

                $gallery_name = $field_args['name'].'['.$key.']';

                $gallery_value = '';

                if ( isset( $item['placeholder'] ) && ! empty ( $item['placeholder'] ) ) {
                    $gallery_placeholder = esc_attr( $item['placeholder'] );
                } else {
                    $gallery_placeholder = '';
                }

                if ( isset( $item['width'] ) && ! empty ( $item['width'] ) ) {
                    $gallery_width = esc_attr( $item['width'] );
                } else {
                    $gallery_width = '100';
                }

                $output .= '<div class="box-field-item render-item box-field-gallery">';
                $output .= '<div class="box-field-title">';
                $output .= '<label '.$for.' class="txt-label field-text-label">';
                $output .=  esc_attr( $item_title );
                $output .= '</label>';
                $output .= '</div>';
                $output .= '<div class="box-field-content">';
                $output .= '<div id="get_result_gallery" data-gallery_class="'.$gallery_class.'" data-gallery_id="'.$gallery_id.'" data-gallery_name="'.$gallery_name.'" data-gallery_placeholder="'.$gallery_placeholder.'" data-gallery_width="'.$gallery_width.'"></div>';
                $output .= '<div class="render-gallery-images">';
                if ( isset ( $field_args['value'][$key] ) && is_array ( $field_args['value'][$key] ) ) {
                    $image_stt = 0;
                    foreach ( $field_args['value'][$key] as $gallery => $value ) {
                        $output .= '<div class="gallery-column">';
                        $output .= '<div class="preview-image-item">';
                        $output .= '<img style="width: '.$gallery_width.'px; max-width: '.$gallery_width.'px; height:auto" class="'.$gallery_class.'" id="'.$gallery_id.'-'.$image_stt.'" src="'.esc_url( $value ).'" />';
                        $output .= '<input type="hidden" id="'.$gallery_id.'-'.$image_stt.'" name="'.$gallery_name.'['.$image_stt.']" value="'.esc_url( $value ).'" placeholder="'.$gallery_placeholder.'"/>';
                        $output .= '<div class="preview-image-action">';
                        $output .= '<a href="javascript:;" class="act-remove-image">'.__( 'Xóa', 'monamedia' ).'</a>';
                        $output .= '</div>';
                        $output .= '</div>';
                        $output .= '</div>';
                        $image_stt++;
                    }
                }
                $output .=  '</div>';
                $output .= '<div class="box-gallery-button">';
                $output .= '<button class="upload_gallery_button button button-primary">'.__( 'Chọn ảnh', 'monamedia' ).'</button>';
                $output .= '</div>';
                $output .= '</div>';
                $output .= '<script>
                jQuery(document).ready(function($) {
                    WidgetMakeUlSortGallery = function () {
                        $(".render-gallery-images").sortable({
                            items: ".gallery-column:not(.sprite-add)",
                            opacity: .7,
                            scroll: true,
                            stop: function(event, ui){
                                $(".render-gallery-images").closest(".widget").find("input.widget-control-save").prop("disabled", false);
                                $(".render-gallery-images .gallery-column").each(function(i = 0, el){
                                $(el).attr("data-id",$(el).index()+1-1);
                            });
                        }});
                        $(".render-gallery-images").disableSelection();
                    };
                    WidgetMakeUlSortGallery();
                });
                </script>';
                $output .= '</div>';

            }

        }
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
            if ( isset( $instance[ 'group' ] ) ) {
                $group = $instance[ 'group' ];
            } else {
                $group = '';
            }

            // Gọi hàm
            $this->Mona_Widgets->create_field(
                [
                    'type'   => 'group',
                    'name'   => $this->get_field_name( 'group' ),
                    'id'     => $this->get_field_id( 'group' ),
                    'value'  => $group,
                    'title'  => __( 'Group', 'monamedia' ),
                    'fields' => [
                        'item_text' => [
                            'type'        => 'text',
                            'title'       => __( 'Text', 'monamedia' ),
                            'placeholder' => __( 'Nhập nội dung văn bản', 'monamedia' ),
                        ]
                    ],
                    'docs'   => false,
                ]
            );

            // Cập nhật
            $instance['group'] = $this->Mona_Widgets->update_field( $new_instance['group'] );
            </code>
        </pre>
        <?php
    }

}
