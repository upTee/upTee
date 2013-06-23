from django.conf.urls import *

urlpatterns = patterns('messaging.views',
    url(r'^contact/$', 'contact', name='contact'),
)
