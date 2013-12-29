"""
Controllers for top level pages on blainegarrett.com
TODO: Most of these can be converted to pages at a later date
"""

from __future__ import with_statement
from merkabah.core.controllers import MerkabahDjangoController
from django.core.urlresolvers import reverse


class BaseCtrl(MerkabahDjangoController):
    """
    Base controller for all of BlaineGarrett.com
    """
    chrome_template = 'v2/base.html'
    active_menu_tab = 'home'

    @property
    def content_breadcrumbs(self):
        return [('/', 'Home'), (reverse(self.view_name, args=[]), self.content_title)]

    def process_request(self, request, context, *args, **kwargs):
        result = super(BaseCtrl, self).process_request(request, context, *args, **kwargs)
        if not result:
            context['active_menu_tab'] = self.active_menu_tab
        return result


class MainCtrl(BaseCtrl):
    """
    Welcome page - mapped to /
    """

    view_name = 'main'
    template = 'v2/main.html'
    content_title = 'Welcome'
    active_menu_tab = 'home'

    def process_request(self, request, context, *args, **kwargs):
        from plugins.blog.internal.api import get_published_posts
        result = super(MainCtrl, self).process_request(request, context, *args, **kwargs)

        if not result:
            context['posts'] = get_published_posts(page_number=1)[0][:4]
        return result


class AboutCtrl(BaseCtrl):
    """
    About Page - mapped to /about
    """

    view_name = 'about'
    template = 'v2/about.html'
    content_title = 'About'
    active_menu_tab = 'about'


class ContactCtrl(BaseCtrl):
    """
    Contact Page - mapped to /contact
    """

    view_name = 'contact'
    template = 'v2/contact.html'
    content_title = 'Contact'


class SoftwareCtrl(BaseCtrl):
    """
    Software Page - mapped to /software
    """

    view_name = 'software_index'
    template = 'v2/software/index.html'
    content_title = 'Software'


class ProjectsCtrl(BaseCtrl):
    """
    Projects Page - mapped to /projects
    """

    view_name = 'projects_index'
    template = 'v2/projects/index.html'
    content_title = 'Projects'
    active_menu_tab = 'projects'


class ProjectsCategoryCtrl(BaseCtrl):
    """
    Projects Page - mapped to /projects
    """

    view_name = 'projects_category'
    template = 'v2/projects/category.html'
    content_title = 'View Projects'
    active_menu_tab = 'projects'

    @property
    def content_breadcrumbs(self):
        return [('/', 'Home'), ('/projects/', 'Projects'), ('/', 'FIXME')]


class LinksCtrl(BaseCtrl):
    """
    Display list of links - Maps to /links
    """

    view_name = 'links'
    template = 'v2/links.html'
    content_title = 'Links'


class ClientsCtrl(BaseCtrl):
    """
    Display list of clients - maps to /clients
    """
    '''
    @property
    def content_breadcrumbs(self):

        crumbs = super(ClientsCtrl, self).content_breadcrumbs
        crumbs.append(('genus', 'Welco'))
        return crumbs
    '''

    view_name = 'clients'
    template = 'v2/clients.html'
    content_title = 'Clients'
