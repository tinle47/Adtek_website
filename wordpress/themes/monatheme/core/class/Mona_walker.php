<?php
class Mona_Custom_Walker_Nav_Menu extends Walker_Nav_Menu
{

    function start_lvl(&$output, $depth = 0, $args = array())
    {
        $indent = str_repeat("\t", $depth);
        $output .= "\n$indent" . '<img src="' . get_site_url() . '/template/assets/images/menu-dropdown.svg" class="subBtn"><ul class="submenu">' . "\n";
    }

    function end_lvl(&$output, $depth = 0, $args = array())
    {
        $indent = str_repeat("\t", $depth);
        $output .= "$indent</ul>\n";
    }

    function start_el(&$output, $item, $depth = 0, $args = array(), $id = 0)
    {
        $object = $item->object;
        $type = $item->type;
        $title = $item->title;
        $description = $item->description;
        $permalink = $item->url;

        if ($depth == 0) {
            $output .= "<li class='" .  implode(" ", $item->classes) . "'>";
        } else {
            $output .= "<li class='submenu-item" .  implode(" ", $item->classes) . "'>";
        }

        //Add SPAN if no Permalink
        if ($permalink && $permalink != '#') {
            $output .= '<a href="' . $permalink . '">';
        } else {
            $output .= '<a href="javascript:;">';
        }

        $output .= $title;

        if ($permalink && $permalink != '#') {
            $output .= '</a>';
        } else {
            $output .= '</a>';
        }
    }
}

class Mona_Custom_Walker_Nav_Menu_Cat_Link extends Walker_Nav_Menu
{

    // Displays start of an element. E.g '<li> Item Name'
    // @see Walker::start_el()
    function start_el(&$output, $item, $depth = 0, $args = array(), $id = 0)
    {
        $object = $item->object;
        $type = $item->type;
        $title = $item->title;
        $description = $item->description;
        $permalink = $item->url;

        $output .= "<li class='subject-item" .  implode(" ", $item->classes) . "'>";

        //Add SPAN if no Permalink
        if ($permalink && $permalink != '#') {
            $output .= '<a class="text-upcase text-16" href="' . $permalink . '">';
        } else {
            $output .= '<span>';
        }

        $output .= $title;

        if ($permalink && $permalink != '#') {
            $output .= '</a>';
        } else {
            $output .= '</span>';
        }

        $output .= "</li>";
    }
}


class Mona_Custom_Walker_Nav_Menu_Sidebar_Link extends Walker_Nav_Menu
{

    // Displays start of an element. E.g '<li> Item Name'
    // @see Walker::start_el()
    function start_el(&$output, $item, $depth = 0, $args = array(), $id = 0)
    {
        $object = $item->object;
        $type = $item->type;
        $title = $item->title;
        $description = $item->description;
        $permalink = $item->url;

        $output .= "<li class='policy-item" .  implode(" ", $item->classes) . "'>";

        //Add SPAN if no Permalink
        if ($permalink && $permalink != '#') {
            $output .= '<a class="title tt-20 t-uppercase policy-link" href="' . $permalink . '">';
        } else {
            $output .= '<span>';
        }

        $output .= $title;

        if ($permalink && $permalink != '#') {
            $output .= '</a>';
        } else {
            $output .= '</span>';
        }

        $output .= "</li>";
    }
}



class Mona_Custom2_Walker_Nav_Menu extends Walker_Nav_Menu
{

    function start_lvl(&$output, $depth = 0, $args = array())
    {
        $indent = str_repeat("\t", $depth);
        $output .= "\n$indent" . '<ul class="menu-list">' . "\n";
    }

    function end_lvl(&$output, $depth = 0, $args = array())
    {
        $indent = str_repeat("\t", $depth);
        $output .= "$indent</ul>\n";
    }

    function start_el(&$output, $item, $depth = 0, $args = array(), $id = 0)
    {
        $classes = empty($item->classes) ? array() : (array) $item->classes;
        $classes[] = 'menu-item-' . $item->ID;

        $class_names = join(' ', array_filter($classes));
        $class_names = $class_names ? ' class="' . esc_attr($class_names) . '"' : '';

        $output .= '<li' . $class_names . '>';

        $atts = array();
        $atts['title']  = ! empty($item->attr_title) ? $item->attr_title : '';
        $atts['target'] = ! empty($item->target)     ? $item->target     : '';
        $atts['rel']    = ! empty($item->xfn)        ? $item->xfn        : '';
        $atts['href']   = ! empty($item->url)        ? $item->url        : '';

        $attributes = '';
        foreach ($atts as $attr => $value) {
            if (! empty($value)) {
                $value = ('href' === $attr) ? esc_url($value) : esc_attr($value);
                $attributes .= ' ' . $attr . '="' . $value . '"';
            }
        }

        $title = apply_filters('the_title', $item->title, $item->ID);

        // Thêm icon nếu có submenu
        $icon = '';
        if (in_array('menu-item-has-children', $classes)) {
            $icon = ' <i class="fa-solid fa-chevron-down"></i>';
        }

        $item_output  = $args->before;
        $item_output .= '<a' . $attributes . '>';
        $item_output .= $args->link_before . $title . $icon . $args->link_after;
        $item_output .= '</a>';
        $item_output .= $args->after;

        $output .= apply_filters('walker_nav_menu_start_el', $item_output, $item, $depth, $args);
    }
}
