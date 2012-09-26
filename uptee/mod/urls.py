from django.conf.urls.defaults import *
from mod.models import Mod

urlpatterns = patterns('mod.views',
    url(r'^$', 'user_server_list', name='home'),
    url(r'^servers/$', 'server_list', name='server_list'),
    url(r'^servers/(?P<username>[-\w]+)/$', 'user_server_list', name='user_home'),
    url(r'^server/(?P<username>[-\w]+)/(?P<mod_name>[-\w]+)/$', 'server_detail', name='server_detail'),
    url(r'^server/(?P<username>[-\w]+)/(?P<mod_name>[-\w]+)/edit/$', 'server_edit', name='server_edit'),
    url(r'^server/(?P<username>[-\w]+)/(?P<mod_name>[-\w]+)/uploadmap/$', 'upload_map', name='upload_map'),
    url(r'^startstopserver/(?P<server_id>\d+)/$', 'start_stop_server', name='start_stop_server'),
    url(r'^updatesettings/(?P<server_id>\d+)/$', 'update_settings', name='update_settings'),
)
