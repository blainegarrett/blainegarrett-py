from google.appengine.ext import ndb

'''
class Person(db.Model):
    firstname = db.TextProperty()
    lastname = db.TextProperty()
'''    

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


class BlogCategory(ndb.Model):
    nice_name = 'Category'

    slug = ndb.StringProperty()
    name = ndb.StringProperty()


class BlogPost(ndb.Model):
    nice_name = 'Posts'
    
    title = ndb.StringProperty()
    slug = ndb.StringProperty()
    body = ndb.TextProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    modified_date = ndb.DateTimeProperty(auto_now=True)
    categories = ndb.KeyProperty(repeated=True, kind=BlogCategory)
    primary_image_blob = ndb.BlobKeyProperty()
    #published_data = ndb.DateTimeProperty()
    
    def get_permalink(self):
        dt = self.created_date
        return '/%s/%s/%s/%s' % (dt.year, dt.month, dt.day, self.slug)
            
    
kind_name_map = {
    'post' : BlogPost,
    'category' : BlogCategory
}