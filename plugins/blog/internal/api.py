import logging
from plugins.blog.models import BlogPost
from google.appengine.datastore.datastore_query import Cursor

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