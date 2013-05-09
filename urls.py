from django.conf.urls.defaults import *
from merkabah.urls import urlpatterns

import controllers as c

urlpatterns += patterns('controllers',
    url(r'^$', c.MainCtrl.as_django_view(), name=c.MainCtrl.view_name),
    url(r'^(?P<permalink>\d{4}/\d{2}/\d{2}/[\w-]+/)$', c.BlogPermalinkCtrl.as_django_view(), name=c.BlogPermalinkCtrl.view_name),

    url(r'^about/$', c.AboutCtrl.as_django_view(), name=c.AboutCtrl.view_name),
    url(r'^blog/$', c.BlogCtrl.as_django_view(), name=c.BlogCtrl.view_name),
    url(r'^blog/(?P<page_number>[0-9]+)/$', c.BlogCtrl.as_django_view(), name=c.BlogCtrl.view_name),    
        
    #url(r'^artwork/$', c.ArtworkCtrl.as_django_view(), name=c.ArtworkCtrl.view_name),
    #url(r'^software/$', c.SoftwareCtrl.as_django_view(), name=c.SoftwareCtrl.view_name),
    #url(r'^projects/$', c.ProjectsCtrl.as_django_view(), name=c.ProjectsCtrl.view_name),    
    url(r'^links/$', c.LinksCtrl.as_django_view(), name=c.LinksCtrl.view_name),
    url(r'^clients/$', c.ClientsCtrl.as_django_view(), name=c.ClientsCtrl.view_name),
    url(r'^contact/$', c.ContactCtrl.as_django_view(), name=c.ContactCtrl.view_name),
    
    url(r'^blog_image/(?P<blob_key>[A-Za-z0-9-_:=]+)/$', c.BlogPrimaryImageDisplay.as_django_view(), name=c.BlogPrimaryImageDisplay.view_name),
    url(r'^(?P<category_slug>[\w-]+)/$', c.BlogCategoryCtrl.as_django_view(), name=c.BlogCategoryCtrl.view_name),
)