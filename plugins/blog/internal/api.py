import logging
from datetime import datetime

from google.appengine.datastore.datastore_query import Cursor
from google.appengine.api import memcache

from plugins.blog.internal.models import BlogPost
from plugins.blog.constants import POSTS_PER_PAGE
from plugins.blog.constants import PUBLISHED_DATE_MIN


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

    logging.error(entities, next_cursor)

    for entity in entities:
        logging.warning(entity.title)

    return entities, next_cursor, more


def get_published_posts(page_number=None, limit=POSTS_PER_PAGE):
    """
    Return a list of posts
    TODO: Pagination works on the idea that you have been to that page before, if first hit.. fire off deferred task to populate the index
    """

    memcache_cursor_key = 'public_blog_page_cursor_%s'
    page_cursor_cache_key = memcache_cursor_key % page_number
    start_cursor = memcache.get(page_cursor_cache_key)

    #if not cursor and page_number > 1:
    #    # Groom the index

    q = BlogPost.query().filter().order(-BlogPost.published_date)
    q.filter(BlogPost.published_date > PUBLISHED_DATE_MIN)

    if start_cursor:
        entities, next_cursor, more = q.fetch_page(limit, start_cursor=start_cursor)
    else:
        entities, next_cursor, more = q.fetch_page(limit)

    logging.error(entities, next_cursor)

    page_cursor_cache_key = memcache_cursor_key % (page_number + 1)     
    memcache.set(page_cursor_cache_key, next_cursor)

    return entities, next_cursor, more
