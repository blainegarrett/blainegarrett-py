"""
A Collection of public controllers for the blog module
"""

from plugins.artwork.internal import api as artwork_api
from django.http import Http404, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from plugins.blog.config import BaseCtrlClass

class ArtworkBaseCtrl(BaseCtrlClass):
    """
    Base Controller for all Public Artwork Controllers
    """
    chrome_template = 'v2/base.html'
    active_menu_tab = 'artwork'


class ArtworkIndexCtrl(ArtworkBaseCtrl):
    """
    Display a paginated list of lastest blog posts
    """

    view_name = 'artwork_index'
    template = 'plugins/artwork/index.html'
    content_title = 'Artwork'

    @property
    def content_breadcrumbs(self):
        return [('/', 'Home'), (reverse(self.view_name, args=[]), self.content_title)]

    '''
    def process_request(self, request, context, *args, **kwargs):

        #
        page_number = int(kwargs.get('page_number', 1))
        posts, cursor, more = blog_api.get_published_posts(page_number)
        context['posts'] = posts
        context['cursor'] = cursor
        context['more'] = more
        context['cur_page'] = page_number
    '''


class ArtworkGalleryCtrl(ArtworkBaseCtrl):
    view_name = 'artwork_index'
    template = 'plugins/blog/index.html'

    def process_request(self, request, context, *args, **kwargs):
        from plugins.blog.internal import models as blog_models

        category_slug = kwargs.get('category_slug', None)

        cat = blog_models.BlogCategory.query(blog_models.BlogCategory.slug == category_slug).get()
        if not cat:
            return

        posts = blog_models.BlogPost.query(blog_models.BlogPost.categories == cat.key)
        context['posts'] = posts


class ArtworkPermalinkCtrl(ArtworkBaseCtrl):
    """
    Display a blog post
    """

    # TODO: Handle case when post not found or is not public
    view_name = 'blog_view'
    template = 'plugins/blog/view.html'
    content_title = 'Post'

    @property
    def content_breadcrumbs(self):
        return [('/', 'Home'), (reverse('blog_index', args=[]), 'Blog'), (self.post.get_permalink, self.post.title)]

    def process_request(self, request, context, *args, **kwargs):
        """
        Display a post by its slug given in the kwargs
        """

        target_slug = kwargs.get('permalink', None)
        slug_chunks = target_slug.split('/')

        slug = slug_chunks[-2]
        post = blog_api.get_post_by_slug(slug.lower())
        
        self.post = post # Templ Hack for breadcrumbs

        if not post:
            raise Http404

        if not post.slug == slug:
            return HttpResponsePermanentRedirect(post.get_permalink())

        # Ensure the published date matches the slug for url base plugins, etc
        pub = post.published_date
        expected_date_slug = '%02d/%02d/%02d' % (int(pub.year), int(pub.month), int(pub.day))
        actual_date_slug = target_slug[0:10]
        
        if not expected_date_slug == actual_date_slug:
            # Redirect to the actual permalink
            return HttpResponsePermanentRedirect(post.get_permalink())

        self.content_title = post.title
        context['post'] = post
