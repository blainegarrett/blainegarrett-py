from __future__ import with_statement

import logging

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django import http
from django.views.decorators.csrf import csrf_exempt

from google.appengine.api import files

from merkabah.core import controllers as merkabah_controllers


class MainCtrl(merkabah_controllers.MerkabahController):
    """
    Welcome page - mapped to /
    """

    view_name = 'main'
    template = 'main.html'
    content_title = 'Welcome'


class AboutCtrl(merkabah_controllers.MerkabahController):
    """
    About Page - mapped to /about
    """

    view_name = 'about'
    template = 'about.html'

    
class ContactCtrl(merkabah_controllers.MerkabahController):
    view_name = 'contact'
    template = 'contact.html'


class SoftwareCtrl(merkabah_controllers.MerkabahController):
    view_name = 'software_index'
    template = 'software/index.html'


class ProjectsCtrl(merkabah_controllers.MerkabahController):
    view_name = 'projects_index'
    template = 'projects/index.html'


class LinksCtrl(merkabah_controllers.MerkabahController):
    """
    Display list of links - Maps to /links
    """

    view_name = 'links'
    template = 'links.html'


class ClientsCtrl(merkabah_controllers.MerkabahController):
    """
    Display list of clients - maps to /clients
    """

    view_name = 'clients'
    template = 'clients.html'


'''
@csrf_exempt
def upload_endpoint(request):
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