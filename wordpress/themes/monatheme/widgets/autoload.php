<?php
/**
 * Auto load file
 * widgets
 */
$filename = glob( get_template_directory() . '/widgets/*.php' );
foreach ( $filename as $file ) {
    require_once( $file );
}
?>
