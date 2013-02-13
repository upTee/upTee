$(document).ready(function() {
    // fold button logic
    $('#fold_button').click(function() {
        if($('#fold_button .icon').length) {
            $('#option_menu_entries').slideUp('fast', function() {
                    $('#fold_button .icon').attr('class', 'icon_collapsed');
                    $('#content_container').animate({'left': '100'}, 'fast');
                    $('#breadcrum').animate({'left': '100'}, 'fast');
            });
        }
        if($('#fold_button .icon_collapsed').length) {
            $('#content_container').animate({'left': '301'}, 'fast');
            $('#breadcrum').animate({'left': '300'}, 'fast', function() {
                $('#option_menu_entries').slideDown('fast', function() {
                    $('#fold_button .icon_collapsed').attr('class', 'icon');
                });
            });
        }
    });
});