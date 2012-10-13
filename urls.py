from django.conf.urls.defaults import *

urlpatterns = patterns('views',
    (r'^$', 'index'),       
    (r'^main/$', 'homepage'),
    (r'^(?P<page_key>[A-Za-z0-9-_/:]+)/$', 'index'),       
)