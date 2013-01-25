from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^register/$', 'register', name='register'),
    url(r'^settings/$', 'settings', name='settings'),
    url(r'^settings/password/$', 'change_password', name='change_password'),
    url(r'^users/$', 'users', name='users'),
    url(r'^user/(?P<user_id>\d+)$', 'user', name='user'),
)
