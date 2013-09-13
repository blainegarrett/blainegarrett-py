"""
Controllers for top level pages on blainegarrett.com
TODO: Most of these can be converted to pages at a later date
"""

from __future__ import with_statement
from merkabah.core import controllers as merkabah_controllers


class BaseCtrl(merkabah_controllers.MerkabahController):
    """
    Base controller for all of BlaineGarrett.com
    """
    pass


class MainCtrl(BaseCtrl):
    """
    Welcome page - mapped to /
    """

    view_name = 'main'
    template = 'main.html'
    content_title = 'Welcome'


class AboutCtrl(BaseCtrl):
    """
    About Page - mapped to /about
    """

    view_name = 'about'
    template = 'about.html'
    content_title = 'About'


class ContactCtrl(BaseCtrl):
    """
    Contact Page - mapped to /contact
    """

    view_name = 'contact'
    template = 'contact.html'
    content_title = 'Contact'


class SoftwareCtrl(BaseCtrl):
    """
    Software Page - mapped to /software
    """

    view_name = 'software_index'
    template = 'software/index.html'
    content_title = 'Software'


class ProjectsCtrl(BaseCtrl):
    """
    Projects Page - mapped to /projects
    """

    view_name = 'projects_index'
    template = 'projects/index.html'
    content_title = 'Projects'


class LinksCtrl(BaseCtrl):
    """
    Display list of links - Maps to /links
    """

    view_name = 'links'
    template = 'links.html'
    content_title = 'Links'


class ClientsCtrl(BaseCtrl):
    """
    Display list of clients - maps to /clients
    """

    view_name = 'clients'
    template = 'clients.html'
    content_title = 'Clients'


class UploadCtrl(BaseCtrl):
    """
    Display list of clients - maps to /clients
    """
    view_name = 'upload'
    template = 'upload.html'
    content_title = 'Upload'

    def process_request(self, request, context, *args, **kwargs):
        from merkabah.core.files.api.cloudstorage import Cloudstorage
        from merkabah.core.files.api.blobstore import Blobstore

        fs = Cloudstorage('blaine-garrett')

        context['upload_url'] = fs.create_upload_url('/upload_endpoint/')

        #fs = Blobstore()
        #context['upload_url'] = fs.create_upload_url('/upload_endpoint/')
        #context['upload_url'] = fs.create_upload_url('/upload_endpoint/')

        #filename = fs.write('zotz.html', 'what<b>evXXXXXX</b>er', 'text/html')
        #content = fs.read(filename)

        #fs = Blobstore()
        #filename = blob_key = fs.write('snorf.html', 'whatevXXXXXXer', 'text/html')
        #content = fs.read(blob_key)

        #context['file_content'] = content
        #context['file_url'] = fs.get_full_url(filename)


class UploadCtrlEndpoint(BaseCtrl):
    """
    Display list of clients - maps to /clients
    """

    view_name = 'upload_endpoint'
    template = 'upload_endpoint.html'
    content_title = 'Upload Endpoint'
    
    def process_request(self, request, context, *args, **kwargs):
        from plugins.blog.internal.models import BlogMedia

        from merkabah.core.files.api.cloudstorage import Cloudstorage
        from merkabah.core.files.api.blobstore import Blobstore

        #from merkabah.core.files.api.cloudstorage import Cloudstorage
        #from merkabah.core.files.api.blobstore import Blobstore

        #fs = Cloudstorage('blaine-garrett')
        #context['files'] = fs.get_files()

        fs = Cloudstorage('blaine-garrett')
        files = fs.get_uploads(request)

        for f in files:
            
            b = BlogMedia()
            b.content_type = f.content_type
            b.size = f.size
            b.gcs_filename = f.gs_object_name

            b.put()
            

        
        
        

#UploadCtrlEndpoint

'''
@csrf_exempt
def upload_endpoint(request):
    from django.shortcuts import render_to_response, redirect
    from django.template import RequestContext
    from django import http
    from django.views.decorators.csrf import csrf_exempt
    from google.appengine.api import files

    from merkabah.core.files import get_uploads
    upload_files = get_uploads(request, 'image_file', True)

    #TODO: ADD ERROR CHECKING
    #blob_info = upload_files[0]
    logging.error(request.META)
    raise Exception([upload_files, request.POST])
    post_data = request.POST #{'title' : 'testupload', 'slug' : 'glork'}

    form = control_forms.ArtForm(post_data)
    if form.is_valid():
        models.Artwork(title=form.cleaned_data['title'], slug=form.cleaned_data['slug'],
            blob=blob_info.key()).put()
    else:
        raise Exception(form.errors)

    return redirect('/admin/artwork/')

#upload_endpoint


'''
