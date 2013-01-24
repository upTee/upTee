from django.conf.urls.defaults import *

urlpatterns = patterns('messaging.views',
    url(r'^contact/$', 'contact', name='contact'),
)
