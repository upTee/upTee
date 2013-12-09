import os
from calendar import timegm
from datetime import datetime, timedelta
from time import time
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.views.decorators.http import require_POST
from annoying.decorators import ajax_request
from econ.tasks import telnet_client
from lib.invalidate import invalidate
from lib.session_user import get_user
from mod.forms import CommandForm, ChangeModForm, MapUploadForm, ModeratorForm, ServerDescriptionForm, TaskEventForm
from mod.models import Map, Option, RconCommand, Server, Vote, TaskEvent
from mod.tasks import restart_server, start_server, stop_server
from settings import MEDIA_ROOT


def server_list(request, username=None, server_status=None):
    if username:
        user = get_object_or_404(User.objects.filter(is_active=True), username=username)
        servers = Server.active.filter(owner=user)
    else:
        servers = Server.active.all()
    if server_status:
        online = True if server_status == 'online' else False
        servers = (server for server in servers if server.is_online == online)
    return render_to_response('mod/servers.html', {
        'server_list': servers,
        'username': username,
        'server_type': server_status
    }, context_instance=RequestContext(request))


def server_detail(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    moderator = server.moderators.filter(user=request.user) if request.user.is_authenticated() else None
    moderator = moderator[0] if moderator else None
    return render_to_response('mod/server_detail_info.html', {
        'server': server,
        'moderator': moderator,
    }, context_instance=RequestContext(request))


def server_scoreboard(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    moderator = server.moderators.filter(user=request.user) if request.user.is_authenticated() else None
    moderator = moderator[0] if moderator else None
    return render_to_response('mod/server_detail_scoreboard.html', {
        'server': server,
        'moderator': moderator
    }, context_instance=RequestContext(request))


@login_required
def server_edit_description(request, server_id):
    server = get_object_or_404(Server.active.select_related().filter(owner=request.user), pk=server_id)
    form = ServerDescriptionForm(instance=server)
    if request.method == 'POST':
        form = ServerDescriptionForm(request.POST, instance=server)
        if form.is_valid():
            form.save()
            next = request.REQUEST.get('next', reverse('server_detail', kwargs={'server_id': server.id}))
            return render_to_response('mod/description_updated.html', {'next': next}, context_instance=RequestContext(request))
    return render_to_response('mod/server_edit_description.html', {
        'server': server,
        'description_form': form
    }, context_instance=RequestContext(request))


@login_required
def server_moderators(request, server_id):
    server = get_object_or_404(Server.active.select_related().filter(owner=request.user), pk=server_id)
    form = ModeratorForm(request.user, server)
    if request.method == 'POST':
        form = ModeratorForm(request.user, server, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Moderator successfully added.')
    return render_to_response('mod/server_detail_moderators.html', {
        'server': server,
        'moderator_form': form,
        'moderator': None
    }, context_instance=RequestContext(request))


@login_required
def server_edit_moderator(request, server_id, user_id):
    server = get_object_or_404(Server.active.select_related().filter(owner=request.user), pk=server_id)
    moderator = get_object_or_404(server.moderators.select_related(), user__pk=user_id)
    if request.method == 'POST':
        option_set = request.GET.get('set', '')
        if 'form-delete-moderator' in request.POST.keys():
            moderator.delete()
            messages.success(request, 'Moderator successfully deleted.')
            return redirect(reverse(server_moderators, kwargs={'server_id': server.pk}))
        if not option_set or option_set == 'general':
            if 'restart_allowed' in request.POST.keys():
                moderator.restart_allowed = True
            else:
                moderator.restart_allowed = False
            if 'edit_automatic_restart_allowed' in request.POST.keys():
                moderator.edit_automatic_restart_allowed = True
            else:
                moderator.edit_automatic_restart_allowed = False
            if 'edit_map_download_allowed' in request.POST.keys():
                moderator.edit_map_download_allowed = True
            else:
                moderator.edit_map_download_allowed = False
            if 'console_allowed' in request.POST.keys():
                moderator.console_allowed = True
            else:
                moderator.console_allowed = False
            if 'edit_votes_allowed' in request.POST.keys():
                moderator.edit_votes_allowed = True
            else:
                moderator.edit_votes_allowed = False
            if 'map_upload_allowed' in request.POST.keys():
                moderator.map_upload_allowed = True
            else:
                moderator.map_upload_allowed = False
            if 'edit_rcon_commands_allowed' in request.POST.keys():
                moderator.edit_rcon_commands_allowed = True
            else:
                moderator.edit_rcon_commands_allowed = False
        if not option_set or option_set == 'options':
            for option in moderator.allowed_options.all():
                if option.command not in request.POST.keys():
                    moderator.allowed_options.remove(option)
        if not option_set or option_set == 'tunings':
            for tune in moderator.allowed_tunings.all():
                if tune.command not in request.POST.keys():
                    moderator.allowed_tunings.remove(tune)
        for key in request.POST.keys():
            if key == 'csrfmiddlewaretoken':
                continue
            if not option_set or option_set == 'options':
                option = moderator.allowed_options.filter(command=key)
                if not option:
                    option = server.config_options.filter(command=key)
                    if option:
                        moderator.allowed_options.add(option[0])
                else:
                    continue
            if not option_set or option_set == 'tunings':
                tune = moderator.allowed_tunings.filter(command=key)
                if not tune:
                    tune = server.config_tunes.filter(command=key)
                    if tune:
                        moderator.allowed_tunings.add(tune[0])
        moderator.save()
        messages.success(request, 'Moderator successfully updated.')
    return render_to_response('mod/server_edit_moderator.html', {
        'server': server,
        'moderator_settings': moderator,
        'moderator': None
    }, context_instance=RequestContext(request))


@login_required
def server_edit(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    moderator = server.moderators.filter(user=request.user)
    if server.owner != request.user and not moderator:
        raise Http404
    moderator = moderator[0] if moderator else None
    if server.owner != request.user and moderator:
        options = moderator.allowed_options.all()
        if not options:
            raise Http404
    else:
        options = server.config_options.all()
    return render_to_response('mod/server_detail_edit.html', {
        'server': server,
        'options': options,
        'moderator': moderator
    }, context_instance=RequestContext(request))


@login_required
def upload_map(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    moderator = server.moderators.filter(user=request.user)
    if server.owner != request.user and (not moderator or not moderator[0].map_upload_allowed):
        raise Http404
    moderator = moderator[0] if moderator else None
    if request.method == 'POST':
        form = MapUploadForm(request.POST, request.FILES)
        if form.is_valid():
            map_file = form.cleaned_data['map_file']
            mod_name = server.mod.title
            maps_path = os.path.join(MEDIA_ROOT, 'mods', mod_name, 'servers', server.owner.username, '{0}'.format(server_id), server.random_key, 'maps')
            if not os.path.exists(maps_path):
                os.makedirs(maps_path)
            with open(os.path.join(maps_path, map_file.name), 'wb') as f:
                f.write(map_file.read())
            map_obj = Map(server=server, name=os.path.splitext(map_file.name)[0])
            map_obj.save()
            messages.success(request, 'Map was successfully uploaded.')
    else:
        form = MapUploadForm()
    return render_to_response('mod/server_detail_upload_map.html', {
        'server': server,
        'form': form,
        'moderator': moderator
    }, context_instance=RequestContext(request))


def map_download(request, map_id):
    map_obj = get_object_or_404(Map, pk=map_id, server__is_active=True)
    server = map_obj.server
    moderator = server.moderators.filter(user=request.user) if request.user.is_authenticated() else None
    password = server.config_options.filter(command='password')
    password = password[0].get_value() if password else ''
    if server.owner != request.user and (not server.map_download_allowed or password) and not moderator:
        raise Http404
    map_path = map_obj.get_download_url()
    if not map_path:
        raise Http404
    map_obj.download_count += 1
    map_obj.save()
    map_name = os.path.basename(map_path)
    fsock = open(map_path, 'rb')
    response = HttpResponse(fsock, mimetype='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(map_name)
    return response


def map_details(request, map_id):
    map_obj = get_object_or_404(Map, pk=map_id, server__is_active=True)
    return render_to_response('mod/map_details.html', {
        'map_obj': map_obj,
    }, context_instance=RequestContext(request))


def config_download(request, server_id):
    server = get_object_or_404(Server.active, pk=server_id)
    server.save_config(download=True)
    fsock = open(os.path.join(MEDIA_ROOT, 'mods', server.mod.title, 'servers', server.owner.username, '{0}'.format(server.id), server.random_key, 'generated.cfg'), 'rb')
    response = HttpResponse(fsock, mimetype='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=config.cfg'
    return response


@login_required
@require_POST
def delete_map(request, map_id):
    map_obj = get_object_or_404(Map, pk=map_id)
    if map_obj.server.owner != request.user:
        raise Http404
    next = request.REQUEST.get('next', reverse('server_detail', kwargs={'server_id': map_obj.server.id}))
    map_obj.delete()
    return render_to_response('mod/map_deleted.html', {'next': next}, context_instance=RequestContext(request))


@login_required
def server_edit_votes(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    moderator = server.moderators.filter(user=request.user)
    if server.owner != request.user and (not moderator or not moderator[0].edit_votes_allowed):
        raise Http404
    moderator = moderator[0] if moderator else None
    if request.method == 'POST':
        vote = Vote(server=server, command='command', title='New vote')
        vote.save()
    votes = server.config_votes.all()
    return render_to_response('mod/server_detail_edit_votes.html', {
        'server': server,
        'votes': votes,
        'moderator': moderator
    }, context_instance=RequestContext(request))


@login_required
def server_edit_rcon_commands(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    available_rcon_commands = server.config_available_rconcommands.all()
    if not available_rcon_commands:
        raise Http404
    moderator = server.moderators.filter(user=request.user)
    if server.owner != request.user and (not moderator or not moderator[0].edit_rcon_commands_allowed):
        raise Http404
    moderator = moderator[0] if moderator else None
    rcon_commands = server.config_rconcommands.all()
    return render_to_response('mod/server_detail_edit_rcon_commands.html', {
        'server': server,
        'rcon_commands': rcon_commands,
        'available_rcon_commands': available_rcon_commands,
        'moderator': moderator
    }, context_instance=RequestContext(request))


@login_required
def server_tunes(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    moderator = server.moderators.filter(user=request.user)
    if server.owner != request.user and not moderator:
        raise Http404
    moderator = moderator[0] if moderator else None
    if server.owner != request.user and moderator:
        tunes = moderator.allowed_tunings.all()
        if not tunes:
            raise Http404
    else:
        tunes = server.config_tunes.all()
    if not tunes:
        raise Http404
    return render_to_response('mod/server_detail_tunes.html', {
        'server': server,
        'tunes': tunes,
        'moderator': moderator
    }, context_instance=RequestContext(request))


@login_required
def server_change_mod(request, server_id):
    server = get_object_or_404(Server.active.select_related().filter(owner=request.user), pk=server_id)
    if request.method == 'POST':
        form = ChangeModForm(request.user, request.POST, instance=server)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mod was successfully changed.')
    else:
        form = ChangeModForm(request.user, initial={'mod': server.mod.pk})
    return render_to_response('mod/server_detail_change_mod.html', {
        'server': server,
        'form': form,
        'moderator': None
    }, context_instance=RequestContext(request))


@login_required
def server_console(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    if not server.is_online:
        raise Http404
    moderator = server.moderators.filter(user=request.user)
    if server.owner != request.user and (not moderator or not moderator[0].console_allowed):
        raise Http404
    moderator = moderator[0] if moderator else None
    cache.delete('server-{0}-in'.format(server_id))
    cache.delete('server-{0}-out'.format(server_id))
    cache.set('server-{0}-ping'.format(server_id), time())
    telnet_client.delay(server_id, server.port.port)
    return render_to_response('mod/server_detail_console.html', {
        'server': server,
        'moderator': moderator
    }, context_instance=RequestContext(request))


def server_votes(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    moderator = server.moderators.filter(user=request.user) if request.user.is_authenticated() else None
    moderator = moderator[0] if moderator else None
    votes = server.config_votes.all()
    if not votes:
        raise Http404
    return render_to_response('mod/server_detail_votes.html', {
        'server': server,
        'votes': votes,
        'moderator': moderator
    }, context_instance=RequestContext(request))


@login_required
@require_POST
def start_stop_server(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    moderator = server.moderators.filter(user=request.user)
    if server.owner != request.user and not request.user.is_staff and (not moderator or not moderator[0].restart_allowed):
        raise Http404
    next = request.REQUEST.get('next', reverse('user_server_list', kwargs={'username': server.owner.username}))
    map_exists = True
    if server.is_online:
        server.set_offline()
    else:
        if server.map_exists:
            server.set_online()
        else:
            map_exists = False
    return render_to_response('mod/state_changed.html', {'next': next, 'map_exists': map_exists}, context_instance=RequestContext(request))


@login_required
@require_POST
def update_settings(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    moderator = server.moderators.filter(user=request.user)
    if server.owner != request.user and not moderator:
        raise Http404
    moderator = moderator[0] if moderator else None
    next = request.REQUEST.get('next', reverse('server_edit', kwargs={'server_id': server.id}))
    options = server.config_options.exclude(widget__in=[Option.WIDGET_CHECKBOX, Option.WIDGET_SELECT])
    post = request.POST.copy()
    if server.owner == request.user or (moderator and moderator.edit_automatic_restart_allowed):
        if 'automatic_restart' in post.keys():
            server.automatic_restart = True
        else:
            server.automatic_restart = False
    if server.owner == request.user or (moderator and moderator.edit_map_download_allowed):
        if 'map_download_allowed' in post.keys():
            server.map_download_allowed = True
        else:
            server.map_download_allowed = False
    server.save()
    if 'automatic_restart' in post.keys():
        del post['automatic_restart']
    if 'map_download_allowed' in post.keys():
        del post['map_download_allowed']
    for key in post.keys():
        if server.owner != request.user:
            if not moderator.allowed_options.filter(command=key):
                continue
        option = options.filter(command=key)[0] if options.filter(command=key) else None
        if option:
            if option.widget == Option.WIDGET_TEXTAREA:
                option.value = post[key].replace('\r\n', r'\n')
            else:
                option.value = post[key]
            option.save()
    options = server.config_options.filter(widget=Option.WIDGET_CHECKBOX)
    for option in options:
        if server.owner != request.user:
            if not moderator.allowed_options.filter(command=key):
                continue
        if option.command in post.keys():
            option.value = '1'
        else:
            option.value = '0'
        option.save()
    options = server.config_options.filter(widget=Option.WIDGET_SELECT)
    for key in post.keys():
        if server.owner != request.user:
            if not moderator.allowed_options.filter(command=key):
                continue
        option = options.filter(command=key)[0] if options.filter(command=key) else None
        if option:
            selections = option.selections()
            if post[key] in selections:
                option.value = post[key]
                for selection in selections:
                    option.value += ',{0}'.format(selection)
                option.save()
    return render_to_response('mod/settings_updated.html', {'next': next}, context_instance=RequestContext(request))


@login_required
@require_POST
def update_votes(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    moderator = server.moderators.filter(user=request.user)
    if server.owner != request.user and not moderator:
        raise Http404
    moderator = moderator[0] if moderator else None
    if server.owner != request.user and not moderator.edit_votes_allowed:
        raise Http404
    next = request.REQUEST.get('next', reverse('server_edit_votes', kwargs={'server_id': server.id}))
    votes = server.config_votes.all()
    post = request.POST.copy()
    id_done_list = []
    title_done_list = []
    for key in post:
        if ' ' not in key:
            continue
        input_type = key.split(' ', 1)[0]
        if input_type not in ['title', 'command']:
            continue
        vote_id = key.rsplit(' ', 1)[-1]
        if vote_id == 'new':
            if not post[key]:
                continue
            vote_id = key.rsplit(' ', 2)[-2]
            if vote_id in id_done_list:
                continue
            if vote_id.isdigit:
                if input_type == 'title':
                    if post[key] in title_done_list:
                        continue
                    other = 'command'
                else:
                    other = 'title'
                vars()[input_type] = post[key]
                for _key in post:
                    if not post[_key] and ' ' not in _key:
                        continue
                    if _key.rsplit(' ', 1)[-1] == 'new' and _key.split(' ', 1)[0] == other:
                        check_id = key.rsplit(' ', 2)[-2]
                        if check_id == vote_id:
                            if input_type == 'command':
                                if post[_key] in title_done_list:
                                    break
                            vars()[other] = post[_key]
                            new_vote = Vote(server=server, command=vars()['command'], title=vars()['title'])
                            new_vote.save()
                            id_done_list.append(vote_id)
                            title_done_list.append(vars()['title'])
                            break
        elif vote_id.isdigit():
            if input_type == 'title':
                vote = votes.filter(title=post[key]).exclude(pk=vote_id)
                if vote:
                    vote.delete()
            vote = votes.filter(pk=vote_id)
            if len(vote) != 1:
                continue
            vote = vote[0]
            if not post[key]:
                vote.delete()
            else:
                setattr(vote, input_type, post[key])
                vote.save()
    return render_to_response('mod/settings_updated.html', {'next': next}, context_instance=RequestContext(request))


@login_required
@require_POST
def update_rcon_commands(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    moderator = server.moderators.filter(user=request.user)
    if server.owner != request.user and not moderator:
        raise Http404
    moderator = moderator[0] if moderator else None
    if server.owner != request.user and not moderator.edit_rcon_commands_allowed:
        raise Http404
    next = request.REQUEST.get('next', reverse('server_edit_rcon_commands', kwargs={'server_id': server.id}))
    rcon_commands = server.config_rconcommands.all()
    post = request.POST.copy()
    new_commands = []
    for key in post:
        if '-' not in key:
            continue
        if key[:4] == 'new-' and post[key]:
            new_commands.append((key[4:].rsplit('-', 1)[0], post[key]))
        else:
            rcon_id = key.rsplit('-', 1)[1]
            rcon_command = rcon_commands.filter(pk=rcon_id)
            rcon_command = rcon_command[0] if rcon_command else None
            if rcon_command:
                if post[key] and rcon_command.command == key.rsplit('-', 1)[0]:
                    rcon_command.value = post[key]
                    rcon_command.save()
                else:
                    rcon_command.delete()
    for command in new_commands:
        rcon_command = RconCommand(server=server, command=command[0], value=command[1])
        rcon_command.save()
    return render_to_response('mod/settings_updated.html', {'next': next}, context_instance=RequestContext(request))


@login_required
@require_POST
def update_tunes(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    moderator = server.moderators.filter(user=request.user)
    if server.owner != request.user and not moderator:
        raise Http404
    moderator = moderator[0] if moderator else None
    next = request.REQUEST.get('next', reverse('server_tunes', kwargs={'server_id': server.id}))
    tunes = server.config_tunes.all()
    if tunes:
        for key in request.POST.keys():
            if server.owner != request.user:
                if not moderator.allowed_tunings.filter(command=key):
                    continue
            tune = tunes.filter(command=key)[0] if tunes.filter(command=key) else None
            if tune:
                try:
                    tune.value = float(request.POST[key])
                except ValueError:
                    continue
                tune.save()
    return render_to_response('mod/settings_updated.html', {'next': next}, context_instance=RequestContext(request))


@ajax_request
def server_info_update_ajax(request, server_id):
    if not request.is_ajax():
        raise Http404
    invalidate(Server)
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    return {'server_info': server.server_info}


@ajax_request
@require_POST
def terminal_command_ajax(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    if not server.is_online:
        raise Http404
    user = get_user(request)
    if not user:
        raise Http404
    moderator = server.moderators.filter(user=user)
    if server.owner != user and (not moderator or not moderator[0].console_allowed):
        raise Http404
    form = CommandForm(request.POST)
    if not form.is_valid():
        raise Http404
    key = 'server-{0}-in'.format(server_id)
    lines = cache.get(key, [])
    lines.append(form.cleaned_data['command'])
    cache.set(key, lines)
    cache.set('server-{0}-ping'.format(server_id), time())
    return {}


@ajax_request
def terminal_receive_ajax(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    if not server.is_online:
        raise Http404
    user = get_user(request)
    if not user:
        raise Http404
    moderator = server.moderators.filter(user=user)
    if server.owner != user and (not moderator or not moderator[0].console_allowed):
        raise Http404
    cache.set('server-{0}-ping'.format(server_id), time())
    key = 'server-{0}-out'.format(server_id)
    lines = cache.get(key, [])
    cache.delete(key)
    cache.delete('server-{0}-terminate'.format(server_id))
    return {} if not lines else {"lines": lines}


@ajax_request
def events_ajax(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')
    day = request.GET.get('day', '')
    events = TaskEvent.objects.filter(server=server)
    if year and month and day:
        events = events.filter(date__year=year, date__month=month, date__day=day)
    elif year and month:
        events = events.filter(date__year=year, date__month=month)
    elif year:
        events = events.filter(date__day=year)
    events_json = [{
        "date": str(int(timegm(event.date.timetuple())*1000)),
        "type": event.get_task_type_display(),
        "title": event.name, "server_id": str(server_id),
        "repeat": str(event.repeat),
        "event_id": str(event.id),
        "status": event.get_status_display()
    } for event in events]
    return [] if not events else events_json


@ajax_request
@require_POST
def events_delete_ajax(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    user = get_user(request)
    if not user:
        raise Http404
    if server.owner != user:
        raise Http404
    event_id = request.POST.get('event_id', None)
    if not event_id:
        raise Http404
    event = get_object_or_404(TaskEvent.objects.all(), pk=event_id)
    event.delete()
    return {}


@ajax_request
def events_add_ajax(request, server_id):
    server = get_object_or_404(Server.active.select_related(), pk=server_id)
    user = get_user(request)
    if not user:
        raise Http404
    if server.owner != user:
        raise Http404
    form = TaskEventForm()
    if request.method == 'POST':
        form = TaskEventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            repeat = form.cleaned_data['repeat']
            task_type = form.cleaned_data['task_type']
            event = TaskEvent(server=server, name=name, task_type=task_type, date=date, repeat=repeat, status=TaskEvent.STATUS_ACTIVE)
            event.save()
            task = None
            if event.task_type == TaskEvent.TYPE_START:
                task = start_server.apply_async((event.id,), eta=event.date)
            elif event.task_type == TaskEvent.TYPE_STOP:
                task = stop_server.apply_async((event.id,), eta=event.date)
            elif event.task_type == TaskEvent.TYPE_RESTART:
                task = restart_server.apply_async((event.id,), eta=event.date)
            if task:
                event.task_id = task.task_id
            event.save()
            return {'event_id': event.id}
    return render_to_response('mod/event_form.html', {
        'server': server,
        'event_form': form
    }, context_instance=RequestContext(request))
