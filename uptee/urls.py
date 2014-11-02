from django.conf.urls import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.defaults import page_not_found, permission_denied, server_error
from django.views.generic import TemplateView
import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('blog.urls')),
    url(r'^', include('mod.urls')),
    url(r'^', include('accounts.urls')),
    url(r'^', include('messaging.urls')),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^captcha/', include('captcha.urls')),
    (r'^comments/', include('django_comments.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin_tools/', include('admin_tools.urls')),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('django.views.defaults',
        (r'^403/$', permission_denied),
        (r'^404/$', page_not_found),
        (r'^500/$', server_error),
    )
    try:
        __import__('debug_toolbar')
    except ImportError:
        pass
    else:
        import debug_toolbar
        urlpatterns += patterns('',
            url(r'^__debug__/', include(debug_toolbar.urls)),
        )

if settings.TESTING_STATE:
    urlpatterns += patterns('',
        url(r'^', include('testingstate.urls')),
    )
