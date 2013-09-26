$(document).ready(function() {

    // notification closer
    $(document).on('click', '.notificationClose', function() {
        $(this).parent().animate({opacity: 0, height: 0, paddingTop: 0, paddingBottom: 0, marginTop: 0}, 300, function() {
            $(this).remove();
        });
    });

    // vote stuff
    var vote_number = 1;
    $('#addVote').html('<p><button class="button" type="button">Add vote</button></p>');
    $('#addVote button').click(function() {
        var table = $('#addVote').parent().find('tbody');
        table.append('<tr> \
                        <th><input type="text" name="title new title ' + vote_number + ' new" value="New vote" id="id-' + vote_number + '-title_new"></th> \
                        <td><input type="text" name="command new command ' + vote_number + ' new" value="command" id="id-' + vote_number + '-command_new"></td> \
                        <td><div class="deleteVote"><div class="delButton" onclick=""></div></div></td> \
                    </tr>');
        vote_number++;
    });

    $('.deleteVote').html('<div class="delButton" onclick=""></div>');
    $(document).on('click', '.deleteVote div.delButton', function() {
        var tr = $(this).parents('tr');
        tr.hide();
        tr.find('input').attr('value', '');
    });

    // rcon commands stuff
    var rcon_number = 1;
    $('#addCommand').html('<p><button class="button" type="button">Add rcon command</button></p>');
    $('#addCommand button').click(function() {
        var selected_command = $('#rcon_commands_select :selected').text();
        var table = $('#addCommand').parent().find('tbody');
        table.append('<tr> \
                        <th><label for="new-' + selected_command + '-' + rcon_number + '">' + selected_command + ':</label></th> \
                        <td><input type="text" name="new-' + selected_command + '-' + rcon_number + '" value="command" id="new-' + selected_command + '-' + rcon_number + '"></td> \
                        <td><div class="deleteCommand"><div class="delButton" onclick=""></div></div></td> \
                    </tr>');
        rcon_number++;
    });

    $('.deleteCommand').html('<div class="delButton" onclick=""></div>');
    $(document).on('click', '.deleteCommand div.delButton', function() {
        var tr = $(this).parents('tr');
        tr.hide();
        tr.find('input').attr('value', '');
    });

    // menu cookie
    var active_menus_cookie = get_active_menus_cokkie();
    //$.cookie("active_menus", "[]", { path: '/' });

    // open menu depended of the cookie
    $('.menu_head').each(function() {
        var menu = $(this);
        var menu_ul = $(this).find('ul');
        var server_id = $(this).attr("data-serverid");

        if($.inArray(server_id, active_menus_cookie) > -1) {
            $(menu_ul).css('display', 'block');

            var icon = $(menu).find('i:first');
            if($(icon).attr('class') == 'icon-chevron-right') {
                $(icon).attr('class', 'icon-chevron-down');
            }
        }
    });

    // menu slider
    $('.menu_head p').click(function() {
        var menu = $(this);
        var menu_ul = $(this).parent('.menu_head').find('ul');
        var server_id = $(this).parent('.menu_head').attr("data-serverid");
        $(menu_ul).slideToggle('fast');

        var array_index = $.inArray(server_id, active_menus_cookie);
        if(menu_ul.css('display') == 'block' && array_index == -1) {  // menu is closed
            $(menu).find('i:first').attr('class', 'icon-chevron-down');
            active_menus_cookie.push(server_id);
            $.cookie("active_menus", JSON.stringify(active_menus_cookie), { path: '/' });
        }
        else if(array_index > -1) {  // menu is open
            $(menu).find('i:first').attr('class', 'icon-chevron-right');
            active_menus_cookie.splice(array_index, 1);
            $.cookie("active_menus", JSON.stringify(active_menus_cookie), { path: '/' });
        }
    });

    // menu user settings
    $('#userMenu .icon-gear').click(function() {
        $('#usermenuBox').toggle();
        $('#userMenu .arrow').toggle();
    });

    // terminal interval
    (function receive_terminal_interval() {
        receive_entries();

        setTimeout(receive_terminal_interval, 1000);
    })();

    // event calende
    {
        var current_date = new calendarDate(new Date());
        calendarInit(current_date);
        calendarGetData(current_date);

        $('.calendarHead .arrowLeft').click(function() {
            current_date = changeMonth(current_date, -1);
            calendarGetData(current_date);
        });

        $('.calendarHead .arrowRight').click(function() {
            current_date = changeMonth(current_date, 1);
            calendarGetData(current_date);
        });

        $('.calendarDayListContainer').on('click', '.calendarDayListItem .day:not(:empty)', function() {
            if($(this).attr('class') == 'day fill')
                return;

            var day_list = $(this).parent('.calendarDayListContainer .calendarDayListItem');
            var year = $(day_list).attr('data-year');
            var month = $(day_list).attr('data-month');
            var day = parseInt($(this).html(), 10);
            var date = new Date(year, parseInt(month, 10)-1, day);

            (function calendarCheckEventDetails() {
                var ret = calendarGetEventDetails(date, 0);

                if(!ret)
                    setTimeout(calendarCheckEventDetails, 10);
            })();
        });

        $('.calendarHead .addEventButton').click(function() {
            calendarAddEvent();
        });
    }
});

function get_active_menus_cokkie() {
    var active_menus_cookie;
    try {
        active_menus_cookie = $.parseJSON($.cookie("active_menus"));
    }
    catch (e) {
        active_menus_cookie = [];
    }
    if(!active_menus_cookie)
        active_menus_cookie = [];

    return active_menus_cookie;
}

// terminal stuff
var command_list = [];
var command_list_index = 0;

$(document).keypress(function(e) {
    if (e.which == 13 && $('#terminalCommandInput:focus').length) {
        handle_input();
    }

    if (e.keyCode == 38 && $("#terminalCommandInput:focus").length) {
        rotate_commands(0);
    }
    
    if (e.keyCode == 40 && $("#terminalCommandInput:focus").length) {
        rotate_commands(1);
    }
});

function handle_input() {
    var command = $('#terminalCommandInput').val();
    if (command === '') return;
    command_list.push(command);
    command_list_index = command_list.length;
    $('#terminalCommandInput').val('');
    send_command(command);
}

function add_entry(line) {
    var data = '<p>' + line + '</p>';
    $('#terminalEntry').append(data);
    $('#terminalEntry').animate({
        scrollTop: $('#terminalEntry')[0].scrollHeight
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
            $('#terminalCommandInput').val(command_list[command_list_index]);
        }
    }
    else {
        if(command_list_index < command_list.length) {
            command_list_index++;
            $('#terminalCommandInput').val(command_list[command_list_index]);
        }
        else {
            $('#terminalCommandInput').val('');
        }
    }
}
