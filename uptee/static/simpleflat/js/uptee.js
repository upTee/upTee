$(document).ready(function() {

    // notification closer
    $('.notificationClose').live('click', function() {
        $(this).parent().animate({opacity: 0, height: 0, paddingTop: 0, paddingBottom: 0, marginTop: 0}, 300, function() {
            $(this).remove();
        });
    });

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

    // vote stuff
    var vote_number = 1;
    $('#add_vote').html('<p><button class="button" type="button">Add vote</button></p>');
    $('#add_vote button').click(function() {
        var table = $('#add_vote').parent().find('tbody');
        table.append('<tr> \
                        <th><input type="text" name="title new title ' + vote_number + ' new" value="New vote" id="id-' + vote_number + '-title_new"></th> \
                        <td><input type="text" name="command new command ' + vote_number + ' new" value="command" id="id-' + vote_number + '-command_new"></td> \
                        <td><div class="delete_vote"><div class="del_button" onclick=""></div></div></td> \
                    </tr>');
        vote_number++;
    });

    $('.delete_vote').html('<div class="del_button" onclick=""></div>');
    $('.delete_vote div.del_button').live('click', function() {
        var tr = $(this).parents('tr');
        tr.hide();
        tr.find('input').attr('value', '');
    });

    // rcon commands stuff
    var rcon_number = 1;
    $('#add_command').html('<p><button class="button" type="button">Add rcon command</button></p>');
    $('#add_command button').click(function() {
        var selected_command = $('#rcon_commands_select :selected').text();
        var table = $('#add_command').parent().find('tbody');
        table.append('<tr> \
                        <th><label for="new-' + selected_command + '-' + rcon_number + '">' + selected_command + ':</label></th> \
                        <td><input type="text" name="new-' + selected_command + '-' + rcon_number + '" value="command" id="new-' + selected_command + '-' + rcon_number + '"></td> \
                        <td><div class="delete_command"><div class="del_button" onclick=""></div></div></td> \
                    </tr>');
        rcon_number++;
    });

    $('.delete_command').html('<div class="del_button" onclick=""></div>');
    $('.delete_command div.del_button').live('click', function() {
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