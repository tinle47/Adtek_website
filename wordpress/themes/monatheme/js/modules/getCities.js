export default function SelectGetCities() {
    $("#filterRecruitment select[name=country_recruitment]").each(function(i,v){
      
        var _this = $(this);
        var country_recruitment = _this.val();
        var slug_city_action = $("#filterRecruitment input[name=slug_city_action]").val();
        var loading = $('#filterRecruitment');

        $.ajax({
            url: mona_ajax_url.ajaxURL,
            type: 'post',
            data: {
                action: 'mona_ajax_get_cities',
                country_recruitment: country_recruitment,
                slug_city_action: slug_city_action
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
}