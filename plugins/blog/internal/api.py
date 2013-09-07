import logging
from plugins.blog.internal.models import BlogPost
from google.appengine.datastore.datastore_query import Cursor
from datetime import datetime


def get_post_by_slug(slug):
    post = BlogPost.query(BlogPost.slug == slug).get()
    #TODO: Check if published or not

    return post

def get_posts(cursor=None, limit=200):
    """
    Return a list of posts
    """
    if cursor:
        cursor = Cursor(urlsafe=cursor)

    q = BlogPost.query().order(-BlogPost.published_date)

    if cursor:
        entities, next_curs, more = q.fetch_page(limit)
    else:
        entities, next_curs, more = q.fetch_page(limit, start_cursor=cursor)

    logging.error(entities, next_curs)

    for entity in entities:
        logging.warning(entity.title)

    return entities, next_curs, more


def get_published_posts(cursor=None, limit=10):
    """
    Return a list of posts
    """
    if cursor:
        cursor = Cursor(urlsafe=cursor)

    q = BlogPost.query().filter().order(-BlogPost.published_date)
    q.filter(BlogPost.published_date > datetime(1980,1,1))

    if cursor:
        entities, next_curs, more = q.fetch_page(limit, start_cursor=cursor)
    else:
        entities, next_curs, more = q.fetch_page(limit)

    logging.error(entities, next_curs)

    for entity in entities:
        logging.warning(entity.title)

    return entities, next_curs, more