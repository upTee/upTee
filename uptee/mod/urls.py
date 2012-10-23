from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from mod.models import Mod

urlpatterns = patterns('mod.views',
    url(r'^$', direct_to_template, {'template': 'base.html'}, name='home'),
    url(r'^servers/$', 'server_list', name='server_list'),
    url(r'^servers/(?P<username>[-\w]+)/$', 'user_server_list', name='user_server_list'),
    url(r'^server/(?P<server_id>\d+)/$', 'server_detail', name='server_detail'),
    url(r'^server/(?P<server_id>\d+)/edit/$', 'server_edit', name='server_edit'),
    url(r'^server/(?P<server_id>\d+)/uploadmap/$', 'upload_map', name='upload_map'),
    url(r'^startstopserver/(?P<server_id>\d+)/$', 'start_stop_server', name='start_stop_server'),
    url(r'^updatesettings/(?P<server_id>\d+)/$', 'update_settings', name='update_settings'),
    url(r'^server_info_update/(?P<server_id>\d+)/$', 'server_info_update_ajax', name='server_info_update_ajax'),
)
