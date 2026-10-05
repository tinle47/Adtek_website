<?php

if (class_exists('Kirki')) {

    /**
     * Add sections
     */
    function kirki_demo_scripts() {
        wp_enqueue_style('kirki-demo', get_stylesheet_uri(), array(), time());
    }

    add_action('wp_enqueue_scripts', 'kirki_demo_scripts');
    $priority = 1;
    Kirki::add_panel('panel_theme', array(
            'title' => __('Theme Functions', 'monamedia'),
            'priority' => $priority++,
            'capability' => 'edit_theme_options',
    ));
    
    Kirki::add_section('shortcode_form', array(
        'title' => esc_attr__('Shortcode Form', 'monamedia'),
        'priority' => $priority++,
        'capability' => 'edit_theme_options',
        'panel' => 'panel_theme',
    ));

    /** Add field */
    Kirki::add_field('mona_setting', array(
        'type' => 'text',
        'settings' => 'recruitment_contactform',
        'label' => esc_attr__('Form RECRUITMENT', 'monamedia'),
        'description' => '',
        'help' => '',
        'section' => 'shortcode_form',
        'default' => '',
        'priority' => $priority++,
    ));
    Kirki::add_field('mona_setting', array(
        'type' => 'text',
        'settings' => 'reports_contactform',
        'label' => esc_attr__('Form REPORTS', 'monamedia'),
        'description' => '',
        'help' => '',
        'section' => 'shortcode_form',
        'default' => '',
        'priority' => $priority++,
    ));

    Kirki::add_section('section_information', array(
        'title' => esc_attr__('Website Information', 'monamedia'),
        'priority' => $priority++,
        'capability' => 'edit_theme_options',
        'panel' => 'panel_theme',
    ));
     /** Add field */
     Kirki::add_field('mona_setting', array(
        'type' => 'text',
        'settings' => 'information_time',
        'label' => esc_attr__('Time', 'monamedia'),
        'description' => '',
        'help' => '',
        'section' => 'section_information',
        'default' => '',
        'priority' => $priority++,
    ));
    Kirki::add_field('mona_setting', array(
        'type' => 'text',
        'settings' => 'information_phone',
        'label' => esc_attr__('Phone', 'monamedia'),
        'description' => '',
        'help' => '',
        'section' => 'section_information',
        'default' => '',
        'priority' => $priority++,
    ));
    Kirki::add_field('mona_setting', array(
        'type' => 'text',
        'settings' => 'information_email',
        'label' => esc_attr__('Email', 'monamedia'),
        'description' => '',
        'help' => '',
        'section' => 'section_information',
        'default' => '',
        'priority' => $priority++,
    ));
    Kirki::add_field('mona_setting', array(
        'type' => 'text',
        'settings' => 'information_faq',
        'label' => esc_attr__('FAQ', 'monamedia'),
        'description' => '',
        'help' => '',
        'section' => 'section_information',
        'default' => '',
        'priority' => $priority++,
    ));
    Kirki::add_field('mona_setting', array(
        'type' => 'image',
        'settings' => 'information_ft_logo',
        'label' => esc_attr__('Footer Logo', 'monamedia'),
        'description' => '',
        'help' => '',
        'section' => 'section_information',
        'default' => '',
        'priority' => $priority++,
    ));
    Kirki::add_field('mona_setting', array(
        'type' => 'textarea',
        'settings' => 'information_desc',
        'label' => esc_attr__('Description', 'monamedia'),
        'description' => '',
        'help' => '',
        'section' => 'section_information',
        'default' => '',
        'priority' => $priority++,
    ));
}
if (!function_exists('mona_option')) {

    function mona_option($setting, $default = '') {
        echo mona_get_option($setting, $default);
    }

    function mona_get_option($setting, $default = '') {
        if (class_exists('Kirki')) {
            $value = $default;
            $options = get_option('option_name', array());
            $options = get_theme_mod($setting, $default);
            if (isset($options)) {
                $value = $options;
            }
            return $value;
        }
        return $default;
    }

}