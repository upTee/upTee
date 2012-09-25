import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from mod.forms import MapUploadForm
from mod.models import Server
from settings import MEDIA_ROOT

def user_server_list(request):
    servers = None
    if request.user.is_authenticated():
        servers = Server.objects.filter(is_active=True).filter(owner=request.user)
        for server in servers:
            server.check_online()
    return render_to_response('mod/base.html', {'server_list': servers}, context_instance=RequestContext(request))

def server_list(request):
    servers = Server.objects.filter(is_active=True)
    for server in servers:
        server.check_online()
    return render_to_response('mod/servers.html', {'server_list': servers}, context_instance=RequestContext(request))

@login_required
def server_detail(request, mod_name):
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True).filter(owner=request.user), mod__title=mod_name)
    options = server.config_options.all()
    return render_to_response('mod/server_detail.html', {
        'server': server,
        'options': options,
    }, context_instance=RequestContext(request))

@login_required
def upload_map(request, mod_name):
    if request.method == 'POST':
        form = MapUploadForm(request.POST, request.FILES)
        if form.is_valid():
            map_file = form.cleaned_data['map_file']
            with open(os.path.join(MEDIA_ROOT, 'users', request.user.username, mod_name, 'data', 'maps', map_file.name), 'wb') as f:
                f.write(map_file.read())
            messages.success(request, 'Map was successfully uploaded.')
    else:
        form = MapUploadForm()
    return render_to_response('mod/upload_map.html', {
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
@require_POST
def start_stop_server(request, mod_name):
    next = request.REQUEST.get('next', reverse('home'))
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True).filter(owner=request.user), mod__title=mod_name)
    server.check_online()
    if server.is_online:
        server.set_offline()
    else:
        server.set_online()
    return render_to_response('mod/state_changed.html', {'next': next }, context_instance=RequestContext(request))

@login_required
@require_POST
def start_stop_server_by_id(request, server_id):
    server = get_object_or_404(Server.objects.select_related().filter(is_active=True), pk=server_id)
    user = request.user
    if not user.is_staff and server.owner != user:
        raise Http404
    next = request.REQUEST.get('next', reverse('server_list'))
    server.check_online()
    if server.is_online:
        server.set_offline()
    else:
        server.set_online()
    return render_to_response('mod/state_changed.html', {'next': next }, context_instance=RequestContext(request))

@login_required
@require_POST
def update_settings(request, mod_name):
    next = request.REQUEST.get('next', reverse('server_detail', kwargs={'mod_name': mod_name}))
    server = get_object_or_404(Server.objects.filter(is_active=True).filter(owner=request.user), mod__title=mod_name)
    options = server.config_options.all()
    for key in request.POST.keys():
        option = options.filter(command=key)[0] if options.filter(command=key) else None
        if option:
            option.value = request.POST[key]
            option.save()
    return render_to_response('mod/settings_updated.html', {'next': next }, context_instance=RequestContext(request))
