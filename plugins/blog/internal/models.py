from __future__ import absolute_import

import logging

from google.appengine.ext import ndb
from google.appengine.ext.blobstore import BlobInfo

#import bs4
#from bs4 import BeautifulSoup

def get_kind_class(kind_key):
    if kind_key == 'post':
        return BlogPost
    elif kind_key == 'category':
        return BlogCategory        
    raise Exception('No model defined for kind_key %s' % kind_key)


class Person(ndb.Model):
  """Models an individual Guestbook entry with content and date."""
  firstname = ndb.TextProperty()
  lastname = ndb.TextProperty()
  #content = ndb.StringProperty()
  #date = ndb.DateTimeProperty(auto_now_add=True)


class Page(ndb.Model):
    primary_content = ndb.TextProperty()
    slug = ndb.StringProperty()
    title = ndb.StringProperty()

class BlogMedia(ndb.Model):
    filename = ndb.StringProperty()
    blob_key = ndb.BlobKeyProperty()    
    content_type = ndb.StringProperty()
    gcs_filename = ndb.StringProperty()
    size = ndb.IntegerProperty()

class BlogCategory(ndb.Model):
    nice_name = 'Category'

    slug = ndb.StringProperty()
    name = ndb.StringProperty()


class BlogPost(ndb.Model):
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
        dt = self.created_date
        return '/%02d/%02d/%02d/%s' % (dt.year, dt.month, dt.day, self.slug)
    
kind_name_map = {
    'post' : BlogPost,
    'category' : BlogCategory
}


def make_dummy_data(total):
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


def kickoff_migration():
    """
    """

    from google.appengine.ext import deferred

    m_list = BlogMedia.query().fetch()

    for m in m_list:
        media_keystr = m.key.urlsafe()
        deferred.defer(migrate_media_to_gs, media_keystr)


def migrate_media_to_gs(media_key):
    """
    This should be run in a task
    """
    from merkabah.core.files.api.blobstore import Blobstore
    from merkabah.core.files.api.cloudstorage import Cloudstorage

    logging.debug('MIGRATING %s' % media_key)

    key = ndb.Key(urlsafe=media_key)
    media = key.get()
    blob_key = media.blob_key

    logging.debug(str(blob_key))

    blob_info = BlobInfo.get(blob_key)
    if not blob_info:
        return
        raise Exception('Blob Key does not exist')


    # Calculate file extension from content type
    if blob_info.content_type == 'image/gif':
        extension = 'gif'
    elif blob_info.content_type == 'image/png':
        extension = 'png'
    elif blob_info.content_type == 'image/jpeg':
        extension = 'jpg'
    else:
        return

    logging.debug(blob_info.content_type)
    
    fs1 = Blobstore()
    fs2 = Cloudstorage('blaine-garrett')

    file_content = fs1.read(blob_key)


    filename = 'blog_images/%s.%s' % (blob_info.md5_hash, extension)

    logging.debug(filename)

    fs2.write(filename, file_content, blob_info.content_type)

    #blob_file_size = blob_info.size
    #blob_content_type = blob_info.content_type
    media.gcs_filename = filename
    media.put()
    # Read the image

def all_done():
    """Will be run if the async task runs successfully."""
    from furious.context import get_current_async

    async = get_current_async()

    logging.info('async task complete, value returned: %r', async.result)


def handle_an_error():
    """Will be run if the async task raises an unhandled exception."""

    logging.warning('here....')
    import os

    from furious.context import get_current_async

    exception_info = get_current_async().result

    logging.info('async job blew up, exception info: %r', exception_info)

    retries = int(os.environ['HTTP_X_APPENGINE_TASKRETRYCOUNT'])
    if retries < 4:
        raise exception_info.exception
    else:
        logging.info('Caught too many errors, giving up now.')


    