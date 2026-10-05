<?php
/**
 * Class Mona Custom Widget
 */
class Render_Field_Gallery {

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
            $widget_title = __( 'Gallery', 'monamedia' );
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

        if ( isset ( $field_args['id'] ) ) {
            $gallery_id = $field_args['id'];
        } else {
            $gallery_id = $field_args['name'];
        }

        if ( isset ( $field_args['class'] ) ) {
            $class = 'mona-custom-widget ref-field-gallery '.esc_attr( $field_args['class'] ).'';
        } else {
            $class = 'mona-custom-widget ref-field-gallery';
        }

        if ( isset ( $field_args['name'] ) ) {
            $name = $field_args['name'];
        } else {
            $name = '';
        }

        $value = '';

        if ( isset ( $field_args['placeholder'] ) ) {
            $placeholder = esc_attr( $field_args['placeholder'] );
        } else {
            $placeholder = '';
        }

        if ( isset ( $field_args['width'] ) ) {
            $width = esc_attr( $field_args['width'] );
        } else {
            $width = '100';
        }

        $output .= '<div class="mona-widget-items render-field box-field-gallery">';
        $output .= '<div class="box-field-title">';
        $output .= '<label '.$for.' class="txt-label field-text-label">';
        $output .=  $widget_title;
        $output .= '</label>';
        $output .= '</div>';
        $output .= '<div class="box-field-content">';
        $output .= '<div id="get_result_gallery" data-gallery_class="'.$class.'" data-gallery_id="'.$gallery_id.'" data-gallery_name="'.$name.'" data-gallery_placeholder="'.$placeholder.'" data-gallery_width="'.$width.'"></div>';
        $output .= '<div class="render-gallery-images">';
        if ( isset ( $field_args['value'] ) && ! empty ( $field_args['value'] ) ) {
            $image_stt = 0;
            foreach ( $field_args['value'] as $gallery => $value ) {
                $output .= '<div class="gallery-column">';
                $output .= '<div class="preview-image-item">';
                $output .= '<img style="width: '.$width.'px; max-width: '.$width.'px; height:auto" class="'.$class.'" id="'.$gallery_id.'-'.$image_stt.'" src="'.esc_url( $value ).'" />';
                $output .= '<input type="hidden" id="'.$gallery_id.'-'.$image_stt.'" name="'.$name.'['.$image_stt.']" value="'.esc_url( $value ).'" placeholder="'.$placeholder.'"/>';
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
            if ( isset( $instance[ 'gallery' ] ) ) {
                $gallery = $instance[ 'gallery' ];
            } else {
                $gallery = '';
            }

            // Gọi hàm
            $this->Mona_Widgets->create_field(
                [
                    'type'         => 'gallery',
                    'name'         => $this->get_field_name( 'gallery' ),
                    'id'           => $this->get_field_id( 'gallery' ),
                    'value'        => $gallery,
                    'title'        => __( 'Gallery', 'monamedia' ),
                    'placeholder'  => __( 'Chọn hình ảnh', 'monamedia' ),
                    'width'        => 50,
                    'docs'         => false,
                ]
            );

            // Cập nhật
            $instance['gallery'] = $this->Mona_Widgets->update_field( $new_instance['gallery'] );
            </code>
            </pre>
        <?php
    }

}
