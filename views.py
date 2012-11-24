from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from merkabah.core import controllers as merkabah_controllers
import logging
    
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
    
class ContactCtrl(merkabah_controllers.MerkabahController):
    view_name = 'contact'
    template = 'contact.html'

class ArtworkCtrl(merkabah_controllers.MerkabahController):
    view_name = 'artwork_index'
    template = 'artwork/index.html'

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