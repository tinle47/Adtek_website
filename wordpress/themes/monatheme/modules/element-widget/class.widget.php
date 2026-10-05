<?php
/**
 * Update version 2
 * Ngày 11-1-2022
 * Nội dung sửa chữa:
 *  - Cập nhật lại layout và chia file, chia thư mục
 *
 *  --------- Khoảng cách ---------------
 *
 * Update version 2.1
 * Ngày 25-1-2022
 * Nội dung sửa chữa:
 *  - Thêm trường nhập liệu field group
 *  - Thêm phần hiện hướng dẫn dùng field tại create_field(): docs = true,
 *  - Thay đổi cách gọi hàm ở class callback
 *
 *  --------- Khoảng cách ---------------
 *
 * Class Mona Custom Widget
 * Chức năng:
 * - Tạo field, render ra mã html từ dữ liệu đầu vào
 * - Các tham số phải có như:
 *  + $field_args
 *  + $field_args: [ type, name, value ]
 * - Đối với field repeater, group buộc phải có thêm mãng con với khóa là fields.
 */
define( 'MODULE_WIDGET_FOLDER', 'modules/element-widget' );

class Mona_Exs_Widgets extends MWidget_Callback {

    /**
     * Undocumented function
     * Load css, js
     */
    function __construct() {

        add_action( 'admin_enqueue_scripts', [$this, 'add_support_upload'] );
    }

    /**
     * Undocumented function
     *
     * Khởi tạo funtion
     * funtion tạo các field html từ dữ liệu truyền vào
     * @param array $field_args
     * @return void
     */
    public function create_field( array $field_args = [] ) {

        $output = '';

        $field_type = isset( $field_args['type'] ) ? esc_attr( $field_args['type'] ) : '';

        if ( ! $this->is_field( esc_attr( $field_args['type'] ) ) ) {

            $field_type = 'not_found';

        }

        switch ( $field_type ) :

            case 'text':

                $this->widget_inc_field( 'class.field_Text',
                    [
                        'func_class' => 'Render_Field_Text',
                        'field_args' => $field_args,
                    ]
                );
                break;

            case 'textarea':

                $this->widget_inc_field( 'class.field_Textarea',
                    [
                        'func_class' => 'Render_Field_Textarea',
                        'field_args' => $field_args,
                    ]
                );
                break;

            case 'image':

                $this->widget_inc_field( 'class.field_Image',
                    [
                        'func_class' => 'Render_Field_Image',
                        'field_args' => $field_args,
                    ]
                );
                break;

            case 'select':

                $this->widget_inc_field( 'class.field_Select',
                    [
                        'func_class' => 'Render_Field_Select',
                        'field_args' => $field_args,
                    ]
                );
                break;

            case 'radio':

                $this->widget_inc_field( 'class.field_Radio',
                    [
                        'func_class' => 'Render_Field_Radio',
                        'field_args' => $field_args,
                    ]
                );
                break;

            case 'checkbox':

                $this->widget_inc_field( 'class.field_Checkbox',
                    [
                        'func_class' => 'Render_Field_Checkbox',
                        'field_args' => $field_args,
                    ]
                );
                break;

            case 'gallery':

                $this->widget_inc_field( 'class.field_Gallery',
                    [
                        'func_class' => 'Render_Field_Gallery',
                        'field_args' => $field_args,
                    ]
                );
                break;

            case 'group':

                $this->widget_inc_field( 'class.field_Group',
                    [
                        'func_class' => 'Render_Field_Group',
                        'field_args' => $field_args,
                    ]
                );
                break;

            case 'repeater':

                $this->widget_inc_field( 'class.field_Repeater',
                    [
                        'func_class' => 'Render_Field_Repeater',
                        'field_args' => $field_args,
                    ]
                );
                break;

            default:

                $this->field_not_found( $field_args['type'] );
                break;

        endswitch;

    }

    /**
     * Undocumented function
     *
     * @param string $fied_value
     * @return void
     */
    public function update_field( $fied_value = '' ) {

        if ( ! empty ( $fied_value ) && is_array( $fied_value ) ) {

            $instance = (array)$fied_value;

        } elseif ( ! empty ( $fied_value ) && ! is_array( $fied_value ) ) {

            $instance = esc_attr( $fied_value );

        } else {
            $instance = '';
        }

        return $instance;
    }

    /**
     * Undocumented function
     *
     * @return void
     */
    public function add_support_upload() {
        wp_enqueue_media();
        // loading css
        wp_enqueue_style( 'mona_style_widget_admin', get_template_directory_uri() .'/'. MODULE_WIDGET_FOLDER . '/css/widget-style.css', array(), false, 'all' );
        // loading js
        wp_enqueue_script( 'mona_js_widget_admin', get_template_directory_uri() .'/'. MODULE_WIDGET_FOLDER . '/js/widget-field.js', array(), false, true );
         // loading js
         wp_enqueue_script( 'mona_ui_widget_admin', get_template_directory_uri() .'/'. MODULE_WIDGET_FOLDER . '/js/jquery-ui.js', array(), false, true );
    }

}
