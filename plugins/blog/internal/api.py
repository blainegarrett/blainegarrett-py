import logging

from datetime import datetime
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.api import memcache

from google.appengine.ext import ndb

from plugins.blog.internal.models import BlogPost
from plugins.blog.internal.models import BlogMedia
from plugins.blog.constants import POSTS_PER_PAGE
from plugins.blog.constants import PUBLISHED_DATE_MIN

############################
# Posts
###########################

def get_post_by_slug(slug):
    post = BlogPost.query(BlogPost.slug == slug).get()
    #TODO: Check if published or not

    return post


def get_posts(cursor=None, limit=POSTS_PER_PAGE):
    """
    Return a list of posts
    """
    if cursor:
        cursor = Cursor(urlsafe=cursor)

    q = BlogPost.query().order(-BlogPost.published_date)

    if cursor:
        entities, next_cursor, more = q.fetch_page(limit)
    else:
        entities, next_cursor, more = q.fetch_page(limit, start_cursor=cursor)

    return entities, next_cursor, more


def get_published_posts(page_number=1, limit=POSTS_PER_PAGE):
    """
    Return a list of posts
    """

    q = BlogPost.query().filter(BlogPost.published_date > PUBLISHED_DATE_MIN).order(-BlogPost.published_date)

    # Check if cursor index is in memcache
    cursor_index_key = 'cursor_index' # TODO: Build this from the query
    cursor_index = memcache.get(cursor_index_key)

    if not cursor_index:
        logging.debug('No Cursor Index found in memcache... generating it')
        # No Cursor Index in memcache - build it
        cursor_index = build_index(q)

        memcache.set(cursor_index_key, cursor_index)
    
    # Fetch the cursor based on the page #
    #TODO: Catch index error!

    cursor = None

    if page_number > 1:
        urlsafe_cursor = cursor_index['cursors'][(page_number - 1)]
        cursor = Cursor(urlsafe=urlsafe_cursor)

    # Run the query
    posts, cursor, more = q.fetch_page(limit, start_cursor=cursor)
    
    # Finally, bulk dereference the primary image
    
    p_map = {}
    for p in posts:
        if p.primary_media_image:
            p_map[p.primary_media_image] = p

    images = ndb.get_multi(p_map.keys())
    for image in images:
        post = p_map.get(image.key, None)
        if post and image:
            setattr(post, 'get_primary_media_image', image)
    
    return posts, cursor, more


def create_post(cleaned_data):
    """
    """
    
    # Category checks
    category_keys = []
    for keystr in cleaned_data['categories']:
        category_keys.append(ndb.Key(urlsafe=keystr))

    published_date = None
    if cleaned_data['publish']:
        published_date = datetime.now()

    post = BlogPost(
        title=cleaned_data['title'],
        content=cleaned_data['content'],
        slug=cleaned_data['slug'],
        categories=category_keys,
        published_date = published_date
    )

    if cleaned_data['primary_media_image']:
        blog_media_key = ndb.Key(urlsafe=cleaned_data['primary_media_image'])
        post.primary_media_image = blog_media_key
        post.attached_media.append(blog_media_key)
    else:
        post.primary_media_image = None

    post.put()
    return post

def edit_post(post, cleaned_data):
    post.is_published = cleaned_data['publish']
    post.content = cleaned_data['content']
    post.title = cleaned_data['title']

    if (not post.published_date) and cleaned_data['publish']:
        # Set the published date - note this is never unset if it is unchecked
        post.published_date = datetime.now()

    post.put()
    return post


'''
def get_published_posts(page_number=1, limit=POSTS_PER_PAGE):
    """
    Return a list of posts
    TODO: Pagination works on the idea that you have been to that page before, if first hit.. fire off deferred task to populate the index
    """

    memcache_cursor_key = 'public_blog_page_cursor_%s'
    page_cursor_cache_key = memcache_cursor_key % page_number
    start_cursor = memcache.get(page_cursor_cache_key)

    if start_cursor:
        start_cursor = Cursor(urlsafe=start_cursor)
    #start_cursor = False

    #if not cursor and page_number > 1:
    #    # Groom the index

    q = BlogPost.query().filter().order(-BlogPost.published_date)
    q.filter(BlogPost.published_date > PUBLISHED_DATE_MIN)

    if start_cursor:
        entities, next_cursor, more = q.fetch_page(limit, start_cursor=start_cursor)
    else:
        entities, next_cursor, more = q.fetch_page(limit)

    page_cursor_cache_key = memcache_cursor_key % (page_number + 1)     
    memcache.set(page_cursor_cache_key, next_cursor.urlsafe())

    return entities, next_cursor, more
'''


def build_index(q):
    total_pages = 0 # This is determined...
    total_items = 0

    limit = 10

    next_cursor = None
    cursors = [None] # Represents 1st page cursor

    qo = ndb.QueryOptions(keys_only=True)

    while True:
        entities, next_cursor, more = q.fetch_page(limit, start_cursor=next_cursor, options=qo)
        if next_cursor:
            cursors.append(next_cursor.urlsafe())
        total_items += len(entities)

        if not more:
            break

    total_pages = len(cursors)
    logging.debug(total_pages)
    logging.debug(total_items)

    for c in cursors:
        logging.warning(c)
    
    # Construct index
    return {'total_pages': total_pages, 'total_items': total_items, 'cursors': cursors}


#####################
# Images
#####################
def get_images():
    # TODO: Paginate this, etc
    entities = BlogMedia.query().order(-BlogMedia.gcs_filename).fetch(1000)
    
    return entities
