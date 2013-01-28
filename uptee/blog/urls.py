from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',
    url(r'^$', 'blog_home', name='home'),
    url(r'^entry/(?P<slug>[-\w]+)/$', 'entry_detail', name='entry_detail'),
)
