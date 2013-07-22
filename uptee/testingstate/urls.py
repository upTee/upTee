from django.conf.urls import *

urlpatterns = patterns('testingstate.views',
                       url(r'^generatetestingkeys/$', 'generate_testing_keys', name='generate_testing_keys'),
                       )