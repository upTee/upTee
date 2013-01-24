from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.home', name='home'),
    url(r'^', include('mod.urls')),
    url(r'^', include('accounts.urls')),
    url(r'^', include('messaging.urls')),
    url(r'^about/$', 'views.about', name='about'),
    url(r'^captcha/', include('captcha.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin_tools/', include('admin_tools.urls')),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('views',
        (r'^403/$', 'custom_permission_denied'),
        (r'^404/$', 'custom_page_not_found'),
        (r'^500/$', 'custom_server_error'),
    )

# custom views for error pages
handler403 = 'views.custom_permission_denied'
handler404 = 'views.custom_page_not_found'
handler500 = 'views.custom_server_error'
