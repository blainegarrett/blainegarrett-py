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
