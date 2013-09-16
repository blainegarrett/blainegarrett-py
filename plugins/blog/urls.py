"""
Blog urls? Are these in use?
"""

"""
from django.conf.urls.defaults import patterns, url
from plugins.blog import views as blog_views

urlpatterns = patterns('plugins.admin.views',
    
    # Generic Blog urls - to, more dynamically generate these based on installed plugins
    url(r'^blog/$', blog_views.BlogIndexCtrl.as_django_view(), name=blog_views.BlogIndexCtrl.view_name),

    url(r'^blog/post/$', blog_views.BlogPostIndexCtrl.as_django_view(), name=blog_views.BlogPostIndexCtrl.view_name),
    url(r'^blog/post/add/$', blog_views.BlogPostCreateCtrl.as_django_view(), name=blog_views.BlogPostCreateCtrl.view_name),
    url(r'^blog/post/(?P<entity_key>[A-Za-z0-9-_:]+)/edit/$', blog_views.BlogPostEditCtrl.as_django_view(), name=blog_views.BlogPostEditCtrl.view_name),

    url(r'^blog/category/$', blog_views.BlogCategoryIndexCtrl.as_django_view(), name=blog_views.BlogCategoryIndexCtrl.view_name),
    url(r'^blog/category/add/$', blog_views.BlogCategoryCreateCtrl.as_django_view(), name=blog_views.BlogCategoryCreateCtrl.view_name),
    url(r'^blog/category/(?P<entity_key>[A-Za-z0-9-_:]+)/edit/$', blog_views.BlogCategoryEditCtrl.as_django_view(), name=blog_views.BlogCategoryEditCtrl.view_name),
 
    url(r'^blog/media/$', blog_views.BlogMediaIndexCtrl.as_django_view(), name=blog_views.BlogMediaIndexCtrl.view_name),
    url(r'^blog/media/add/$', blog_views.BlogMediaCreateCtrl.as_django_view(), name=blog_views.BlogMediaCreateCtrl.view_name),
    url(r'^blog/media/(?P<entity_key>[A-Za-z0-9-_:]+)/edit/$', blog_views.BlogMediaEditCtrl.as_django_view(), name=blog_views.BlogMediaEditCtrl.view_name),
    
    #url(r'^$', blog_views.BlogViewCtrl.as_django_view(), name=blog_views.IndexCtrl.view_name),                

)
"""
