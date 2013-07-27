var calendar_last_action = new Date();
var events_json = {};
var calendar_loading = [0,0]; // for saving the loading state
var calendar_current_date;

function calendarDate(date) {
    this.date = date;

    this.daysOfMonth = function() {
        return 32 - new Date(this.date.getFullYear(), this.date.getMonth(), 32).getDate();
    };

    this.firstDayOfMonth = function() {
        return new Date(this.date.getFullYear(), this.date.getMonth(), 1).getDay();
    };

    this.lastDayOfMonth = function() {
        return new Date(this.date.getFullYear(), this.date.getMonth(), 1).getDay();
    };

    this.monthName = function() {
        var month_names = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ];
        return month_names[this.date.getMonth()];
    };
}

function calendarInit(current_date) {
    calendar_current_date = current_date.date;

    $('.calendarHead .month').html(current_date.monthName());
    $('.calendarHead .year').html(current_date.date.getFullYear());

    $('.calendarBody .calendarDayListItem').html(drawMonth(current_date));
    $('.calendarBody .calendarDayListItem').attr({'data-month': current_date.date.getMonth()+1, 'data-year': current_date.date.getFullYear()});
}

function drawMonth(calendar_date) {
    var day_list = '';
    var day_num = 0;
    for(var i = 1; i <= calendar_date.firstDayOfMonth()-1+calendar_date.daysOfMonth(); i++) {
        // days
        var day_data = '';
        if(i >= calendar_date.firstDayOfMonth()) {
            day_num++;
            day_data = day_num;
        }

        // sunday
        var sunday_class = '';
        if(i % 7 === 0) {
            sunday_class = ' sun';
        }

        // current
        var current_class = '';
        var today = new Date();
        if(day_num == today.getDate() && today.getFullYear() == calendar_date.date.getFullYear() && today.getMonth() == calendar_date.date.getMonth()) {
            current_class = ' current';
        }

        day_list += '<div class="day' + sunday_class + current_class + '">' + day_data + '</div>';
    }

    return day_list;
}

function changeMonth(current_date, direction) { // -1 left, +1 right
    // check last action
    var skip_animation = 0;
    var action_now = new Date();
    if(action_now.getTime() - calendar_last_action.getTime() < 450)
        skip_animation = 1;
    calendar_last_action = action_now;

    // get a next month date
    current_date = new calendarDate(new Date(current_date.date.getFullYear(), current_date.date.getMonth()+direction, 12));

    // draw the month
    var extra_attr = 'data-month="' + (current_date.date.getMonth()+1) + '" data-year="' + current_date.date.getFullYear() + '"';
    if(direction == 1) {
        $('.calendarBody .calendarDayLists').append('<div class="calendarDayListItem" ' + extra_attr + '></div>');
        $('.calendarBody .calendarDayListItem:last').html(drawMonth(current_date));
    } else {
        $('.calendarBody .calendarDayLists').prepend('<div class="calendarDayListItem" ' + extra_attr + '></div>');
        $('.calendarBody .calendarDayListItem:first').html(drawMonth(current_date));
        $('.calendarBody .calendarDayLists').css('left', '-280px');
    }

    // change calendar header
    $('.calendarHead .month').html(current_date.monthName());
    $('.calendarHead .year').html(current_date.date.getFullYear());

    // animate
    if(!skip_animation) {
        var css_left = '0px';
        if(direction == 1)
            css_left = '-280px';
        $('.calendarBody .calendarDayLists').animate({left: css_left}, 400, 'easeOutExpo', function() {
            if(direction == 1)
                $('.calendarBody .calendarDayListItem:first').remove();
            else
                $('.calendarBody .calendarDayListItem:last').remove();
            $('.calendarBody .calendarDayLists').css('left', '0');
        });
    } else {
        $('.calendarBody .calendarDayLists').css('left', '0');
        if(direction == 1)
            $('.calendarBody .calendarDayListItem:first').remove();
        else
            $('.calendarBody .calendarDayListItem:last').remove();
    }

    return current_date;
}

function fillEvents(date) {
    var day_list = $('.calendarBody .calendarDayListItem[data-year="' + date.getFullYear() + '"][data-month="' + (date.getMonth()+1) + '"]');
    var days = $(day_list).children('.day:not(:empty)');
    var data = events_json[date.getFullYear()+'-'+(date.getMonth()+1)];

    $(days).each(function(i) {
        var day_index = i+1;

        for(var j = 0; j < data.length; j++) {
            var event = data[j];

            if(day_index == event.date.getDate()) {
                var day = this;
                var event_element = $(day).children('.event');
                if(!event_element.length)
                    $(day).append('<div class="event ' + event.status + '"></div>');
                else {
                    var found = 0;
                    $(event_element).each(function() {
                        var event_class = $(this).attr('class');
                        if(event_class.indexOf(event.status) !== -1)
                            found = 1;
                    });
                    if(!found)
                        $(day).append('<div class="event ' + event.status + '"></div>');
                }
            }
        }
    });
}

function calendarGetEventDetails(date, tomorrow) {
    if(calendar_loading[0] || calendar_loading[1]) {
        return 0;
    }

    if(!tomorrow)
        calendar_current_date = date;

    var month_events = events_json[date.getFullYear()+'-'+(date.getMonth()+1)];
    var day_events = [];
    var today = new Date();
    var event;

    for(var i = 0; i < month_events.length; i++) {
        event = month_events[i];

        if(event.date.getDate() == date.getDate()) {
            day_events.push(event);
        }
    }

    var html_str;
    if(day_events.length) {
        html_str = '<div class="event headline">Events for ' + (date.getMonth()+1) + '/' + date.getDate() + '/' + date.getFullYear() + '</div>';
        if(tomorrow)
            html_str = '<div class="event headline">Events for tomorrow</div>';
        else if(today.toDateString() == date.toDateString())
            html_str = '<div class="event headline">Events for today</div>';
    } else {
        html_str = '<div class="event headline">No events for ' + (date.getMonth()+1) + '/' + date.getDate() + '/' + date.getFullYear() + '</div>';
        if(tomorrow)
            html_str = '<div class="event headline">No events for tomorrow</div>';
        else if(today.toDateString() == date.toDateString())
            html_str = '<div class="event headline">No events for today</div>';
    }

    for(var j = 0; j < day_events.length; j++) {
        event = day_events[j];

        var hours = event.date.getHours();
        if(hours <= 9)
            hours = '0' + hours;
        var minutes = event.date.getMinutes();
        if(minutes <= 9)
            minutes = '0' + minutes;
        html_str += '<div class="event">' + (event.date.getMonth()+1) + '/' + event.date.getDate() + '/' + event.date.getFullYear() + ' | ' + hours + ':' + minutes + ' ' + event.title + '</div>';
    }

    var selector_str = '#calendarContainer .eventsDay';
    if(tomorrow)
        selector_str = '#calendarContainer .eventsUpcoming';

    // remove old data
    if(!tomorrow) {
        $('#calendarContainer .eventsDay').html('');
        $('#calendarContainer .eventsUpcoming').html('');
    }

    $(selector_str).css('display', 'none');
    $(selector_str).html(html_str);
    $(selector_str).fadeIn('fast');

    return 1;
}

function calendarGetData(calendar_date) {
    var date = calendar_date.date;
    var next_day = new Date(date.getFullYear(), date.getMonth(), date.getDate()+1);
    var today = new Date();

    if(!events_json.hasOwnProperty(date.getFullYear()+'-'+(date.getMonth()+1))) {
        // loading animation
        $('.calendarHead .preLoader').css('display', 'inline-block');

        var server_id = $('#calendarContainer').attr('data-serverid');
        var get_parameter = '?year='+date.getFullYear()+'&month='+(date.getMonth()+1);
        var animation_state = [1,1];

        calendar_loading[0] = 1;
        $.ajax({
            url: '/server/' + server_id + '/events/' + get_parameter,
            type: 'GET',
            success: function(data) {
                for(var i = 0; i < data.length; i++) {
                    data[i].date = new Date(parseInt(data[i].date, 10));
                }
                events_json[date.getFullYear()+'-'+(date.getMonth()+1)] = data;
                fillEvents(date);
                calendar_loading[0] = 0;
                if(today.toDateString() == date.toDateString()) {
                    calendarGetEventDetails(date, 0);
                    if(date.getDate() != calendar_date.daysOfMonth())
                        calendarGetEventDetails(next_day, 1);
                }
                animation_state[0] = 0;
                if(animation_state[1] === 0)
                    $('.calendarHead .preLoader').css('display', 'none');
            }
        });

        // load next month if it is the last day of the month to be able to show tomorrows events
        if(date.getDate() == calendar_date.daysOfMonth()) {
            date = next_day;
            get_parameter = '?year='+date.getFullYear()+'&month='+(date.getMonth()+1);

            calendar_loading[1] = 1;
            $.ajax({
                url: '/server/' + server_id + '/events/' + get_parameter,
                type: 'GET',
                success: function(data) {
                    for(var i = 0; i < data.length; i++) {
                        data[i].date = new Date(parseInt(data[i].date, 10));
                    }
                    events_json[date.getFullYear()+'-'+(date.getMonth()+1)] = data;
                    fillEvents(date);
                    calendar_loading[1] = 0;
                    calendarGetEventDetails(date, 1);
                    animation_state[1] = 0;
                    if(animation_state[0] === 0)
                        $('.calendarHead .preLoader').css('display', 'none');
                }
            });
        } else {
            animation_state[1] = 0;
            if(animation_state[0] === 0)
                $('.calendarHead .preLoader').css('display', 'none');
        }
    } else {
        fillEvents(date);
    }
}

function calendarAddEvent() {
    var server_id = $('#calendarContainer').attr('data-serverid');

    $.ajax({
        url: '/server/' + server_id + '/events/add',
        type: 'GET',
        success: function(data) {
            $('#calendarContainer').children('.addEvent').html(data);
            calendarHandleEventForm(server_id);
        }
    });
}

function calendarHandleEventForm(server_id) {
    var test = $('#calendarContainer').children('.addEvent').find('.button');
    $('#calendarContainer form input.button').live('click', function(e) {
        e.preventDefault();

        // set the value for the hidden field
        var date_val = $('#id_date_input').val();
        $('#id_date').val((calendar_current_date.getMonth()+1) + '/' + calendar_current_date.getDate() + '/' + calendar_current_date.getFullYear() + ' ' + date_val);

        var input_data = $('#calendarContainer form :input');

        $.ajax({
            beforeSend: function(jqXHR, settings) {
                var csrftoken = $.cookie('csrftoken');
                jqXHR.setRequestHeader('X-CSRFToken', csrftoken);
            },
            type: "POST",
            url: '/server/' + server_id + '/events/add/',
            data: input_data.serialize(), // serializes the form's elements.
            success: function(data)
            {
                if(!data.hasOwnProperty('event_id')) {
                    $('#calendarContainer').children('.addEvent').html(data);
                }
                else {
                    $('#calendarContainer').children('.addEvent').html('<div class="notification_s success">Event successfully added!<div class="notification_close"></div></div>');
                    var date;
                    var time = date_val.split(':');
                    if(time.length > 2)
                        date = new Date(calendar_current_date.getFullYear(), calendar_current_date.getMonth(), calendar_current_date.getDate(), time[0], time[1], time[2]);
                    else
                        date = new Date(calendar_current_date.getFullYear(), calendar_current_date.getMonth(), calendar_current_date.getDate(), time[0], time[1]);
                    var new_event = {
                        "date": date,
                        "type": input_data[1][parseInt(input_data[1].value, 10)-1].text,
                        "title": input_data[0].value,
                        "server_id": server_id+'',
                        "repeat": parseInt(input_data[4].value, 10),
                        "event_id": data.event_id,
                        "status": "active"
                    };
                    events_json[date.getFullYear()+'-'+(date.getMonth()+1)].push(new_event);
                    var events = events_json[date.getFullYear()+'-'+(date.getMonth()+1)];
                    events_json[date.getFullYear()+'-'+(date.getMonth()+1)] = $(events).sort(calendarSortJson);

                    // update events for the selected date
                    calendarGetEventDetails(date, 0);

                    // update calender
                    fillEvents(date);
                }
            }
        });
    });
}

function calendarSortJson(a, b) {
    return a.date > b.date ? 1 : -1;
}
