from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from merkabah.core import controllers as merkabah_controllers
from google.appengine.api import users
from google.appengine.ext import ndb
from django.core import urlresolvers
import logging
import datetime
from plugins.blog import utils as blog_utils

from merkabah.admin.views import MerkabahAdminBaseController
from merkabah.core import files as merkabah_files
from merkabah.core import blobstore as merkabah_blobstore
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

class BlogMediaBaseCtrl(BlogIndexCtrl):
    def process_request(self, request, context, *args, **kwargs):
        super(BlogMediaBaseCtrl, self).process_request(request, context, *args, **kwargs)
        context['kind_key'] = 'media'

class BlogPostIndexCtrl(BlogPostBaseCtrl):
    view_name = 'merkabah_admin_blog_post_index'
    template = 'merkabah/admin/plugin/entity/index.html'

    def process_request(self, request, context, *args, **kwargs):
        super(BlogPostIndexCtrl, self).process_request(request, context, *args, **kwargs)
        
        entities = blog_utils.get_all_posts(1)
        context['add_link'] = urlresolvers.reverse('merkabah_admin_blog_post_create', args=())        
        context['datatable'] = blog_datatables.BlogPostGrid(entities, request, context)
        
        
class BlogPostCreateCtrl(BlogPostBaseCtrl):
    view_name = 'merkabah_admin_blog_post_create'
    template = 'merkabah/admin/plugin/entity/form.html'
    
    def process_request(self, request, context, *args, **kwargs):
        super(BlogPostCreateCtrl, self).process_request(request, context, *args, **kwargs)
        
        context['form_type'] = 'Add'
        #context['form_action_url'] = merkabah_blobstore.create_upload_url('/madmin/blog/post/add/?fishdicks=true')
        
        if request.POST:
            context['form'] = blog_forms.BlogPostForm(request.POST)
            if context['form'].is_valid():                                                
                # cleanup categories
                category_keys = []
                for keystr in context['form'].cleaned_data['categories']:
                    category_keys.append(ndb.Key(urlsafe=keystr))
                
                published_date = None
                if context['form'].cleaned_data['publish']:
                    published_date = datetime.datetime.now()
                
                post = blog_models.BlogPost(
                    title=context['form'].cleaned_data['title'], 
                    content=context['form'].cleaned_data['content'], 
                    slug=context['form'].cleaned_data['slug'],
                    categories=category_keys,
                    #primary_media_image = uploaded_key,
                    published_date = published_date
                )
                
                if context['form'].cleaned_data['primary_media_image']:
                    blog_media_key = ndb.Key(urlsafe=context['form'].cleaned_data['primary_media_image'])
                    post.primary_media_image = blog_media_key
                    post.attached_media.append(blog_media_key)
                else:
                    post.primary_media_image = None
                    
                
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
        #context['form_action_url'] = merkabah_blobstore.create_upload_url('/madmin/blog/post/%s/edit/?fishdicks=true' % kwargs['entity_key'])
        
        blog_post_key = ndb.Key(urlsafe=kwargs['entity_key'])
        post = blog_post_key.get()
        
        form_initial = {}
        form_initial['title'] = post.title 
        form_initial['slug'] = post.slug
        form_initial['content'] = post.content
        form_initial['publish'] = bool(post.published_date)
        
        if post.primary_media_image:
            form_initial['primary_media_image'] = post.primary_media_image.urlsafe()
        else:
            form_initial['primary_media_image'] = ''            
                
        # cleanup categories
        form_initial['categories'] = []
        for key in post.categories:
            form_initial['categories'].append(key.urlsafe())
        
        if request.POST:
            context['form'] = blog_forms.BlogPostForm(data=request.POST, initial=form_initial)
            context['form'].is_valid()
        
            if context['form'].is_valid():
                
                # Published case...
                if post.published_date and not context['form'].cleaned_data['publish']:
                    published_date = None # Was published now not
                elif not post.published_date and context['form'].cleaned_data['publish']:
                    published_date = datetime.datetime.now() # Was published now not                    
                else:
                    published_date = post.published_date
                    
                # cleanup categories
                category_keys = []
                for keystr in context['form'].cleaned_data['categories']:
                    category_keys.append(ndb.Key(urlsafe=keystr))
                    
                post.title=context['form'].cleaned_data['title']
                post.content=context['form'].cleaned_data['content']
                post.slug=context['form'].cleaned_data['slug']
                post.categories=category_keys
                post.published_date = published_date
                
                if context['form'].cleaned_data['primary_media_image']:
                    blog_media_key = ndb.Key(urlsafe=context['form'].cleaned_data['primary_media_image'])
                    post.primary_media_image = blog_media_key
                    post.attached_media.append(blog_media_key)
                else:
                    post.primary_media_image = None
                
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


class BlogMediaIndexCtrl(BlogCategoryBaseCtrl):
    view_name = 'merkabah_admin_blog_media_index'
    template = 'merkabah/admin/plugin/entity/index.html'

    def process_request(self, request, context, *args, **kwargs):
        super(BlogMediaIndexCtrl, self).process_request(request, context, *args, **kwargs)

        entities = blog_models.BlogMedia.query()
        context['add_link'] = urlresolvers.reverse('merkabah_admin_blog_media_create', args=())
        context['datatable'] = blog_datatables.BlogMediaGrid(entities, request, context)
        

class BlogMediaCreateCtrl(BlogPostBaseCtrl):
    view_name = 'merkabah_admin_blog_media_create'
    template = 'merkabah/admin/plugin/entity/form.html'
    
    def process_request(self, request, context, *args, **kwargs):
        super(BlogMediaCreateCtrl, self).process_request(request, context, *args, **kwargs)
        
        context['form_type'] = 'Add'
        context['form_action_url'] = merkabah_blobstore.create_upload_url('/madmin/blog/media/add/?fishdicks=true')
        
        if request.POST:
            context['form'] = blog_forms.BlogMediaForm(request.POST)
            if context['form'].is_valid():
                # Process Images
                upload_files = merkabah_files.get_uploads(request, 'image_file', True)
                uploaded_key = None
                if upload_files: # list of BlobInfo objects
                    for blob_info in upload_files:
                        blob_file_size = blob_info.size
                        blob_content_type = blob_info.content_type
                        
                        blob_key = blob_info.key()
                        media_key = blog_models.BlogMedia(blob_key=blob_key, content_type=blob_info.content_type, size=blob_file_size, filename=blob_info.filename).put()            
                        #post.primary_media_image = media_key
                        #post.attached_media.append(media_key)
                
                return redirect(urlresolvers.reverse('merkabah_admin_blog_media_index', args=()))    
                #post.put()
                
                
                
                
                
        else:
            context['form'] = blog_forms.BlogMediaForm(initial={'is_upload' : True})
        

class BlogMediaEditCtrl(BlogPostBaseCtrl):
    view_name = 'merkabah_admin_blog_media_edit'
    template = 'merkabah/admin/plugin/entity/form.html'
        
        