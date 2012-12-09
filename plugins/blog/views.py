from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from merkabah.core import controllers as merkabah_controllers
from google.appengine.api import users
from google.appengine.ext import ndb
from django.core import urlresolvers
import logging

from merkabah.admin.views import MerkabahAdminBaseController
from merkabah.core import files as merkabah_files
from plugins import blog as blog_base
from plugins.blog import forms as blog_forms
from plugins.blog import models as blog_models
from plugins.blog import datatables as blog_datatables
 
    
class BlogIndexCtrl(MerkabahAdminBaseController):
    view_name = 'merkabah_admin_blog_index'
    template = 'merkabah/admin/plugin/index.html'
    
    def process_request(self, request, context, *args, **kwargs):
        context['plugin_key'] = 'blog'
        context['plugin_name'] = blog_base.PLUGIN_NAME
        
        
class BlogPostBaseCtrl(BlogIndexCtrl):
    def process_request(self, request, context, *args, **kwargs):
        super(BlogPostBaseCtrl, self).process_request(request, context, *args, **kwargs)
        context['kind_key'] = 'post'


class BlogCategoryBaseCtrl(BlogIndexCtrl):
    def process_request(self, request, context, *args, **kwargs):
        super(BlogCategoryBaseCtrl, self).process_request(request, context, *args, **kwargs)
        context['kind_key'] = 'category'


class BlogPostIndexCtrl(BlogPostBaseCtrl):
    view_name = 'merkabah_admin_blog_post_index'
    template = 'merkabah/admin/plugin/entity/index.html'

    def process_request(self, request, context, *args, **kwargs):
        super(BlogPostIndexCtrl, self).process_request(request, context, *args, **kwargs)
        entities = blog_models.get_kind_class(context['kind_key']).query()
        context['add_link'] = urlresolvers.reverse('merkabah_admin_blog_post_create', args=())        
        context['datatable'] = blog_datatables.BlogPostGrid(entities, request, context)
        
        
class BlogPostCreateCtrl(BlogPostBaseCtrl):
    view_name = 'merkabah_admin_blog_post_create'
    template = 'merkabah/admin/plugin/entity/form.html'
    
    def process_request(self, request, context, *args, **kwargs):    
        super(BlogPostCreateCtrl, self).process_request(request, context, *args, **kwargs)
        
        context['form_type'] = 'Add'
        context['form_action_url'] = merkabah_files.create_upload_url('/madmin/blog/post/add/?fishdicks=true')
        
        if request.POST:
            context['form'] = blog_forms.BlogPostForm(request.POST)
            if context['form'].is_valid():
                
                upload_files = merkabah_files.get_uploads(request, 'image_file', True)
                uploaded_file = upload_files[0]
                uploaded_key = uploaded_file.key()
                                                
                # cleanup categories
                category_keys = []
                for keystr in context['form'].cleaned_data['categories']:
                    category_keys.append(ndb.Key(urlsafe=keystr))
                    
                post = blog_models.BlogPost(
                    title=context['form'].cleaned_data['title'], 
                    body=context['form'].cleaned_data['body'], 
                    slug=context['form'].cleaned_data['slug'],
                    categories=category_keys,
                    primary_image_blob = uploaded_key
                )                
                post.put()
                                
                return redirect(urlresolvers.reverse('merkabah_admin_blog_post_index', args=()))
                            
        else:
            context['form'] = blog_forms.BlogPostForm()
                    
class BlogPostEditCtrl(BlogPostBaseCtrl):
    view_name = 'merkabah_admin_blog_post_edit'
    template = 'merkabah/admin/plugin/entity/form.html'
    
    def process_request(self, request, context, *args, **kwargs):
        super(BlogPostEditCtrl, self).process_request(request, context, *args, **kwargs)
        
        context['form_type'] = 'Edit'        
        blog_post_key = ndb.Key(urlsafe=kwargs['entity_key'])
        post = blog_post_key.get()
        
        form_initial = {}
        form_initial['title'] = post.title 
        form_initial['slug'] = post.slug
        form_initial['body'] = post.body
        
        # cleanup categories
        form_initial['categories'] = []
        for key in post.categories:
            form_initial['categories'].append(key.urlsafe())
        
        if request.POST:
            context['form'] = blog_forms.BlogPostForm(data=request.POST, initial=form_initial)
            context['form'].is_valid()
        
            if context['form'].is_valid():
                
                # cleanup categories
                category_keys = []
                for keystr in context['form'].cleaned_data['categories']:
                    category_keys.append(ndb.Key(urlsafe=keystr))
                    
                post.title=context['form'].cleaned_data['title']
                post.body=context['form'].cleaned_data['body']
                post.slug=context['form'].cleaned_data['slug']
                post.categories=category_keys
                post.put()
                
                return redirect(urlresolvers.reverse('merkabah_admin_blog_post_index', args=()))
                        
        else:
            context['form'] = blog_forms.BlogPostForm(initial=form_initial)
        
        
class BlogCategoryIndexCtrl(BlogCategoryBaseCtrl):
    view_name = 'merkabah_admin_blog_category_index'
    template = 'merkabah/admin/plugin/entity/index.html'

    def process_request(self, request, context, *args, **kwargs):
        super(BlogCategoryIndexCtrl, self).process_request(request, context, *args, **kwargs)
                
        entities = blog_models.BlogCategory.query()
        context['add_link'] = urlresolvers.reverse('merkabah_admin_blog_category_create', args=())
        context['datatable'] = blog_datatables.BlogCategoryGrid(entities, request, context)

class BlogCategoryCreateCtrl(BlogCategoryBaseCtrl):
    view_name = 'merkabah_admin_blog_category_create'
    template = 'merkabah/admin/plugin/entity/form.html'

    def process_request(self, request, context, *args, **kwargs):
        super(BlogCategoryCreateCtrl, self).process_request(request, context, *args, **kwargs)

        context['form_type'] = 'Add'

        if request.POST:
            context['form'] = blog_forms.BlogCategoryForm(request.POST)
            context['form'].is_valid()

            if context['form'].is_valid():
                post = blog_models.BlogCategory(name=context['form'].cleaned_data['name'], slug=context['form'].cleaned_data['slug'])                
                post.put()

                return redirect(urlresolvers.reverse('merkabah_admin_blog_category_index', args=()))

        else:
            context['form'] = blog_forms.BlogCategoryForm()


class BlogCategoryEditCtrl(BlogPostBaseCtrl):
    view_name = 'merkabah_admin_blog_category_edit'
    template = 'merkabah/admin/plugin/entity/form.html'

    def process_request(self, request, context, *args, **kwargs):
        super(BlogCategoryEditCtrl, self).process_request(request, context, *args, **kwargs)

        context['form_type'] = 'Edit'        
        blog_post_key = ndb.Key(urlsafe=kwargs['entity_key'])
        post = blog_post_key.get()

        form_initial = {}
        form_initial['name'] = post.name 
        form_initial['slug'] = post.slug

        if request.POST:
            context['form'] = blog_forms.BlogCategoryForm(data=request.POST, initial=form_initial)
            context['form'].is_valid()

            if context['form'].is_valid():
                post.name=context['form'].cleaned_data['name']
                post.slug=context['form'].cleaned_data['slug']
                post.put()

                return redirect(urlresolvers.reverse('merkabah_admin_blog_category_index', args=()))

        else:
            context['form'] = blog_forms.BlogCategoryForm(initial=form_initial)



