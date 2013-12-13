from __future__ import absolute_import

import logging

from google.appengine.ext import ndb


class Page(ndb.Model):
    """
    Blog Pages module - currently Not in use
    """

    primary_content = ndb.TextProperty()
    slug = ndb.StringProperty(indexed=True)
    title = ndb.StringProperty()


class BlogMedia(ndb.Model):
    """
    A ndb.model wrapper to house a media file
    """

    filename = ndb.StringProperty()
    blob_key = ndb.BlobKeyProperty()
    content_type = ndb.StringProperty()
    gcs_filename = ndb.StringProperty()
    size = ndb.IntegerProperty()
    
    
    @property
    def size_in_kb(self):
        return self.size * 1000
    
    


class BlogCategory(ndb.Model):
    """
    A blog category
    """

    nice_name = 'Category'

    slug = ndb.StringProperty()
    name = ndb.StringProperty()


class BlogPost(ndb.Model):
    """
    A Blog Post
    """

    nice_name = 'Posts'

    title = ndb.StringProperty()
    slug = ndb.StringProperty()
    content = ndb.TextProperty()
    published_date = ndb.DateTimeProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    modified_date = ndb.DateTimeProperty(auto_now=True)
    categories = ndb.KeyProperty(repeated=True, kind=BlogCategory)
    primary_media_image = ndb.KeyProperty(kind=BlogMedia)
    attached_media = ndb.KeyProperty(repeated=True, kind=BlogMedia)
    is_published = ndb.BooleanProperty(default=False)

    def get_primary_image_url(self):
        return BlogMedia.get(self.primary_media_image).filename

    def get_permalink(self):
        dt = self.published_date
        if dt:
            return '/%02d/%02d/%02d/%s' % (dt.year, dt.month, dt.day, self.slug)
        else:
            return '#'

#kind_name_map = { 'post' : BlogPost, 'category' : BlogCategory }


def make_dummy_data(total):
    """
    Helper to make some dummy data to test with.
    """

    from datetime import datetime
    from google.appengine.api import memcache

    i = 0
    while i < total:

        b = BlogPost()
        b.title='Super Cool %s' % i
        b.slug='super-cool-%s' % i
        b.content = 'This <b>Thing that happened to me</b>'
        b.published_date = datetime.now()
        b.is_published = True
        b.put()
        i += 1

    memcache.delete('cursor_index')
