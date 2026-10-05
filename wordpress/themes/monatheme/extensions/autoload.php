<?php
/**
 * Auto load file
 * extensions
 */
$widgetfile = glob( get_template_directory() . '/extensions/*.php' );
foreach ( $widgetfile as $file ) {
    require_once( $file );
}
?>
