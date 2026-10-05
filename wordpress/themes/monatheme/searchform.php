
<div class="search-box fr">
    <form method="get" id="searchform" class="searchform" action="<?php echo esc_url(home_url('/')); ?>" >
        <input type="search" class="search-field" name="s" value="<?php echo get_search_query(); ?>" id="s" placeholder="<?php echo esc_attr_x('Search &hellip;', 'placeholder', 'monamedia'); ?>" />
        <button type="submit" class="submit-btn"><i class="fa fa-search"></i></button>
    </form>
</div>
