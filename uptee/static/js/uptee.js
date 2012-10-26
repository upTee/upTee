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
                            if(server_info.clients.length) {
                                if($(this).find(".clients").length)
                                    $(this).find(".clients").html('<div class="sidebar_entry"></div>');
                                else
                                    $(this).append('<div class="clients"><div class="sidebar_entry"></div></div>')
                                if(server_info.players.length) {
                                    var table = $(this).find(".clients .sidebar_entry");
                                    table.html('<div class="players"><p><b>Players</b></p><table><tbody><tr><th>Score</th><th>Name</th><th>Clan</th></tr></tbody></table></div>');
                                    table = $(this).find(".clients .sidebar_entry .players tbody tr:last");
                                    for(var i = 0; i < server_info.players.length; i++) {
                                        data = "<tr><td>" + server_info.players[i].score + "</td><td>" + server_info.players[i].name + "</td><td>" + server_info.players[i].clan + "</td></tr>";
                                        table.after(data);
                                    }
                                }
                                if(server_info.spectators.length) {
                                    var table = $(this).find(".clients .sidebar_entry");
                                    table.append('<div class="spectators"><p><b>Spectators</b></p><table><tbody><tr><th>Name</th><th>Clan</th></tr></tbody></table></div>');
                                    table = $(this).find(".clients .sidebar_entry .spectators tbody tr:last");
                                    for(var i = 0; i < server_info.spectators.length; i++) {
                                        data = "<tr><td>" + server_info.spectators[i].name + "</td><td>" + server_info.spectators[i].clan + "</td></tr>";
                                        table.after(data);
                                    }
                                }
                            }
                            else
                                $(this).find(".clients").remove();
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

    $('p[info="slots"]').mousemove(function(e) {
        var clients = $(this).parent().find("div.clients");
        if(clients.length) {
            var x = e.clientX-parseInt(clients.css("width"))-10;
            if(x < 5)
                x = e.clientX+10;
            var y = e.clientY-10;
            clients.css({"visibility": "visible", "top": y, "left": x});
        }
    }).mouseout(function(){
        $("div.clients").css("visibility", "hidden");
    });

    var number = 1;
    $('#add_vote').html('<p><button type="button">Add vote</button></p>');
    $('#add_vote button').click(function() {
        table = $('#add_vote').parent().find('tbody');
        table.append('<tr> \
                        <th><input type="text" name="title new title ' + number + ' new" value="New vote" id="id-' + number + '-title_new"></th> \
                        <td><input type="text" name="command new command ' + number + ' new" value="command" id="id-' + number + '-command_new"></td> \
                        <td><div class="delete_vote"><div class="del_button"></div></div></td> \
                    </tr>');
        number++;
    });

    $('.delete_vote').html('<div class="del_button"></div>');
    $('.delete_vote div.del_button').live('click', function() {
        tr = $(this).parents('tr');
        tr.hide();
        tr.find('input').attr('value', '');
    });
});
