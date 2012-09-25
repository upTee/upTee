from django.conf.urls.defaults import *
from mod.models import Mod

urlpatterns = patterns('mod.views',
    url(r'^$', 'user_server_list', name='home'),
    url(r'^servers/$', 'server_list', name='server_list'),
    url(r'^server/(?P<mod_name>[-\w]+)/$', 'server_detail', name='server_detail'),
    url(r'^server/(?P<mod_name>[-\w]+)/uploadmap/$', 'upload_map', name='upload_map'),
    url(r'^startstopserver/(?P<mod_name>[-\w]+)/$', 'start_stop_server', name='start_stop_server'),
    url(r'^startstopserver/id/(?P<server_id>\d+)/$', 'start_stop_server_by_id', name='start_stop_server_by_id'),
    url(r'^updatesettings/(?P<mod_name>[-\w]+)/$', 'update_settings', name='update_settings'),
)
