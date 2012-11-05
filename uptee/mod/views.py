import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from annoying.decorators import ajax_request
from mod.forms import MapUploadForm
from mod.models import Map, Option, Server, Vote
from settings import MEDIA_ROOT


def server_list(request, username=None, server_type=None):
    if server_type:
        if server_type not in ['online', 'offline']:
            raise Http404
    if username:
        user = get_object_or_404(User.objects.filter(is_active=True), username=username)
        servers = Server.objects.filter(is_active=True, owner=user)
    else:
        servers = Server.objects.filter(is_active=True)
    for server in servers:
        server.check_online()
    if server_type:
        online = True if server_type == 'online' else False
        servers = (server for server in servers if server.is_online == online)
    return render_to_response('mod/servers.html', {'server_list': servers, 'username': username, 'server_type': server_type}, context_instance=RequestContext(request))


def server_detail(request, server_id):
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True), pk=server_id)
    return render_to_response('mod/server_detail_info.html', {
        'server': server
    }, context_instance=RequestContext(request))


@login_required
def server_edit(request, server_id):
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True, owner=request.user), pk=server_id)
    options = server.config_options.all()
    return render_to_response('mod/server_detail_edit.html', {
        'server': server,
        'options': options
    }, context_instance=RequestContext(request))


@login_required
def upload_map(request, server_id):
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True, owner=request.user), pk=server_id)
    if request.method == 'POST':
        form = MapUploadForm(request.POST, request.FILES)
        if form.is_valid():
            map_file = form.cleaned_data['map_file']
            mod_name = server.mod.title
            with open(os.path.join(MEDIA_ROOT, 'users', request.user.username, mod_name, 'data', 'maps', map_file.name), 'wb') as f:
                f.write(map_file.read())
            map_obj = Map(server=server, name=os.path.splitext(map_file.name)[0])
            map_obj.save()
            messages.success(request, 'Map was successfully uploaded.')
    else:
        form = MapUploadForm()
    return render_to_response('mod/server_detail_upload_map.html', {
        'server': server,
        'form': form
    }, context_instance=RequestContext(request))


@login_required
def server_votes(request, server_id):
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True, owner=request.user), pk=server_id)
    if request.method == 'POST':
        vote = Vote(server=server, command='command', title='New vote')
        vote.save()
    votes = server.config_votes.all()
    return render_to_response('mod/server_detail_votes.html', {
        'server': server,
        'votes': votes
    }, context_instance=RequestContext(request))


@login_required
def server_tunes(request, server_id):
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True, owner=request.user), pk=server_id)
    tunes = server.config_tunes.all()
    if not tunes:
        raise Http404
    return render_to_response('mod/server_detail_tunes.html', {
        'server': server,
        'tunes': tunes
    }, context_instance=RequestContext(request))


@login_required
@require_POST
def start_stop_server(request, server_id):
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True), pk=server_id)
    user = request.user
    if not user.is_staff and server.owner != user:
        raise Http404
    next = request.REQUEST.get('next', reverse('user_server_list', kwargs={'username': server.owner.username}))
    server.check_online()
    if server.is_online:
        server.set_offline()
    else:
        server.set_online()
    return render_to_response('mod/state_changed.html', {'next': next}, context_instance=RequestContext(request))


@login_required
@require_POST
def update_settings(request, server_id):
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True), pk=server_id)
    if server.owner != request.user:
        raise Http404
    next = request.REQUEST.get('next', reverse('server_edit', kwargs={'server_id': server.id}))
    options = server.config_options.exclude(widget=Option.WIDGET_CHECKBOX)
    for key in request.POST.keys():
        option = options.filter(command=key)[0] if options.filter(command=key) else None
        if option:
            if option.widget == Option.WIDGET_TEXTAREA:
                option.value = request.POST[key].replace('\r\n', r'\n')
            else:
                option.value = request.POST[key]
            option.save()
    options = server.config_options.filter(widget=Option.WIDGET_CHECKBOX)
    for option in options:
        if option.command in request.POST.keys():
            option.value = '1'
        else:
            option.value = '0'
        option.save()
    return render_to_response('mod/settings_updated.html', {'next': next}, context_instance=RequestContext(request))


@login_required
@require_POST
def update_votes(request, server_id):
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True), pk=server_id)
    if server.owner != request.user:
        raise Http404
    next = request.REQUEST.get('next', reverse('server_votes', kwargs={'server_id': server.id}))
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
    """for vote in votes:
        vote_list = votes.filter(title=vote.title)
        if len(vote_list) > 1:
            vote_list = vote_list[1:]
            for item in vote_list:
                item.delete()"""
    return render_to_response('mod/settings_updated.html', {'next': next}, context_instance=RequestContext(request))


@login_required
@require_POST
def update_tunes(request, server_id):
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True), pk=server_id)
    if server.owner != request.user:
        raise Http404
    next = request.REQUEST.get('next', reverse('server_tunes', kwargs={'server_id': server.id}))
    tunes = server.config_tunes.all()
    if tunes:
        for key in request.POST.keys():
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
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True), pk=server_id)
    return {'server_info': server.info}
