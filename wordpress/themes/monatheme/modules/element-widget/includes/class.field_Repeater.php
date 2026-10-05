<?php
/**
 * Class Mona Custom Widget
 */
class Render_Field_Repeater {

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
            $widget_title = __( 'Repeater', 'monamedia' );
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

        $output .= '<div class="mona-widget-items render-field box-field-repeater repeaters">';
        $output .= '<div class="field-repeater-head">';
        $output .= '<label '.$for.' class="txt-label field-text-label">';
        $output .= $widget_title;
        $output .= '</label>';
        $output .= '</div>';
        /**
         * Start row clone
         */
        $output .= '<div class="field-row-repeater rowCloneindex" data-row_id="rowCloneindex" data-repeatable>';
        $output .= '<div class="box-row-head handle">';
        $output .= '<span>'.__( 'rowCloneindex', 'monamedia' ).'</span>';
        $output .= '</div>';
        $output .= '<div class="box-row-repeaters">';
        foreach ( $field_args['fields'] as $key => $item ) {

            if ( isset ( $field_args['id'] ) ) {
                $id = 'id="'.$field_args['id'].'-rowCloneindex-'.$key.'"';
                $for = 'for="'.$field_args['id'].'-rowCloneindex-'.$key.'"';
            } else {
                $id = 'id="'.$field_args['name'].'-rowCloneindex-'.$key.'"';
                $for = 'for="'.$field_args['name'].'-rowCloneindex-'.$key.'"';
            }

            if ( isset ( $field_args['name'] ) ) {
                $name = 'name="'.$field_args['name'].'[rowCloneindex]['.$key.']"';
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

                if ( isset ( $item['class'] ) ) {
                    $class = 'class="mona-custom-widget ref-field-text '.esc_attr( $item['class'] ).'"';
                } else {
                    $class = 'class="mona-custom-widget ref-field-text"';
                }

                $output .= '<div class="box-field-item render-item box-field-text">';
                $output .= '<div class="box-field-title">';
                $output .= '<label '.$for.' class="txt-label field-text-label">';
                $output .=  esc_attr( $item_title );
                $output .= '</label>';
                $output .= '</div>';
                $output .= '<div class="box-field-content">';
                $output .= '<input type="text" '.$class.' '.$id.' '.$name.' '.$placeholder.'/>';
                $output .= '</div>';
                $output .= '</div>';

            } elseif ( $item['type'] == 'textarea' ) {

                if ( isset ( $item['title'] ) ) {
                    $item_title = $item['title'];
                } else {
                    $item_title = __( 'Văn bản dài', 'monamedia' );
                }

                if ( isset ( $item['class'] ) ) {
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

                $output .= '<div class="box-field-item render-item box-field-textarea">';
                $output .= '<div class="box-field-title">';
                $output .= '<label '.$for.' class="txt-label field-text-label">';
                $output .=  esc_attr( $item_title );
                $output .= '</label>';
                $output .= '</div>';
                $output .= '<div class="box-field-content">';
                $output .= '<textarea '.$rows.' '.$cols.' '.$class.' '.$id.' '.$name.' '.$placeholder.'></textarea>';
                $output .= '</div>';
                $output .= '</div>';

            } elseif ( $item['type'] == 'image' ) {

                if ( isset ( $item['title'] ) ) {
                    $item_title = $item['title'];
                } else {
                    $item_title = __( 'Hình ảnh', 'monamedia' );
                }

                if ( isset ( $item['class'] ) ) {
                    $class = 'class="mona-custom-widget ref-field-image '.esc_attr( $item['class'] ).'"';
                } else {
                    $class = 'class="mona-custom-widget ref-field-image"';
                }

                $image_src = '';

                if ( isset( $item['width'] ) && ! empty ( $item['width'] ) ) {
                    $width = esc_attr( $item['width'] );
                } else {
                    $width = '325';
                }

                $output .= '<div class="box-field-item render-item box-field-image">';
                $output .= '<div class="box-field-title">';
                $output .= '<label '.$for.' class="txt-label field-text-label">';
                $output .=  esc_attr( $item_title );
                $output .= '</label>';
                $output .= '</div>';
                $output .= '<div class="box-field-content">';
                $output .= '<input type="hidden" '.$class.' '.$id.' '.$name.' '.$placeholder.'/>';
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

                if ( isset ( $item['title'] ) ) {
                    $item_title = $item['title'];
                } else {
                    $item_title = __( 'Select', 'monamedia' );
                }

                if ( isset ( $item['class'] ) ) {
                    $class = 'class="mona-custom-widget ref-field-select '.esc_attr( $item['class'] ).'"';
                } else {
                    $class = 'class="mona-custom-widget ref-field-select"';
                }

                $output .= '<div class="box-field-item render-item box-field-select">';
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
                        $output .= '<option value="'.esc_attr( $options ).'">'.esc_attr( $option ).'</option>';
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

                if ( isset ( $item['class'] ) ) {
                    $class = 'class="mona-custom-widget ref-field-radio '.esc_attr( $item['class'] ).'"';
                } else {
                    $class = 'class="mona-custom-widget ref-field-radio"';
                }

                $output .= '<div class="box-field-item render-item box-field-radio">';
                $output .= '<div class="box-field-title">';
                $output .= '<label '.$for.' class="txt-label field-text-label">';
                $output .=  esc_attr( $item_title );
                $output .= '</label>';
                $output .= '</div>';
                $output .= '<div class="box-field-content">';
                if ( isset ( $item['radio'] ) && is_array( $item['radio'] ) ) {
                    foreach ( $item['radio'] as $radio => $value ) {

                        $for = $field_args['name'].'-rowCloneindex'.'-'.$key.'-'.sanitize_title( $value );

                        $output .= '<div class="field-radio-item" '.$style_clss.'>';
                        $output .= '<div class="radio-text">';
                        $output .= '<label for="'.$for.'" class="txt-label item-text-label"></label>';
                        $output .= '<input type="radio" '.$class.' id="'.$for.'" '.$name.' value="'.esc_attr( $radio ).'" '.$placeholder.' />';
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

                if ( isset ( $item['class'] ) ) {
                    $class = 'class="mona-custom-widget ref-field-checkbox '.esc_attr( $item['class'] ).'"';
                } else {
                    $class = 'class="mona-custom-widget ref-field-checkbox"';
                }

                $output .= '<div class="box-field-item render-item box-field-checkbox">';
                $output .= '<div class="box-field-title">';
                $output .= '<label '.$for.' class="txt-label field-text-label">';
                $output .=  esc_attr( $item_title );
                $output .= '</label>';
                $output .= '</div>';
                $output .= '<div class="box-field-content">';
                if ( isset ( $item['checkbox'] ) && is_array( $item['checkbox'] ) ) {
                    foreach ( $item['checkbox'] as $checkbox => $value ) {

                        $for = $field_args['name'].'-rowCloneindex'.'-'.$key.'-'.sanitize_title( $value );

                        $checkbox_name = 'name="'.$field_args['name'].'[rowCloneindex]['.$key.']['.$checkbox.']"';

                        $output .= '<div class="field-checkbox-item" '.$style_clss.'>';
                        $output .= '<div class="checkbox-text">';
                        $output .= '<label for="'.$for.'" class="txt-label item-text-label"></label>';
                        $output .= '<input type="checkbox" '.$class.' id="'.$for.'" '.$checkbox_name.' value="'.esc_attr( $checkbox ).'" '.$placeholder.' />';
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
                    $gallery_class = 'class="mona-custom-widget ref-field-gallery '.esc_attr( $item['class'] ).'"';
                } else {
                    $gallery_class = 'class="mona-custom-widget ref-field-gallery"';
                }

                if ( isset ( $item['id'] ) ) {
                    $gallery_id = $item['id'].'-rowCloneindex-'.$key.'';
                } else {
                    $gallery_id = $field_args['name'].'-rowCloneindex-'.$key.'';
                }

                $gallery_name = $field_args['name'].'[rowCloneindex]['.$key.']';

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
                $output .= '<div class="render-gallery-images"></div>';
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
        $output .= '<div class="box-row-action box-repeater-button button-remove">';
        $output .= '<button class="remove_row_button button button-danger">'.__( 'Xóa dòng', 'monamedia' ).'</button>';
        $output .= '</div>';
        $output .= '</div>';
        $output .= '</div>';
        /**
         * End row clone
         */
        /**
         * Kiểm tra dữ liệu đầu vào -> $field_args['value']
         * Nếu có tòn tại mãng dữ liệu
         * - Chạy vòng lặp mãng và lấy dữ liệu render ra mã html
         * - So sánh khóa dữ liệu và kiểm tra hiển thị đúng kiểu dữ liệu -> $field_args['fields']
         * - Tạo các id, name, value,...vvv dựa trên khóa dữ liệu
         */
        $row = 0;
        if ( is_array( $field_args['value'] ) ) {
            foreach ( $field_args['value'] as $key => $fields ) {
                $output .= '<div class="field-row-repeater" data-row_id="'.$row.'" data-repeatable>';
                $output .= '<div class="box-row-head handle">';
                $output .= '<span>'.( $row + 1 ).'</span>';
                $output .= '</div>';
                $output .= '<div class="box-row-repeaters">';
                if ( isset ( $fields ) && ! empty ( $fields ) ) {
                    foreach ( $field_args['fields'] as $k => $field ) {

                        if ( isset ( $field_args['id'] ) ) {
                            $id  = 'id="'.$field_args['id'].'-row-'.$row.'-'.$k.'"';
                            $for = 'for="'.$field_args['id'].'-row-'.$row.'-'.$k.'"';
                        } else {
                            $id  = 'id="'.$field_args['name'].'-row-'.$row.'-'.$k.'"';
                            $for = 'for="'.$field_args['name'].'-row-'.$row.'-'.$k.'"';
                        }

                        $name = 'name="'.$field_args['name'].'[row-'.$row.']['.$k.']"';

                        if ( isset( $field_args['fields'][$k]['placeholder'] ) && ! empty ( $field_args['fields'][$k]['placeholder'] ) ) {
                            $placeholder = 'placeholder="'.esc_attr( $field_args['fields'][$k]['placeholder'] ).'"';
                        } else {
                            $placeholder = '';
                        }

                        if ( $field_args['fields'][$k]['type'] == 'text' ) {

                            if ( isset ( $field_args['fields'][$k]['title'] ) ) {
                                $item_title = $field_args['fields'][$k]['title'];
                            } else {
                                $item_title = __( 'Văn bản ngắn', 'monamedia' );
                            }

                            if ( isset ( $field_args['fields'][$k]['class'] ) ) {
                                $class = 'class="mona-custom-widget ref-field-text '.$field_args['fields'][$k]['class'].'"';
                            } else {
                                $class = 'class="mona-custom-widget ref-field-text"';
                            }

                            if ( ! empty ( $field_args['value'][$key][$k] ) ) {
                                $value = 'value="'.esc_attr( $field_args['value'][$key][$k] ).'"';
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

                        } elseif ( $field_args['fields'][$k]['type'] == 'textarea' ) {

                            if ( isset ( $field_args['fields'][$k]['title'] ) ) {
                                $item_title = $field_args['fields'][$k]['title'];
                            } else {
                                $item_title = __( 'Văn bản dài', 'monamedia' );
                            }

                            if ( isset ( $field_args['fields'][$k]['class'] ) ) {
                                $class = 'class="mona-custom-widget ref-field-textarea '.$field_args['fields'][$k]['class'].'"';
                            } else {
                                $class = 'class="mona-custom-widget ref-field-textarea"';
                            }

                            if ( ! empty ( $field_args['fields'][$k]['rows'] ) ) {
                                $rows = 'rows="'.$field_args['fields'][$k]['rows'].'"';
                            } else {
                                $rows = 'rows="5"';
                            }

                            if ( ! empty ( $field_args['fields'][$k]['cols'] ) ) {
                                $cols = 'cols="'.$field_args['fields'][$k]['cols'].'"';
                            } else {
                                $cols = 'cols="10"';
                            }

                            if ( ! empty ( $field_args['value'][$key][$k] ) ) {

                                if ( ! empty ( $field_args['fields'][$k]['str_text'] ) && $field_args['fields'][$k]['str_text'] == false ) {
                                    $value = $field_args['value'][$key][$k];
                                } else {
                                    $value = esc_attr( $field_args['value'][$key][$k] );
                                }

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

                        } elseif ( $field_args['fields'][$k]['type'] == 'image' ) {

                            if ( isset ( $field_args['fields'][$k]['title'] ) ) {
                                $item_title = $field_args['fields'][$k]['title'];
                            } else {
                                $item_title = __( 'Hình ảnh', 'monamedia' );
                            }

                            if ( isset ( $field_args['fields'][$k]['class'] ) ) {
                                $class = 'class="mona-custom-widget ref-field-image '.$field_args['fields'][$k]['class'].'"';
                            } else {
                                $class = 'class="mona-custom-widget ref-field-image"';
                            }

                            if ( ! empty ( $field_args['value'][$key][$k] ) ) {
                                $image_src = wp_get_attachment_image_url( mona_get_mod_image_id( $field_args['value'][$key][$k] ), 'full' );
                            } else {
                                $image_src = '';
                            }

                            if ( ! empty ( $field_args['value'][$key][$k] ) ) {
                                $value = 'value="'.esc_url( $field_args['value'][$key][$k] ).'"';
                            } else {
                                $value = '';
                            }

                            if ( isset( $field_args['fields'][$k]['width'] ) && ! empty ( $field_args['fields'][$k]['width'] ) ) {
                                $width = esc_attr( $field_args['fields'][$k]['width'] );
                            } else {
                                $width = '325';
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
                            if ( ! empty ( $field_args['value'][$key][$k] ) ) {
                                $output .= '<button class="remove_image_button button button-danger">'.__( 'Xóa ảnh', 'monamedia' ).'</button>';
                            }
                            $output .= '</div>';
                            $output .= '</div>';
                            $output .= '</div>';

                        } elseif ( $field_args['fields'][$k]['type'] == 'select' ) {

                            if ( isset ( $field_args['fields'][$k]['title'] ) ) {
                                $item_title = $field_args['fields'][$k]['title'];
                            } else {
                                $item_title = __( 'Select', 'monamedia' );
                            }

                            if ( isset ( $field_args['fields'][$k]['class'] ) ) {
                                $class = 'class="mona-custom-widget ref-field-select '.$field_args['fields'][$k]['class'].'"';
                            } else {
                                $class = 'class="mona-custom-widget ref-field-select"';
                            }

                            if ( ! empty ( $field_args['value'][$key][$k] ) ) {
                                $selected = $field_args['value'][$key][$k];
                            } else {
                                $selected = '';

                            }

                            $output .= '<div class="box-field-item render-item box-field-select">';
                            $output .= '<div class="box-field-title">';
                            $output .= '<label '.$for.' class="txt-label field-text-label">';
                            $output .=  esc_attr( $item_title );
                            $output .= '</label>';
                            $output .= '</div>';
                            $output .= '<div class="box-field-content">';
                            $output .= '<select '.$class.' '.$id.' '.$name.'>';
                            if ( ! empty ( $field_args['fields'][$k]['placeholder'] ) ) {
                                $output .= '<option selected>'.esc_attr( $field_args['fields'][$k]['placeholder'] ).'</option>';
                            }
                            if ( ! empty ( $field_args['fields'][$k]['select'] ) && is_array( $field_args['fields'][$k]['select'] ) ) {
                                foreach ( $field_args['fields'][$k]['select'] as $option => $value ) {
                                    if ( sanitize_title( $selected ) == sanitize_title( $option ) ) {
                                        $output .= '<option value="'.esc_attr( $option ).'" selected>'.esc_attr( $value ).'</option>';
                                    } else {
                                        $output .= '<option value="'.esc_attr( $option ).'">'.esc_attr( $value ).'</option>';
                                    }
                                }
                            }
                            $output .= '</select>';
                            $output .= '</div>';
                            $output .= '</div>';

                        } elseif ( $field_args['fields'][$k]['type'] == 'radio' ) {

                            if ( isset ( $field_args['fields'][$k]['title'] ) ) {
                                $item_title = $field_args['fields'][$k]['title'];
                            } else {
                                $item_title = __( 'Radio', 'monamedia' );
                            }

                            if ( isset ( $field_args['fields'][$k]['class'] ) ) {
                                $class = 'class="mona-custom-widget ref-field-radio '.$field_args['fields'][$k]['class'].'"';
                            } else {
                                $class = 'class="mona-custom-widget ref-field-radio"';
                            }

                            if ( isset( $field_args['fields'][$k]['placeholder'] ) && ! empty ( $field_args['fields'][$k]['placeholder'] ) ) {
                                $placeholder = 'placeholder="'.esc_attr( $field_args['fields'][$k]['placeholder'] ).'"';
                            } else {
                                $placeholder = '';
                            }

                            if ( ! empty ( $field_args['value'][$key][$k] ) ) {
                                $checked = $field_args['value'][$key][$k];
                            } else {
                                $checked = '';
                            }

                            if ( ! empty ( $field_args['fields'][$k]['column'] ) && $field_args['fields'][$k]['column'] == 1 ) {
                                $style_clss = 'style="width: 100%;"';
                            } elseif ( ! empty ( $field_args['fields'][$k]['column'] ) && $field_args['fields'][$k]['column'] == 2 ) {
                                $style_clss = 'style="width: 50%;"';
                            } elseif ( ! empty ( $field_args['fields'][$k]['column'] ) && $field_args['fields'][$k]['column'] == 3 ) {
                                $style_clss = 'style="width: 33.3333%;"';
                            } elseif ( ! empty ( $field_args['fields'][$k]['column'] ) && $field_args['fields'][$k]['column'] == 4 ) {
                                $style_clss = 'style="width: 25%;"';
                            } elseif ( ! empty ( $field_args['fields'][$k]['column'] ) && $field_args['fields'][$k]['column'] == 5 ) {
                                $style_clss = 'style="width: 20%;"';
                            } else {
                                $style_clss = 'style="width: 25%;"';
                            }

                            $output .= '<div class="box-field-item render-item box-field-radio">';
                            $output .= '<div class="box-field-title">';
                            $output .= '<label '.$for.' class="txt-label field-text-label">';
                            $output .=  esc_attr( $item_title );
                            $output .= '</label>';
                            $output .= '</div>';
                            $output .= '<div class="box-field-content">';
                            if ( ! empty ( $field_args['fields'][$k]['radio'] ) && is_array( $field_args['fields'][$k]['radio'] ) ) {
                                foreach ( $field_args['fields'][$k]['radio'] as $radio => $value ) {

                                    if ( isset ( $field_args['id'] ) ) {
                                        $for = $field_args['id'].'-row'.'-'.$row.'-'.$k.'-'.sanitize_title( $value );
                                    } else {
                                        $for = $field_args['name'].'-row'.'-'.$row.'-'.$k.'-'.sanitize_title( $value );
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

                        } elseif ( $field_args['fields'][$k]['type'] == 'checkbox' ) {

                            if ( isset ( $field_args['fields'][$k]['title'] ) ) {
                                $item_title = $field_args['fields'][$k]['title'];
                            } else {
                                $item_title = __( 'Checkbox', 'monamedia' );
                            }

                            if ( isset ( $field_args['fields'][$k]['class'] ) ) {
                                $class = 'class="mona-custom-widget ref-field-checkbox '.$field_args['fields'][$k]['class'].'"';
                            } else {
                                $class = 'class="mona-custom-widget ref-field-checkbox"';
                            }

                            if ( isset( $field_args['fields'][$k]['placeholder'] ) && ! empty ( $field_args['fields'][$k]['placeholder'] ) ) {
                                $placeholder = 'placeholder="'.esc_attr( $field_args['fields'][$k]['placeholder'] ).'"';
                            } else {
                                $placeholder = '';
                            }

                            if ( ! empty ( $field_args['value'][$key][$k] ) ) {
                                $checked = $field_args['value'][$key][$k];
                            } else {
                                $checked = '';
                            }

                            if ( ! empty ( $field_args['fields'][$k]['column'] ) && $field_args['fields'][$k]['column'] == 1 ) {
                                $style_clss = 'style="width: 100%;"';
                            } elseif ( ! empty ( $field_args['fields'][$k]['column'] ) && $field_args['fields'][$k]['column'] == 2 ) {
                                $style_clss = 'style="width: 50%;"';
                            } elseif ( ! empty ( $field_args['fields'][$k]['column'] ) && $field_args['fields'][$k]['column'] == 3 ) {
                                $style_clss = 'style="width: 33.3333%;"';
                            } elseif ( ! empty ( $field_args['fields'][$k]['column'] ) && $field_args['fields'][$k]['column'] == 4 ) {
                                $style_clss = 'style="width: 25%;"';
                            } elseif ( ! empty ( $field_args['fields'][$k]['column'] ) && $field_args['fields'][$k]['column'] == 5 ) {
                                $style_clss = 'style="width: 20%;"';
                            } else {
                                $style_clss = 'style="width: 25%;"';
                            }

                            $output .= '<div class="box-field-item render-item box-field-checkbox">';
                            $output .= '<div class="box-field-title">';
                            $output .= '<label '.$for.' class="txt-label field-text-label">';
                            $output .=  esc_attr( $item_title );
                            $output .= '</label>';
                            $output .= '</div>';
                            $output .= '<div class="box-field-content">';
                            if ( ! empty ( $field_args['fields'][$k]['checkbox'] ) && is_array( $field_args['fields'][$k]['checkbox'] ) ) {
                                foreach ( $field_args['fields'][$k]['checkbox'] as $checkbox => $value ) {

                                    if ( isset ( $field_args['id'] ) ) {
                                        $for = $field_args['id'].'-row'.'-'.$row.'-'.$k.'-'.sanitize_title( $value );
                                    } else {
                                        $for = $field_args['name'].'-row'.'-'.$row.'-'.$k.'-'.sanitize_title( $value );
                                    }

                                    $checkbox_name = 'name="'.$field_args['name'].'[row-'.$row.']['.$k.']['.$checkbox.']"';

                                    $output .= '<div class="field-checkbox-item" '.$style_clss.'>';
                                    $output .= '<div class="checkbox-text">';
                                    $output .= '<label for="'.$for.'" class="txt-label item-text-label"></label>';
                                    if ( ! empty ( $field_args['value'][$key][$k] ) && self::is_checked( $checkbox, $field_args['value'][$key][$k] ) ) {
                                        $output .= '<input type="checkbox" '.$class.' id="'.$for.'" '.$checkbox_name.' value="'.esc_attr( $checkbox ).'" '.$placeholder.' checked="checked" />';
                                    } else {
                                        $output .= '<input type="checkbox" '.$class.' id="'.$for.'" '.$checkbox_name.' value="'.esc_attr( $checkbox ).'" '.$placeholder.' />';
                                    }
                                    $output .= '<span class="checkbox-txt">'.esc_attr( $value ).'</span>';
                                    $output .= '</div>';
                                    $output .= '</div>';
                                }
                            }
                            $output .= '</div>';
                            $output .= '</div>';

                        } elseif ( $field_args['fields'][$k]['type'] == 'gallery' ) {

                            if ( isset ( $field_args['fields'][$k]['title'] ) ) {
                                $item_title = $field_args['fields'][$k]['title'];
                            } else {
                                $item_title = __( 'Gallery', 'monamedia' );
                            }

                            if ( ! empty ( $field_args['fields'][$k]['type']['class'] ) ) {
                                $gallery_class = 'mona-custom-widget ref-field-gallery '.$field_args['fields'][$k]['type']['class'].'';
                            } else {
                                $gallery_class = 'mona-custom-widget ref-field-gallery';
                            }

                            $gallery_id = $field_args['name'].'-row-'.$row.'-'.$k.'';

                            $gallery_name = $field_args['name'].'[row-'.$row.']['.$k.']';

                            if ( isset( $field_args['fields'][$k]['placeholder'] ) && ! empty ( $field_args['fields'][$k]['placeholder'] ) ) {
                                $gallery_placeholder = esc_attr( $field_args['fields'][$k]['placeholder'] );
                            } else {
                                $gallery_placeholder = '';
                            }

                            if ( isset( $field_args['fields'][$k]['width'] ) && ! empty ( $field_args['fields'][$k]['width'] ) ) {
                                $width = esc_attr( $field_args['fields'][$k]['width'] );
                            } else {
                                $width = '100';
                            }

                            $output .= '<div class="box-field-item render-item box-field-gallery">';
                            $output .= '<div class="box-field-title">';
                            $output .= '<label '.$for.' class="txt-label field-text-label">';
                            $output .=  esc_attr( $item_title );
                            $output .= '</label>';
                            $output .= '</div>';
                            $output .= '<div class="box-field-content">';
                            $output .= '<div id="get_result_gallery" data-gallery_class="'.$gallery_class.'" data-gallery_id="'.$gallery_id.'" data-gallery_name="'.$gallery_name.'" data-gallery_placeholder="'.$gallery_placeholder.'" data-gallery_width="'.$width.'"></div>';
                            $output .= '<div class="render-gallery-images">';
                            if ( ! empty ( $field_args['value'][$key][$k] ) ) {
                                $image_stt = 0;
                                foreach ( $field_args['value'][$key][$k] as $gallery => $value ) {
                                    $output .= '<div data-id="'.$image_stt.'" class="gallery-column">';
                                    $output .= '<div class="preview-image-item">';
                                    $output .= '<img style="width: '.$width.'px;max-width: '.$width.'px; height:auto" class="'.$gallery_class.'" id="'.$gallery_id.'-'.$image_stt.'" src="'.esc_url( $value ).'" />';
                                    $output .= '<input type="hidden" id="'.$gallery_id.'" name="'.$gallery_name.'['.$image_stt.']" value="'.esc_url( $value ).'" placeholder="'.$gallery_placeholder.'"/>';
                                    $output .= '<div class="preview-image-action">';
                                    $output .= '<a href="javascript:;" class="act-remove-image">'.__( 'Xóa', 'monamedia' ).'</a>';
                                    $output .= '</div>';
                                    $output .= '</div>';
                                    $output .= '</div>';
                                    $image_stt++;
                                }
                            }
                            $output .= '</div>';
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
                }
                $output .= '<div class="box-row-action box-repeater-button button-remove">';
                $output .= '<button class="remove_row_button button button-danger">'.__( 'Xóa dòng', 'monamedia' ).'</button>';
                $output .= '</div>';
                $output .= '</div>';
                $output .= '</div>';
                $row++;
            }
        }
        $output .= '<button class="add_row_button button button-primary">'.__( 'Thêm dòng', 'monamedia' ).'</button>';
        $output .= '<script>
        jQuery(document).ready(function($) {
            WidgetMakeUlSortable = function () {
                $(".box-field-repeater").sortable({
                    handle: ".handle",
                    items: ".field-row-repeater:not(.sprite-add)",
                    opacity: .7,
                    scroll: true,
                    stop: function(event, ui){
                        $(".box-field-repeater").closest(".widget").find("input.widget-control-save").prop("disabled", false);
                        $(".box-field-repeater .field-row-repeater:not(.rowCloneindex)").each(function(i = 0, el){
                        $(el).attr( "data-row_id", $(el).index()-1 );
                        $(el).find(".box-row-head span").text( $(el).index()-1 );
                    });
                }});
                $(".box-field-repeater").disableSelection();
            };
            WidgetMakeUlSortable();
            // // fix disabled input
            $("input, textarea, select").closest(".field-row-repeater").each(function() {
                var row = $(this);
                if (row.hasClass("rowCloneindex")) {
                    row.find("input").attr("disabled", true);
                    row.find("textarea").attr("disabled", true);
                    row.find("select").attr("disabled", true);
                } else {
                    row.find("input").attr("disabled", false);
                    row.find("textarea").attr("disabled", false);
                    row.find("select").attr("disabled", false);
                }
            });
        });
        </script>';
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
            if ( isset( $instance[ 'repeater' ] ) ) {
                $repeater = $instance[ 'repeater' ];
            } else {
                $repeater = '';
            }

            // Gọi hàm
            $this->Mona_Widgets->create_field(
                [
                    'type'   => 'repeater',
                    'name'   => $this->get_field_name( 'repeater' ),
                    'id'     => $this->get_field_id( 'repeater' ),
                    'value'  => $repeater,
                    'title'  => __( 'Repeater', 'monamedia' ),
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
            $instance['repeater'] = $this->Mona_Widgets->update_field( $new_instance['repeater'] );
            </code>
        </pre>
        <?php
    }

}
