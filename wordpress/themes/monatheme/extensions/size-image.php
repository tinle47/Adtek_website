<?php

/**
 * Undocumented function
 *
 * @return void
 */
function mona_image_size()
{
    add_image_size('1900x790', 1900, 790, true);
    add_image_size('1920x600', 1920, 600, true);
    add_image_size('400x675', 400, 675, true);
    add_image_size('600x600', 600, 600, false);
    add_image_size('50x50', 50, 50, true);
    add_image_size('474x474', 474, 474, true);
    add_image_size('270x295', 270, 295, true);
    add_image_size('370x250', 370, 250, true);
    add_image_size('80x70', 80, 70, true);
    add_image_size('100x100', 100, 100, true);
    add_image_size('870x362', 870, 362, true);
    add_image_size('570x345', 570, 345, false);
    add_image_size('960x534', 960, 534, true);
    add_image_size('30x30', 30, 30, true);
    add_image_size('370x300', 0, 0, true);
    add_image_size('370x518', 0, 0, true);
    add_image_size('190x70', 190, 70, true);
    add_image_size('140x120', 140, 120, true);
    add_image_size('0', 0, 0, true);
}
add_action('after_setup_theme', 'mona_image_size');
