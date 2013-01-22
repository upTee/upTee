from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from views import home

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.home', name='home'),
    url(r'^', include('mod.urls')),
    (r'^', include('accounts.urls')),
    url(r'^about/$', 'views.about', name='about'),
    url(r'^captcha/', include('captcha.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin_tools/', include('admin_tools.urls')),
)

urlpatterns += staticfiles_urlpatterns()

# custom views for error pages
handler403 = 'views.custom_permission_denied'
handler404 = 'views.custom_page_not_found'
