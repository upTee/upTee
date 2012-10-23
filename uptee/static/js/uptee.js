function server_info_update() {
    var server_id_list = [];
    $('.server_status_update').each(function(i) {
        var server_id = $(this).attr("serverid");

        if($.inArray(server_id, server_id_list) == -1) {
            $.ajax({
                type: "GET",
                url: "/server_info_update/" + server_id + "/",
                success: function(json) {
                    server_info = json.server_info;
                    if(server_info) {
                        $('.server_status_update[serverid="' + server_id + '"]').each(function(j) {
                            $(this).find('span[info="gametype"]').html(server_info.gametype);
                            $(this).find('span[info="map"]').html(server_info.map);
                            $(this).find('span[info="slots"]').html(server_info.clients.length + "/" + server_info.max_clients);
                        });
                    }
                }
            });

            server_id_list.push(server_id);
        }
    });
}

$(document).ready(function() {
    $('.cycle').cycle({fx:'scrollDown',easing:'easeOutBounce',pause:1});

    $('.notification_close').click(function() {
        $(this).parent().animate({opacity: 0, height: 0, paddingTop: 0, paddingBottom: 0, marginTop: 0}, 300, function() {
            $(this).remove();
        });
    });

    setInterval(server_info_update, 10000);
});
