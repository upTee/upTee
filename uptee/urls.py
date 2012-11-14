from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('mod.urls')),
    (r'^', include('accounts.urls')),
    url(r'^about/$', direct_to_template, {'template': 'about.html'}, name='about'),
    url(r'^captcha/', include('captcha.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin_tools/', include('admin_tools.urls')),
)

urlpatterns += staticfiles_urlpatterns()
