from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from merkabah.core import controllers as merkabah_controllers
import logging
from django import http
    
class MainCtrl(merkabah_controllers.MerkabahController):
    view_name = 'main'
    template = 'main.html'

class AboutCtrl(merkabah_controllers.MerkabahController):
    view_name = 'about'
    template = 'about.html'
    
    def process_get_name(self, request, context, *args, **kwargs):
        from django import http
        
        logging.error('here...')
        content = 'farts'
        return http.HttpResponse(content)

from django.views.decorators.csrf import csrf_exempt
    
@csrf_exempt
def upload_endpoint(request):
    from merkabah.core.files import get_uploads
    upload_files = get_uploads(request, 'image_file', True)

    #TODO: ADD ERROR CHECKING
    #blob_info = upload_files[0]
    logging.error(request.META)
    raise Exception([upload_files, request.POST])
    post_data = request.POST #{'title' : 'farts2', 'slug' : 'glork'}    

    form = control_forms.ArtForm(post_data)
    if form.is_valid():    
        models.Artwork(title=form.cleaned_data['title'], slug=form.cleaned_data['slug'], blob=blob_info.key()).put()
    else:
        raise Exception(form.errors)

    return redirect('/admin/artwork/')

#upload_endpoint

class BlogPrimaryImageDisplay(merkabah_controllers.MerkabahController):
    view_name = 'primary_image_display'

    def process_request(self, request, context, *args, **kwargs):    
        from google.appengine.ext import blobstore
        from google.appengine.api import images        
        
        super(BlogPrimaryImageDisplay, self).process_request(request, context, *args, **kwargs)
        blob_keystr = kwargs.get('blob_key', None)
        
        blob_info = blobstore.BlobInfo.get(blob_keystr)
        if not blob_info:
            raise Exception('Blob Key does not exist')

        blob_file_size = blob_info.size
        blob_content_type = blob_info.content_type
        
        '''
        if blob_info:
            img = images.Image(blob_key=blob_keystr)
            img.resize(width=40, height=100)
            img.im_feeling_lucky()
            thumbnail = img.execute_transforms(output_encoding=images.JPEG)
            return http.HttpResponse(thumbnail, mimetype=blob_content_type)
        '''
        blob_concat = ""
        start = 0
        end = blobstore.MAX_BLOB_FETCH_SIZE - 1
        step = blobstore.MAX_BLOB_FETCH_SIZE - 1

        while(start < blob_file_size):
            blob_concat += blobstore.fetch_data(blob_keystr, start, end)
            temp_end = end
            start = temp_end + 1
            end = temp_end + step
        return http.HttpResponse(blob_concat, mimetype=blob_content_type, status=200)
    
class tinymcetest(merkabah_controllers.MerkabahController):
    view_name = 'tinymcetest'
    template = 'tinymcetest.html'
    chrome_template = 'blank.html'
    
class ContactCtrl(merkabah_controllers.MerkabahController):
    view_name = 'contact'
    template = 'contact.html'

class BlogCategoryCtrl(merkabah_controllers.MerkabahController):
    view_name = 'artwork_index'
    template = 'blog/index.html'
    
    def process_request(self, request, context, *args, **kwargs):
        from plugins.blog import models as blog_models
        
        category_slug = kwargs.get('category_slug', None)
        
        
        cat = blog_models.BlogCategory.query(blog_models.BlogCategory.slug == category_slug).get()        
        posts = blog_models.BlogPost.query(blog_models.BlogPost.categories == cat.key)
        context['posts'] = posts    
    

class SoftwareCtrl(merkabah_controllers.MerkabahController):
    view_name = 'software_index'
    template = 'software/index.html'

class ProjectsCtrl(merkabah_controllers.MerkabahController):
    view_name = 'projects_index'
    template = 'projects/index.html'

class BlogCtrl(merkabah_controllers.MerkabahController):
    view_name = 'blog_index'
    template = 'blog/index.html'
    
    def process_request(self, request, context, *args, **kwargs):
        from plugins.blog import models as blog_models
        posts = blog_models.BlogPost.query()
        context['posts'] = posts
        
        
class BlogPermalinkCtrl(merkabah_controllers.MerkabahController):
    view_name = 'blog_view'
    template = 'blog/view.html'
    
    def process_request(self, request, context, *args, **kwargs):
        slug = kwargs['permalink'].split('/')[-2]
        
        from plugins.blog import models as blog_models
        context['post'] = blog_models.BlogPost.query(blog_models.BlogPost.slug == slug).get()            

        
class LinksCtrl(merkabah_controllers.MerkabahController):
    view_name = 'links'
    template = 'links.html'

class ClientsCtrl(merkabah_controllers.MerkabahController):
    view_name = 'clients'
    template = 'clients.html'