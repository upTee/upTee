function server_info_update() {
    var server_id_list = [];
    $('.server_status_update').each(function(i) {
        var server_id = $(this).attr("data-serverid");

        if($.inArray(server_id, server_id_list) == -1) {
            $.ajax({
                type: "GET",
                url: "/server_info_update/" + server_id + "/",
                success: function(json) {
                    server_info = json.server_info;
                    if(server_info) {
                        $('.server_status_update[data-serverid="' + server_id + '"]').each(function(j) {
                            $(this).find('span[data-info="gametype"]').html(server_info.gametype);
                            $(this).find('span[data-info="map"]').html(server_info.map);
                            $(this).find('span[data-info="slots"]').html(server_info.clients.length + "/" + server_info.max_clients);
                            var password_protected = 'No';
                            if(server_info.flags & 1) // 1 = Flag for password protection
                                password_protected = 'Yes';
                            $(this).find('span[data-info="password"]').html(password_protected);
                        });
                        var scoreboard = $('.server_detail_scoreboard[data-serverid="' + server_id + '"]');
                        if(scoreboard.length && server_info.clients.length) {
                            scoreboard.each(function(j) {
                                $(this).html('<table><tbody><tr><th>Score</th><th>Name</th><th>Clan</th></tr></tbody></table>');
                                var table = $(this).find("tbody tr:last");
                                var data = "";
                                var k;
                                if(server_info.players.length) {
                                    for(k = 0; k < server_info.players.length; k++) {
                                        data += "<tr><td>" + server_info.players[k].score + "</td><td>" + server_info.players[k].name + "</td><td>" + server_info.players[k].clan + "</td></tr>";
                                    }
                                }
                                if(server_info.spectators.length) {
                                    for(k = 0; k < server_info.spectators.length; k++) {
                                        data += "<tr><td>-</td><td>" + server_info.spectators[k].name + "</td><td>" + server_info.spectators[k].clan + "</td></tr>";
                                    }
                                }
                                table.after(data);
                            });
                        }
                        else if(scoreboard.length) {
                            scoreboard.html(''); // clear the scoreboard... otherwise its weird when nobody is there anymore
                            var parent = scoreboard.parent('div.mouseover_overlay');
                            if(parent.length)
                                parent.parent().hide(); // force hiding the overlay so it doesnt look weird when the last player left and you are mouseover
                        }
                    }
                }
            });

            server_id_list.push(server_id);
        }
    });
}

$(document).ready(function() {
    $('.cycle').cycle({fx:'scrollDown',easing:'easeOutBounce',pause:1});

    $('.notification_close').live('click', function() {
        $(this).parent().animate({opacity: 0, height: 0, paddingTop: 0, paddingBottom: 0, marginTop: 0}, 300, function() {
            $(this).remove();
        });
    });

    setInterval(server_info_update, 30000);

    $('p[data-info="slots"]').mousemove(function(e) {
        var hide_mouseover = $(this).siblings("div.hide_mouseover");
        if(hide_mouseover.length) {
            var x = e.clientX-parseInt(hide_mouseover.css("width"), 10)-10;
            if(x < 5)
                x = e.clientX+10;
            var y = e.clientY-10;
            if(hide_mouseover.find('tr').length > 1) // dont even try to activate the overlay if the scoreboard doesnt have any data anyway
                hide_mouseover.css({"display": "inherit", "top": y, "left": x});
        }
    }).mouseout(function(){
        $("div.hide_mouseover").css("display", "none");
    });

    var vote_number = 1;
    $('#add_vote').html('<p><button class="button" type="button">Add vote</button></p>');
    $('#add_vote button').click(function() {
        table = $('#add_vote').parent().find('tbody');
        table.append('<tr> \
                        <th><input type="text" name="title new title ' + vote_number + ' new" value="New vote" id="id-' + vote_number + '-title_new"></th> \
                        <td><input type="text" name="command new command ' + vote_number + ' new" value="command" id="id-' + vote_number + '-command_new"></td> \
                        <td><div class="delete_vote"><div class="del_button" onclick=""></div></div></td> \
                    </tr>');
        vote_number++;
    });

    $('.delete_vote').html('<div class="del_button" onclick=""></div>');
    $('.delete_vote div.del_button').live('click', function() {
        tr = $(this).parents('tr');
        tr.hide();
        tr.find('input').attr('value', '');
    });

    var rcon_number = 1;
    $('#add_command').html('<p><button class="button" type="button">Add rcon command</button></p>');
    $('#add_command button').click(function() {
        var selected_command = $('#rcon_commands_select :selected').text();
        table = $('#add_command').parent().find('tbody');
        table.append('<tr> \
                        <th><label for="new-' + selected_command + '-' + rcon_number + '">' + selected_command + ':</label></th> \
                        <td><input type="text" name="new-' + selected_command + '-' + rcon_number + '" value="command" id="new-' + selected_command + '-' + rcon_number + '"></td> \
                        <td><div class="delete_command"><div class="del_button" onclick=""></div></div></td> \
                    </tr>');
        rcon_number++;
    });

    $('.delete_command').html('<div class="del_button" onclick=""></div>');
    $('.delete_command div.del_button').live('click', function() {
        tr = $(this).parents('tr');
        tr.hide();
        tr.find('input').attr('value', '');
    });

    $('input[type=file]').each(function(i) {
        $(this).css('display', 'none');
        var name = $(this).attr('name');
        $(this).after('<input type="text" data-type="file" data-for="' + name + '" readonly><button type="button" data-type="file" data-for="' + name + '">Browse...</button>');

        $(this).change(function() {
            var data = $(this).attr('value');
            $('input[data-for="' + name + '"]').attr('value', data);
        });
    });
    $('button[data-type=file], input[data-type=file]').click(function() {
        var data_for = $(this).attr('data-for');
        $('input[name=' + data_for + ']').click();
    });

    $('#comment_form').css('display', 'none');

    // terminal interval
    (function receive_terminal_interval() {
        receive_entries();

        setTimeout(receive_terminal_interval, 1000);
    })();

    var event_form_count = 0;
    (function event_calender() {
        if($('#events').length) {
            $('#events').eventCalendar();
        }

        if($('#events-admin').length) {
            $('#events-admin').eventCalendar({
                showDelete: true
            });

            // add button to create a new event here
            $('.eventsCalendar-list-wrap').append('<p><a class="add_event" href="#">Add Event</a></p>');
            $('a.add_event').click(function(e) {
                e.preventDefault();

                if(!$('#event_form').length) {
                    var server_id = $('.server_detail_events').attr('data-serverid');
                    $('.server_detail_events').append('<div id="event_form"><p class="loading">loading...</p></div>');

                    $.ajax({
                        url: '/server/' + server_id + '/events/add/',
                        type: 'GET',
                        success: function(data) {
                            $('#event_form').html(data);

                            if(!event_form_count) {
                                handle_event_form(server_id);
                                event_form_count = 1;
                            }
                        }
                    });
                }
            });
        }
    })();
});

function toogle_comments() {
    $(document).ready(function() {
        $('form').slideToggle('fast', function() {
            if($('.create_comment form').css('display') != 'none')
                $(window).scrollTop($('.create_comment').position().top);
        });
    });
}


// terminal stuff
var command_list = [];
var command_list_index = 0;

$(document).keypress(function(e) {
    if (e.which == 13 && $('#terminal_command_input:focus').length) {
        handle_input();
    }

    if (e.keyCode == 38 && $("#terminal_command_input:focus").length) {
        rotate_commands(0);
    }
    
    if (e.keyCode == 40 && $("#terminal_command_input:focus").length) {
        rotate_commands(1);
    }
});

function handle_input() {
    var command = $('#terminal_command_input').val();
    if (command === '') return;
    command_list.push(command);
    command_list_index = command_list.length;
    $('#terminal_command_input').val('');
    send_command(command);
}

function add_entry(line) {
    var data = '<p>' + line + '</p>';
    $('#terminal_entry').append(data);
    $('#terminal_entry').animate({
        scrollTop: $('#terminal_entry')[0].scrollHeight
    }, 'normal');
}

function send_command(command) {
    var server_id = $('#terminal').attr('data-serverid');

    $.ajax({
        beforeSend: function(jqXHR, settings) {
            var csrftoken = $.cookie('csrftoken');
            jqXHR.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: '/server_terminal_command/' + server_id + '/',
        type: 'POST',
        data: {
            'command': command
        }
    });
}

function receive_entries(command) {
    if($('#terminal').length) {
        var server_id = $('#terminal').attr('data-serverid');

        $.ajax({
            url: '/server_terminal_receive/' + server_id + '/',
            type: 'GET',
            success: function(json) {
                var entries = json.lines;
                if(entries) {
                    var i;
                    for(i = 0; i < entries.length; i++) {
                        add_entry(entries[i]);
                    }
                }
            }
        });
    }
}

function rotate_commands(direction) {
    if(!direction) {
        if(command_list_index > 0) {
            command_list_index--;
            $('#terminal_command_input').val(command_list[command_list_index]);
        }
    }
    else {
        if(command_list_index < command_list.length) {
            command_list_index++;
            $('#terminal_command_input').val(command_list[command_list_index]);
        }
        else {
            $('#terminal_command_input').val('');
        }
    }
}

function handle_event_form(server_id) {
    $('#event_form .button').live('click', function(e) {
        e.preventDefault();

        $('#event_form').append('<p class="loading">loading...</p>');

        $.ajax({
            beforeSend: function(jqXHR, settings) {
                var csrftoken = $.cookie('csrftoken');
                jqXHR.setRequestHeader('X-CSRFToken', csrftoken);
            },
            type: "POST",
            url: '/server/' + server_id + '/events/add/',
            data: $('#event_form :input').serialize(), // serializes the form's elements.
            success: function(data)
            {
                if(data.length) {
                    $('#event_form').html(data);
                }
                else {
                    $('#event_form').remove();
                    $('.eventsCalendar-list-wrap').append('<div class="notification_s success">Event successfully added!<div class="notification_close"></div></div>');
                }
            }
        });
    });

    $('#event_form .close_button').live('click', function(e) {
        e.preventDefault();

        $('#event_form').remove();
    });
}
