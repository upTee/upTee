from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.defaults import page_not_found, permission_denied, server_error
from django.views.generic.simple import direct_to_template
import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('blog.urls')),
    url(r'^', include('mod.urls')),
    url(r'^', include('accounts.urls')),
    url(r'^', include('messaging.urls')),
    url(r'^about/$', direct_to_template, {'template': 'about.html'}, name='about'),
    url(r'^captcha/', include('captcha.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin_tools/', include('admin_tools.urls')),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('django.views.defaults',
        (r'^403/$', page_not_found),
        (r'^404/$', permission_denied),
        (r'^500/$', server_error),
    )
