import os
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from mod.forms import MapUploadForm
from mod.models import Option, Server
from settings import MEDIA_ROOT

def user_server_list(request, username):
    user = get_object_or_404(User.objects.filter(is_active=True), username=username)
    servers = Server.objects.filter(is_active=True, owner=user)
    for server in servers:
        server.check_online()
    return render_to_response('mod/base.html', {'server_list': servers}, context_instance=RequestContext(request))

def server_list(request):
    servers = Server.objects.filter(is_active=True)
    for server in servers:
        server.check_online()
    return render_to_response('mod/servers.html', {'server_list': servers}, context_instance=RequestContext(request))

def server_detail(request, username, mod_name):
    user = get_object_or_404(User.objects.filter(is_active=True), username=username)
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True, owner=user), mod__title=mod_name)
    options = server.config_options.filter(Q(command='sv_name') | Q(command='sv_gametype')).order_by('command')
    details = {
        'gametype': options[0].value if options[0].value else 'default',
        'name': options[1].value if options[1].value else 'unnamed server'
    }
    return render_to_response('mod/server_detail_info.html', {
        'server': server,
        'server_details': details
    }, context_instance=RequestContext(request))

@login_required
def server_edit(request, username, mod_name):
    if username != request.user.username:
        raise Http404
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True, owner=request.user), mod__title=mod_name)
    options = server.config_options.all()
    return render_to_response('mod/server_detail_edit.html', {
        'server': server,
        'options': options
    }, context_instance=RequestContext(request))

@login_required
def upload_map(request, username, mod_name):
    if username != request.user.username:
        raise Http404
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True, owner=request.user), mod__title=mod_name)
    if request.method == 'POST':
        form = MapUploadForm(request.POST, request.FILES)
        if form.is_valid():
            map_file = form.cleaned_data['map_file']
            with open(os.path.join(MEDIA_ROOT, 'users', request.user.username, mod_name, 'data', 'maps', map_file.name), 'wb') as f:
                f.write(map_file.read())
            messages.success(request, 'Map was successfully uploaded.')
    else:
        form = MapUploadForm()
    return render_to_response('mod/server_detail_upload_map.html', {
        'server': server,
        'form': form
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
    return render_to_response('mod/state_changed.html', {'next': next }, context_instance=RequestContext(request))

@login_required
@require_POST
def update_settings(request, server_id):
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True), pk=server_id)
    if server.owner != request.user:
        raise Http404
    next = request.REQUEST.get('next', reverse('server_detail', kwargs={'username': server.owner.username, 'mod_name': server.mod.title}))
    options = server.config_options.all()
    for key in request.POST.keys():
        option = options.filter(command=key)[0] if options.filter(command=key) else None
        if option:
            if option.widget == Option.WIDGET_TEXTAREA:
                option.value = request.POST[key].replace('\r\n', r'\n')
            else:
                option.value = request.POST[key]
            option.save()
    return render_to_response('mod/settings_updated.html', {'next': next }, context_instance=RequestContext(request))
