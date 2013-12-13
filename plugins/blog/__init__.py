"""
Blog Plugin
"""

from plugins.blog.forms import BlogPostForm, ImageUploadForm
from plugins.blog.internal.api import get_posts
from plugins.blog.internal.api import get_images
from plugins.blog.internal.api import create_post, edit_post
from plugins.blog.internal.models import BlogMedia

from google.appengine.ext import ndb

from plugins.blog.datatables import BlogPostGrid, BlogMediaGrid
import logging
from merkabah.core.controllers import TemplateResponse, FormDialogResponse, AlertResponse
from merkabah.core.controllers import FormResponse, FormErrorResponse, CloseFormResponse, GridRowResponse

class BlogPlugin(object):
    name = 'Blog'
    entity_nice_name = 'post'
    entity_plural_name = 'posts'
    query_method = get_posts

    def process_index(self, request, context, *args, **kwargs):
        """
        Driver switchboard logic
        """
        
        entities, cursor, more = get_posts(limit=1000)
        context['grid'] = BlogPostGrid(entities, request, context)

        context['plugin'] = self
        return TemplateResponse('admin/plugin/index.html', context)


    def process_create(self, request, context, *args, **kwargs):
        form = BlogPostForm()

        if request.POST:
            form = BlogPostForm(request.POST)
            if form.is_valid():

                p = create_post(form.cleaned_data)
    
                # Serve up the new row
                content = str(BlogPostGrid([p], request, context).render_row(p))
                return CloseFormResponse('create_form'), GridRowResponse(content, id='dashboard-container')

            else:
                return FormErrorResponse(form, id='create_form')

        if request.is_ajax():
            return FormResponse(form, id='create_form', title="Create a new Blog Post", target_url='/madmin/plugin/blog/create/', target_action='create')
        return TemplateResponse('admin/plugin/inline_form_wrapper.html', context)

    def process_edit(self, request, context, *args, **kwargs):
        post_keystr = request.REQUEST['post_key']

        if not post_keystr:
            raise RuntimeError('No argument post_key provided.')

        post_key = ndb.Key(urlsafe=post_keystr)
        post = post_key.get()

        initial_data = {
            'slug': post.slug,
            'title': post.title,
            'content': post.content,
            'publish': post.is_published,
        }

        form = BlogPostForm(initial=initial_data)

        if request.POST:
            form = BlogPostForm(request.POST, initial=initial_data)
            if form.is_valid():

                p = edit_post(post, form.cleaned_data)

                # Serve up the new row
                content = str(BlogPostGrid([p], request, context).render_row(p))
                return CloseFormResponse('edit_form'), GridRowResponse(content, id='dashboard-container')

            else:
                return FormErrorResponse(form, id='create_form')

        if request.is_ajax():
            return FormResponse(form, id='edit_form', title="Edit Blog Post", target_url='/madmin/plugin/blog/edit/?post_key=%s' % post_key.urlsafe(), target_action='edit')
        return TemplateResponse('admin/plugin/inline_form_wrapper.html', context)


    def process_delete(self, request, context, *args, **kwargs):
        """
        """

        post_keystr = request.REQUEST['post_key']

        if not post_keystr:
            raise RuntimeError('No argument post_key provided.')

        post_key = ndb.Key(urlsafe=post_keystr)

        # Delete the entity that refers to the gcs file
        post_key.delete()
        return AlertResponse('Deleted...')


    def process_images_create(self, request, context, *args, **kwargs):
        from merkabah.core.files.api.cloudstorage import Cloudstorage
        from google.appengine.ext import blobstore

        # Get the file upload url
        fs = Cloudstorage('blaine-garrett')

        form = ImageUploadForm()
        
        context['form'] = form

        if request.POST:
            file_info = fs.get_uploads(request, 'the_file', True)[0]


            original_filename = file_info.filename
            content_type = file_info.content_type
            size = file_info.size
            gs_object_name  = file_info.gs_object_name # Using this we could urlfetch, but the file isn't public...
            blob_key = blobstore.create_gs_key(gs_object_name)
            logging.warning(blob_key)
            data =  fs.read(gs_object_name.replace('/gs', ''))
            #logging.warning(data)

            # What we want to do now is create a copy of the file with our own info
            
            dest_filename = 'juniper/%s' % original_filename

            new_gcs_filename = fs.write(dest_filename, data, content_type)
            logging.warning(new_gcs_filename)
            
            # Finally delete the tmp file
            data =  fs.delete(gs_object_name.replace('/gs', ''))

            media_key = BlogMedia(content_type=content_type, size=size, filename=dest_filename, gcs_filename = dest_filename).put()

            raise Exception(new_gcs_filename)



        from merkabah.core.files.api.cloudstorage import Cloudstorage


        upload_url = fs.create_upload_url('/madmin/plugin/blog/images_create/')
        
        if request.is_ajax():
            return FormResponse(form, id='images_create_form', title="Upload a file", target_url=upload_url, target_action='images_create', is_upload=True)
        return TemplateResponse('admin/plugin/inline_form_wrapper.html', context)

    def process_images(self, request, context, *args, **kwargs):
        
        from merkabah.core.files.api.cloudstorage import Cloudstorage
        
        # Get the file upload url
        fs = Cloudstorage('blaine-garrett')
        context['upload_url'] = fs.create_upload_url('/upload_endpoint/')

        entities = get_images()
        context['grid'] = BlogMediaGrid(entities, request, context)

        return TemplateResponse('plugins/blog/images.html', context)
    
    def process_delete_image(self, request, context, *args, **kwargs):
        """
        """
        from merkabah.core.files.api.cloudstorage import Cloudstorage

        media_keystr = request.REQUEST['media_key']
        
        if not media_keystr:
            raise RuntimeError('No argument media_key provided.')
        
        media_key = ndb.Key(urlsafe=media_keystr)
        
        # Prep the file on cloud storage to be deleted
        media = media_key.get()
        
        if not (media or media.gcs_filename):
            logging.debug('Media with key %s did not have a gs_filename.' % media_keystr)
        else:
            # TODO: Do this in a deferred task
            fs = Cloudstorage('blaine-garrett')
            fs.delete(media.gcs_filename)

        # Delete the entity that refers to the gcs file
        media_key.delete()
        return AlertResponse('Deleted...')

    def process_select_image(self, request, context, *args, **kwargs):
        
        entities = get_images()
        context['grid'] = BlogMediaGrid(entities, request, context)
        
        
        
        
        
        

# Register Plugin
pluginClass = BlogPlugin