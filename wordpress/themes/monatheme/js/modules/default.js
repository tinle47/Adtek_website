export default function monaCreateModuleDefault() {

    $("#filterRecruitment select[name=country_recruitment]").change(function() {

        var _this = $(this);
        var country_recruitment = _this.val();
        var loading = $('#filterRecruitment');

        $.ajax({
            url: mona_ajax_url.ajaxURL,
            type: 'post',
            data: {
                action: 'mona_ajax_get_cities',
                country_recruitment: country_recruitment,
            },
            error: function(request) {
                loading.removeClass('loading');
            },
            beforeSend: function(response) {
                loading.addClass('loading');
            },
            success: function(result) {
                loading.removeClass('loading');
                if (result.success) {

                    // $('select[name=district]').html($result['html']);
                    //alert(result.data.html);
                    $('#filterRecruitment select[name=city_recruitment]').find('option:not(:first)').remove();
                    $('#filterRecruitment select[name=city_recruitment]').append(result.data.html);

                }
            }
        });

    });

    $(document).on('click', '.wpcf7-form-control-wrap', function(e) {
        
        var $this = $(this);
        $this.find('.wpcf7-not-valid-tip').hide();
    });


    $("#filterRecruitment").submit(function() {
        $('#filterRecruitment input[name=slug_city_action]').remove();
    });

    $('.recruitment-dt-btn .btn').click(function() {
        var nominee = $(this).data('nominee');
        $('input[name=your_nominee]').val(nominee);
    })

    $('.ft .social').removeClass('phone');

}