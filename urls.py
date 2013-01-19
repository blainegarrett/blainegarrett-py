from django.conf.urls.defaults import *
from merkabah.urls import urlpatterns

import views

urlpatterns += patterns('views',
    url(r'^$', views.MainCtrl.as_django_view(), name=views.MainCtrl.view_name),
    url(r'^(?P<permalink>\d{4}/\d{2}/\d{2}/[\w-]+/)$', views.BlogPermalinkCtrl.as_django_view(), name=views.BlogPermalinkCtrl.view_name),

    url(r'^about/$', views.AboutCtrl.as_django_view(), name=views.AboutCtrl.view_name),
    url(r'^blog/$', views.BlogCtrl.as_django_view(), name=views.BlogCtrl.view_name),
    url(r'^blog/(?P<page_number>[0-9]+)/$', views.BlogCtrl.as_django_view(), name=views.BlogCtrl.view_name),    
        
    #url(r'^artwork/$', views.ArtworkCtrl.as_django_view(), name=views.ArtworkCtrl.view_name),
    #url(r'^software/$', views.SoftwareCtrl.as_django_view(), name=views.SoftwareCtrl.view_name),
    #url(r'^projects/$', views.ProjectsCtrl.as_django_view(), name=views.ProjectsCtrl.view_name),    
    url(r'^links/$', views.LinksCtrl.as_django_view(), name=views.LinksCtrl.view_name),
    url(r'^clients/$', views.ClientsCtrl.as_django_view(), name=views.ClientsCtrl.view_name),
    url(r'^contact/$', views.ContactCtrl.as_django_view(), name=views.ContactCtrl.view_name),
    
    url(r'^blog_image/(?P<blob_key>[A-Za-z0-9-_:=]+)/$', views.BlogPrimaryImageDisplay.as_django_view(), name=views.BlogPrimaryImageDisplay.view_name),
    url(r'^(?P<category_slug>[\w-]+)/$', views.BlogCategoryCtrl.as_django_view(), name=views.BlogCategoryCtrl.view_name),
)