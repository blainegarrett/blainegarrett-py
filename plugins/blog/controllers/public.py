"""
A Collection of public controllers for the blog module
"""
from merkabah.core.controllers import MerkabahDjangoController
from plugins.blog.internal import api as blog_api


class BlogBaseCtrl(MerkabahDjangoController):
    """
    Base Controller for all Public Blog Controllers
    """
    pass


class BlogCtrl(BlogBaseCtrl):
    """
    Display a paginated list of lastest blog posts
    """

    view_name = 'blog_index'
    template = 'plugins/blog/index.html'
    content_title = 'Blog'

    def process_request(self, request, context, *args, **kwargs):
        #
        page_number = int(kwargs.get('page_number', 1))
        posts, cursor, more = blog_api.get_published_posts(page_number)
        context['posts'] = posts
        context['cursor'] = cursor
        context['more'] = more
        context['cur_page'] = page_number


class BlogCategoryCtrl(BlogBaseCtrl):
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


class BlogPermalinkCtrl(BlogBaseCtrl):
    """
    Display a blog post
    """

    # TODO: Handle case when post not found or is not public
    view_name = 'blog_view'
    template = 'plugins/blog/view.html'
    content_title = 'Post'

    def process_request(self, request, context, *args, **kwargs):
        """
        Display a post by its slug given in the kwargs
        """

        slug = kwargs.get('permalink', None)
        slug = slug.split('/')[-2]
        post = blog_api.get_post_by_slug(slug) # TODO: Validate the date too

        if not post:
            raise Exception('Not found')

        self.content_title = post.title
        context['post'] = post


'''
class BlogPrimaryImageDisplay(BlogBaseCtrl):
    view_name = 'primary_image_display'

    def process_request(self, request, context, *args, **kwargs):
        from google.appengine.ext import blobstore
        from google.appengine.api import images
        from plugins.blog.internal.models import BlogMedia
        from google.appengine.ext import ndb
        from django import http

        super(BlogPrimaryImageDisplay, self).process_request(request, context, *args, **kwargs)
        blob_keystr = kwargs.get('blob_key', None)
        key = ndb.Key(urlsafe=blob_keystr)

        media = key.get()
        blob_key = media.blob_key

        #raise Exception(type(blob_key))

        blob_info = blobstore.BlobInfo.get(blob_key)
        if not blob_info:
            raise Exception('Blob Key does not exist')

        blob_file_size = blob_info.size
        blob_content_type = blob_info.content_type

        """
        if blob_info:
            img = images.Image(blob_key=blob_keystr)
            img.resize(width=40, height=100)
            img.im_feeling_lucky()
            thumbnail = img.execute_transforms(output_encoding=images.JPEG)
            return http.HttpResponse(thumbnail, mimetype=blob_content_type)
        """
        blob_concat = ""
        start = 0
        end = blobstore.MAX_BLOB_FETCH_SIZE - 1
        step = blobstore.MAX_BLOB_FETCH_SIZE - 1

        while(start < blob_file_size):
            blob_concat += blobstore.fetch_data(blob_key, start, end)
            temp_end = end
            start = temp_end + 1
            end = temp_end + step
        return http.HttpResponse(blob_concat, mimetype=blob_content_type, status=200)
'''