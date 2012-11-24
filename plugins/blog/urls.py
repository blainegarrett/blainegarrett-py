from django.conf.urls.defaults import *
from plugins.blog import views as blog_views

urlpatterns = patterns('plugins.admin.views',
    
    # Generic Blog urls - to, more dynamically generate these based on installed plugins
    url(r'^blog/$', blog_views.BlogIndexCtrl.as_view(), name=blog_views.BlogIndexCtrl.view_name),

    url(r'^blog/post/$', blog_views.BlogPostIndexCtrl.as_view(), name=blog_views.BlogPostIndexCtrl.view_name),
    url(r'^blog/post/add/$', blog_views.BlogPostCreateCtrl.as_view(), name=blog_views.BlogPostCreateCtrl.view_name),
    url(r'^blog/post/(?P<entity_key>[A-Za-z0-9-_:]+)/edit/$', blog_views.BlogPostEditCtrl.as_view(), name=blog_views.BlogPostEditCtrl.view_name),

    url(r'^blog/category/$', blog_views.BlogCategoryIndexCtrl.as_view(), name=blog_views.BlogCategoryIndexCtrl.view_name),
    url(r'^blog/category/add/$', blog_views.BlogCategoryCreateCtrl.as_view(), name=blog_views.BlogCategoryCreateCtrl.view_name),
    url(r'^blog/category/(?P<entity_key>[A-Za-z0-9-_:]+)/edit/$', blog_views.BlogCategoryEditCtrl.as_view(), name=blog_views.BlogCategoryEditCtrl.view_name),
    
    #url(r'^$', blog_views.BlogViewCtrl.as_view(), name=blog_views.IndexCtrl.view_name),                

)
