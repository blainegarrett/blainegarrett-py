"""
BlaineGarrett.com main app urls
"""

from django.conf.urls.defaults import patterns, url
from merkabah.urls import urlpatterns

import controllers as c
from plugins.blog.controllers import public as bc

urlpatterns += patterns('controllers',
    url(r'^$', *c.MainCtrl.django_url_args()),
    url(r'^(?P<permalink>\d{4}/\d{2}/\d{2}/[\w-]+/)$', *bc.BlogPermalinkCtrl.django_url_args()),

    url(r'^about/$', *c.AboutCtrl.django_url_args()),
    url(r'^blog/$', *bc.BlogCtrl.django_url_args()),
    url(r'^blog/(?P<page_number>[0-9]+)/$', *bc.BlogCtrl.django_url_args()),
        
    #url(r'^artwork/$', *c.ArtworkCtrl.django_url_args()),
    #url(r'^software/$', *c.SoftwareCtrl.django_url_args()),
    #url(r'^projects/$', *c.ProjectsCtrl.django_url_args()),
    url(r'^links/$', *c.LinksCtrl.django_url_args()),
    url(r'^clients/$', *c.ClientsCtrl.django_url_args()),
    url(r'^contact/$', *c.ContactCtrl.django_url_args()),

    #url(r'^upload/$', *c.UploadCtrl.django_url_args()),
    #url(r'^upload_endpoint/$', *c.UploadCtrlEndpoint.django_url_args()),

    #url(r'^blog_image/(?P<blob_key>[A-Za-z0-9-_:=]+)/$', *bc.BlogPrimaryImageDisplay.django_url_args()),
    url(r'^(?P<category_slug>[\w-]+)/$', *bc.BlogCategoryCtrl.django_url_args()),
)