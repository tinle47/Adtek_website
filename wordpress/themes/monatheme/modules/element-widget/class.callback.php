<?php
/**
 * Class Mona Custom Widget
 * Callback function
 * Xử lý các yêu cầu
 * Gọi hàm
 */
class MWidget_Callback {

    /**
     * Undocumented function
     */
    function __construct() {

    }

    /**
     * Undocumented function
     *
     * @param string|null $file_patch : bắt buộc, Tên file
     * @param [type] $pagram : Các thông số xử lý [
     * func_class: bắt buộc, tên class
     * field_args: bắt buộc, dữ liệu truyền vào
     * ]
     * @return void
     */
    public function widget_inc_field( string $file_patch = null, array $pagram = null ) {

        if ( $file_patch == null || $pagram == null ) {

            return;
        }

        $inc_file_path = get_template_directory() .'/'. MODULE_WIDGET_FOLDER . '/includes/'.$file_patch.'.php';

        if ( file_exists ( $inc_file_path ) ) {

            require_once( $inc_file_path );

            if ( ! class_exists( $pagram['func_class'] ) ) {

                return;
            }

            $callback = new $pagram['func_class']();

            if ( isset ( $pagram['field_args']['docs'] ) && $pagram['field_args']['docs'] == true ) {

                $callback->get_docs();

            } else {

                $callback->render( $pagram['field_args'] );

            }
        }

    }

    /**
     * Undocumented function
     *
     * @param [type] $field_args
     * @return void
     */
    public function field_not_found( string $fiele_name = '', array $message = null ) {

        $message = [
            'title' => __( 'Không tồn tại loại trường dữ liệu ['.esc_attr( $fiele_name ).']. Hãy sử dụng các kiểu dữ liệu được cho phép bên dưới:', 'monamedia' ),
            'allows' => $this->get_regsiter_field(),
        ];
        ?>
        <div class="mona-widget-not-found">
            <div class="w-title">
                <p><?php echo esc_attr( $message['title'] ) ?></p>
            </div>
            <?php if ( is_array ( $message['allows'] ) ) { ?>
            <div class="w-field-items">
                <ul>
                    <?php
                    foreach ( $message['allows'] as $key => $item ) {
                        echo '<li>'.esc_attr( $item['label'] ).'</li>';
                    }
                    ?>
                </ul>
            </div>
            <?php } ?>
        </div>
        <?php

    }

    /**
     * Undocumented function
     *
     * @param string $field_name
     * @return boolean
     */
    public function is_field( string $field_name = null ) {

        $regsiter_fields = $this->get_regsiter_field();

        if ( is_array ( $regsiter_fields ) ) {

            foreach ( $regsiter_fields as $key => $item ) {

                if ( $field_name == $key && $field_name != null ) {

                    return true;

                }

            }

        }

        return false;

    }

    /**
     * Undocumented function
     *
     * @return void
     */
    public function get_regsiter_field() {

        $message = [
            'text'     => [
                'label' => '[text]',
                'description' => '',
            ],
            'textarea' => [
                'label' => '[textarea]',
                'description' => ''
            ],
            'image'    => [
                'label' => '[image]',
                'description' => '',
            ],
            'select'   => [
                'label' => '[select]',
                'description' => '',
            ],
            'checkbox' => [
                'label' => '[checkbox]',
                'description' => '',
            ],
            'radio'    => [
                'label' => '[radio]',
                'description' => '',
            ],
            'gallery'  => [
                'label' => '[gallery]',
                'description' => '',
            ],
            'group'    => [
                'label' => '[group]',
                'description' => '',
            ],
            'repeater' => [
                'label' => '[repeater]',
                'description' => '',
            ],
        ];

        return (array) $message;

    }

}
