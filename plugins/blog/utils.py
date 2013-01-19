from plugins.blog import models as blog_models

from google.appengine.api import memcache
from plugins.blog import models as blog_models
import datetime

def get_published_posts(page_number=0):
    memcache_cursor_key = 'public_blog_page_cursor_%s'
    query = blog_models.BlogPost.query().order(-blog_models.BlogPost.published_date).filter(blog_models.BlogPost.published_date > datetime.datetime(1980,1,1))

    page_cursor_cache_key = memcache_cursor_key % page_number
    start_cursor = memcache.get(page_cursor_cache_key)

    if (page_number > 1 and start_cursor):
        posts, cursor, more = query.fetch_page(10, start_cursor=start_cursor)
    else:
        posts, cursor, more = query.fetch_page(10)
    
    page_cursor_cache_key = memcache_cursor_key % (page_number + 1)     
    memcache.set(page_cursor_cache_key, cursor)
    return posts
    
def get_all_posts(page_number=0):
    memcache_cursor_key = 'admin_blog_page_cursor_%s'    
    query = blog_models.BlogPost.query().order(-blog_models.BlogPost.created_date)

    page_cursor_cache_key = memcache_cursor_key % page_number
    start_cursor = memcache.get(page_cursor_cache_key)

    if (page_number > 1 and start_cursor):
        posts, cursor, more = query.fetch_page(1000, start_cursor=start_cursor)
    else:
        posts, cursor, more = query.fetch_page(1000)

    page_cursor_cache_key = memcache_cursor_key % (page_number + 1)     
    memcache.set(page_cursor_cache_key, cursor)
    return posts