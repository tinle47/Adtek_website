<?php
/*
 * Trang tác giả (/author/<tên>/): hồ sơ tác giả cho E-E-A-T và danh sách bài viết.
 * Tiểu sử lấy từ Hồ sơ người dùng > Thông tin tiểu sử; chức danh (adtek_job_title) và LinkedIn do mu-plugin adtek-yoast-settings ghi.
 * Theme không có author.php trước đây nên trang này rơi về archive.php (trang trống).
 */
get_header();
$author   = get_queried_object();
$bio      = get_the_author_meta( 'description', $author->ID );
$job      = get_user_meta( $author->ID, 'adtek_job_title', true );
$linkedin = get_user_meta( $author->ID, 'linkedin', true );
?>

<div class="breadcrumb" data-aos="fade-right">
    <div class="container">
        <div class="breadcrumb-wrap">
            <ul class="breadcrumb-list">
                <li class="breadcrumb-item"><a href="<?php echo home_url(); ?>"><?php echo mona_get_home_title(); ?></a></li>
                <li class="breadcrumb-item"><a href="<?php echo mona_get_blogs_url(); ?>"><?php echo mona_get_blogs_title(); ?></a></li>
                <li class="breadcrumb-item"><a href="javascript:;"><?php echo esc_html( $author->display_name ); ?></a></li>
            </ul>
        </div>
    </div>
</div>

<style>
.adtek-author { display: flex; gap: 24px; align-items: flex-start; margin: 0 0 40px; padding: 24px; background: #F7F4EE; border-radius: 10px; }
.adtek-author img { width: 96px; height: 96px; border-radius: 10px; object-fit: cover; flex: none; }
.adtek-author-job { margin: 4px 0 12px; color: #F27407; font-weight: 600; }
.adtek-author-bio { margin: 0 0 12px; line-height: 1.7; }
.adtek-author-link { color: #1B4075; font-weight: 600; }
@media (max-width: 600px) { .adtek-author { flex-direction: column; } }
</style>

<section class="section blog">
    <div class="container">
        <?php adtek_page_heading( $author->display_name ); ?>
        <div class="adtek-author" data-aos="fade-up">
            <?php echo get_avatar( $author->ID, 192, '', esc_attr( $author->display_name ) ); ?>
            <div>
                <?php if ( $job ) { ?><p class="adtek-author-job"><?php echo esc_html( $job ); ?></p><?php } ?>
                <?php if ( $bio ) { ?><div class="adtek-author-bio"><?php echo wpautop( wp_kses_post( $bio ) ); ?></div><?php } ?>
                <?php if ( $linkedin ) { ?><a class="adtek-author-link" href="<?php echo esc_url( $linkedin ); ?>" target="_blank" rel="noopener me">LinkedIn</a><?php } ?>
            </div>
        </div>
        <div class="blog-ctn">
            <div class="blog-main">
                <?php if ( have_posts() ) { ?>
                <div class="blog-list">
                    <?php
                    while ( have_posts() ) {
                        the_post();
                        get_template_part( 'patch/loop/box', 'news-blog' );
                    }
                    ?>
                </div>
                <nav class="pagination" data-aos="fade-up">
                    <?php mona_page_navi(); ?>
                </nav>
                <?php } else { ?>
                <div class="mona-mess-empty">
                    <p><?php echo __( 'Content is being update', 'monamedia' ); ?></p>
                </div>
                <?php } wp_reset_query(); ?>
            </div>
            <div class="blog-aside" data-aos="fade-up">
                <?php if ( ! function_exists( 'dynamic_sidebar' ) || ! dynamic_sidebar( 'sidebar_post' ) ) : ?><?php endif; ?>
            </div>
        </div>
    </div>
</section>

<?php get_footer(); ?>
