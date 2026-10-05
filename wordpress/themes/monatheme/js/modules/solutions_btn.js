export default function monaSolutionsBtn() {

    $( ".popup-with-zoom-anim" ).click(function() {
        var solution_title = $(this).data('solution_title');
        var solution_id_cf = $(this).data('solution_id_cf');
        $('#'+solution_id_cf+' input[name="your_solution_title"]').val(solution_title)
    });
    
}