$(document).ready(function() {
    $('.cycle').cycle({fx:'scrollDown',easing:'easeOutBounce',pause:1});

    $('.notification_close').click(function() {
        $(this).parent().animate({opacity: 0, height: 0, padding: 0}, "fast", function() {
            $(this).remove();
        });
    });
});
