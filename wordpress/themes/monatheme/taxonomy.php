<?php
/*
 * CUSTOM POST TYPE TAXONOMY TEMPLATE
 *
 * This is the custom post type taxonomy template. If you edit the custom taxonomy name,
 * you've got to change the name of this template to reflect that name change.
 *
 * For Example, if your custom taxonomy is called "register_taxonomy('shoes')",
 * then your template name should be taxonomy-shoes.php
 *
 * For more info: http://codex.wordpress.org/Post_Type_Templates#Displaying_Custom_Taxonomies
 */
$obz = get_queried_object();
// if($obz->taxonomy == 'teachers') {
//     wp_redirect(get_permalink(PAGE_GV));
//     exit();
// }
?>
<?php get_header(); ?>
<?php 
/**
 * MONA GET LAYOUT - TAXONOMY
 * CONTEN TAXONOMY - GET SLUG TAXONOMY
 * TAXONOMY-CONTENT-{taxonomy}
 */
get_template_part('patch/taxonomy-content/taxonomy', $obz->taxonomy);
?>
<?php get_footer(); ?>
