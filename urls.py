from django.conf.urls.defaults import *
from merkabah.urls import urlpatterns

import views

urlpatterns += patterns('views',
    url(r'^$', views.MainCtrl.as_view(), name=views.MainCtrl.view_name),

    #url(r'^(?P<permalink>\d{4}/\d{2}/\d{2}/[\w-]+/)$', views.BlogPermalinkCtrl.as_view(), name=views.BlogPermalinkCtrl.view_name),
    url(r'^(?P<permalink>\d{4}/\d{2}/\d{2}/[\w-]+/)$', views.BlogPermalinkCtrl.as_view(), name=views.BlogPermalinkCtrl.view_name),

    url(r'^about/$', views.AboutCtrl.as_view(), name=views.AboutCtrl.view_name),
    url(r'^blog/$', views.BlogCtrl.as_view(), name=views.BlogCtrl.view_name),
        
    url(r'^artwork/$', views.ArtworkCtrl.as_view(), name=views.ArtworkCtrl.view_name),
    url(r'^software/$', views.SoftwareCtrl.as_view(), name=views.SoftwareCtrl.view_name),
    url(r'^projects/$', views.ProjectsCtrl.as_view(), name=views.ProjectsCtrl.view_name),    
    url(r'^links/$', views.LinksCtrl.as_view(), name=views.LinksCtrl.view_name),
    url(r'^clients/$', views.ClientsCtrl.as_view(), name=views.ClientsCtrl.view_name),
    url(r'^contact/$', views.ContactCtrl.as_view(), name=views.ContactCtrl.view_name),
)