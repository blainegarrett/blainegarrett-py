"""
A Collection of public controllers for the blog module
"""
from merkabah.core import controllers as merkabah_controllers

from plugins.blog.internal import api as blog_api


class BlogCtrl(merkabah_controllers.MerkabahController):
    """
    Display a paginated list of lastest blog posts
    """

    view_name = 'blog_index'
    template = 'blog/index.html'

    def process_request(self, request, context, *args, **kwargs):
        
        #cursor = request.GET.get('cursor', None)
        page_number = int(kwargs.get('page_number', 1))

        posts, cursor, more = blog_api.get_published_posts(page_number)

        context['posts'] = posts
        context['cursor'] = cursor
        context['more'] = more
        context['cur_page'] = page_number

class BlogCategoryCtrl(merkabah_controllers.MerkabahController):
    view_name = 'artwork_index'
    template = 'blog/index.html'
    
    def process_request(self, request, context, *args, **kwargs):
        from plugins.blog import models as blog_models
        
        category_slug = kwargs.get('category_slug', None)

        cat = blog_models.BlogCategory.query(blog_models.BlogCategory.slug == category_slug).get()
        if not cat:
            return
                
        posts = blog_models.BlogPost.query(blog_models.BlogPost.categories == cat.key)
        context['posts'] = posts


class BlogPermalinkCtrl(merkabah_controllers.MerkabahController):
    """
    Display a blog post
    """

    # TODO: Handle case when post not found or is not public
    view_name = 'blog_view'
    template = 'blog/view.html'

    def process_request(self, request, context, *args, **kwargs):
        from merkabah.core.blobstore import store_image_in_blobstore_by_url
        from bs4 import BeautifulSoup
        from google.appengine.ext import blobstore        
        slug = kwargs['permalink'].split('/')[-2]
        
        post = blog_api.get_post_by_slug(slug)

        if not post:
            raise Exception('Not found')

        context['post'] = post
        


class BlogPrimaryImageDisplay(merkabah_controllers.MerkabahController):
    view_name = 'primary_image_display'

    def process_request(self, request, context, *args, **kwargs):
        from google.appengine.ext import blobstore
        from google.appengine.api import images
        from plugins.blog.intenal.models import BlogMedia
        from google.appengine.ext import ndb

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