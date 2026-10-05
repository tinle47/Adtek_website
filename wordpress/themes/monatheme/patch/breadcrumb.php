<?php
    $obz = get_queried_object();
?>
<div class="breadcrumb" data-aos="fade-right">
    <div class="container">
        <div class="breadcrumb-wrap">
            <ul class="breadcrumb-list">
                <li class="breadcrumb-item">
                    <a href="<?php echo home_url(); ?>"><?php echo mona_get_home_title(); ?></a>
                </li>

                <?php if ( is_category() ){ ?>
                <li class="breadcrumb-item">
                    <a href="javascript:;"><?php echo $obz->name; ?></a>
                </li>
                <?php
                }elseif ( is_home() ){ ?>
                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo get_the_title(MONA_PAGE_BLOG); ?>
                    </a>
                </li>
                <?php
                }elseif ( is_search() ) { ?>
                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo __('Search','monamedia'); ?>
                    </a>
                </li>
                <?php
                } elseif ( $obz->post_type == 'post' ) { ?>
                <li class="breadcrumb-item">
                    <a href="<?php echo mona_get_blogs_url(); ?>">
                        <?php echo mona_get_blogs_title(); ?>
                    </a>
                </li>
                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo the_title(); ?>
                    </a>
                </li>
                <?php
                } elseif ( $obz->post_type == 'mona_recruitment' ) { ?>
                <li class="breadcrumb-item">
                    <a href="<?php echo get_the_permalink(MONA_PAGE_RECRUITMENT); ?>">
                        <?php echo get_the_title(MONA_PAGE_RECRUITMENT); ?>
                    </a>
                </li>
                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo the_title(); ?>
                    </a>
                </li>

                <?php
                } elseif ( is_page(MONA_PAGE_RESOURCES) ) { ?>

                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo __('Resources','monamedia'); ?>
                    </a>
                </li>

                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo the_title(); ?>
                    </a>
                </li>

                <?php
                } elseif ( is_page(MONA_PAGE_GLOSSARY) ) { ?>
                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo __('Resources','monamedia'); ?>
                    </a>
                </li>

                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo the_title(); ?>
                    </a>
                </li>

                <?php
                } elseif ( is_singular('mona_glossary') ) { ?>
                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo __('Resources','monamedia'); ?>
                    </a>
                </li>

                <li class="breadcrumb-item">
                    <a href=" <?php echo get_the_permalink(MONA_PAGE_GLOSSARY); ?>">
                        <?php echo get_the_title(MONA_PAGE_GLOSSARY); ?>
                    </a>
                </li>

                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo the_title(); ?>
                    </a>
                </li>

                <?php
                } elseif ( is_singular('mona_reports') ) { ?>
                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo __('Resources','monamedia'); ?>
                    </a>
                </li>

                <li class="breadcrumb-item">
                    <a href=" <?php echo get_the_permalink(MONA_PAGE_RESOURCES); ?>">
                        <?php echo get_the_title(MONA_PAGE_RESOURCES); ?>
                    </a>
                </li>

                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo the_title(); ?>
                    </a>
                </li>

                <?php
                } elseif ( is_tax('category_reports') ) { ?>
                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo __('Resources','monamedia'); ?>
                    </a>
                </li>

                <li class="breadcrumb-item">
                    <a href=" <?php echo get_the_permalink(MONA_PAGE_RESOURCES); ?>">
                        <?php echo get_the_title(MONA_PAGE_RESOURCES); ?>
                    </a>
                </li>

                <li class="breadcrumb-item">
                    <a href="javascript:;">
                        <?php echo $obz->name; ?>
                    </a>
                </li>

                <?php }elseif( is_tax() ){ ?>
                <li class="breadcrumb-item">
                    <a href="javascript:;"><?php echo $obz->name; ?></a>
                </li>
                <?php } else{ ?>
                <li class="breadcrumb-item">
                    <a href="javascript:;"><?php echo get_the_title(); ?></a>
                </li>
                <?php } ?>
            </ul>
        </div>
    </div>
</div>