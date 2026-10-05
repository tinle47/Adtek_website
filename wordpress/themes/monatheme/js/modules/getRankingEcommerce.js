export default function GetRankingEcommerce() {
    $("#filterRankingEcommerce").submit(function(e){
        e.preventDefault();
        // alert("AA");
        var $this = $(this);
        var _form = $this.serialize();
        var loading = $('.infographic-data');

        $.ajax({
            url: mona_ajax_url.ajaxURL,
            type: 'post',
            data: {
                action: 'mona_ajax_get_rankingEcommerce',
                form:_form
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
                    $('.infographic-data').empty();
                    $('.infographic-data').append(result.data.html);

                }else{
                    
                    $('.infographic-data').empty();
                    $('.infographic-data').append(result.data.mess);
            
                }
            }
        });

    });
}