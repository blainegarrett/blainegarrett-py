
import logging
from datetime import timedelta
from datetime import datetime # Note: This is mocked specifically in testing

from google.appengine.ext import ndb
from google.appengine.api import memcache


def cache_set(key, value, time=None, category=None, write_entity=True):
    """
    """

    if write_entity:
        now = datetime.now()

        expiration_date = None

        if time:
            delta = timedelta(seconds=time)
            expiration_date = now + delta

        if not category:
            category = []

        if category and not isinstance(category, list):
            category = [category]

        ds_key = ndb.Key('MemcacheEntity', key)
        e = MemcacheEntity(key=ds_key,
            value=value,
            expiration_time=time,
            expires=expiration_date,
            category=category)
        future = e.put_async(use_memcache=False)

    # Setup memcache operation
    memcached_return_value = memcache.set(key, value) #, time) TODO: Get expiration working..

    # Get async value
    if write_entity:
        db_key_put = future.get_result()

    return True


def cache_delete(key):
    """
    """

    ds_key = ndb.Key('MemcacheEntity', key)
    future = ds_key.delete_async(use_memcache=False)
    memcache.delete(key)
    future.get_result()

    return True


def cache_get(key):
    """
    Retrieve an item from the cache
    """

    # Check if in memcache
    value = memcache.get(key)
    if value:
        return value

    # else, check datastore backup
    ds_key = ndb.Key('MemcacheEntity', key)
    ds_entity = ds_key.get()

    if not ds_entity:
        return None

    logging.debug('Memcache miss for key %s, but there is a datastore entity.' % key)
    expiration = ds_entity.expires
    value = ds_entity.value

    if expiration and  expiration < datetime.now():
        return None # value is stale, could should would delete the db Entity

    # Update memcache value since it was a miss...
    cache_set(key, value, ds_entity.expiration_time, write_entity=False)

    return value


def cache_invalidate(category):
    """
    Given a category, invalidate all items with this category
    """

    future = MemcacheEntity.query(MemcacheEntity.category == category).fetch_async(
        keys_only=True, use_memcache=False)

    result = future.get_result()

    ds_keys_to_delete = []
    memcache_keys_to_delete = []

    for ds_key in result:
        ds_keys_to_delete.append(ds_key)
        memcache_keys_to_delete.append(ds_key.id())

    # Delete datastore entites
    ndb.delete_multi(ds_keys_to_delete)
    memcache.delete_multi(memcache_keys_to_delete)

    return memcache_keys_to_delete # Return a list of keys that were deleted


class MemcacheEntity(ndb.Model):
    """
    A lightweight entity to function as a memcache backup in systems where
    memcache keys don't exisit in pool very long due to overuse.

    datastore entity key is itself the memcache key.
    """

    value = ndb.PickleProperty()
    created_date = ndb.DateTimeProperty(auto_now=True)
    expiration_time = ndb.IntegerProperty() # The `time` value you would pass to memcache.set
    expires = ndb.DateTimeProperty() # Created timestamp + the expiration time for easy querying
    category = ndb.StringProperty(indexed=True, repeated=True)
