from merkabah.core import datatable as merkabah_datatable
from django.core import urlresolvers

class BlogPostActionColumn(merkabah_datatable.DatatableColumn):
    def render_content(self, obj):
        #link = urlresolvers.reverse('merkabah_admin_blog_post_edit', args=(obj.key.urlsafe(),))
        #output = '<a href="%s" class="button">Edit</a>' % link
        output = ''
        link = '#'
        link = obj.get_permalink()
        output += '<a href="%s" class="button">View</a>' % link

        link = '/madmin/plugin/blog/edit/?post_key=%s' % obj.key.urlsafe()
        output += '<a href="%s" class="button action">Edit</a>' % link

        link = '/madmin/plugin/blog/delete/?post_key=%s' % obj.key.urlsafe()
        output += '<a href="%s" class="button action">Delete</a>' % link


        return output

class BlogCategoryActionColumn(merkabah_datatable.DatatableColumn):
    def render_content(self, obj):
        link = '#'
        #link = urlresolvers.reverse('merkabah_admin_blog_category_edit', args=(obj.key.urlsafe(),))
        return '<a href="%s" class="button">Edit</a>' % link

class BlogGroupActions(object):
    def render_content(self):
        #link = '/madmin/plugin/blog/delete_image/?media_key=%s' % obj.key.urlsafe()
        link = '/madmin/plugin/blog/create/'
        return '<a href="%s" class="action btn-primary btn">Create</a>' % link
    
class BlogImageActionColumn(merkabah_datatable.DatatableColumn):
    def render_content(self, obj):
        link = '/madmin/plugin/blog/delete_image/?media_key=%s' % obj.key.urlsafe()
        return '<a href="%s" class="action button">Delete</a>' % link    

class BlogPostGrid(merkabah_datatable.Datatable):
    
    # Column Definitions
	title = merkabah_datatable.DatatableColumn()
	slug = merkabah_datatable.DatatableColumn()
	created_date = merkabah_datatable.DatatableColumn()
	published_date = merkabah_datatable.DatatableColumn()
	actions = BlogPostActionColumn()

	column_order = ['title' , 'slug', 'published_date', 'created_date', 'actions']
	group_actions = BlogGroupActions()
	
class BlogCategoryGrid(merkabah_datatable.Datatable):
    # Column Definitions
    name = merkabah_datatable.DatatableColumn()
    slug = merkabah_datatable.DatatableColumn()
    actions = BlogCategoryActionColumn()

    column_order = ['name', 'slug', 'actions']
    

class BlogMediaThumbnailColumn(merkabah_datatable.DatatableColumn):
    def render_content(self, obj):
        output = 'http://commondatastorage.googleapis.com/blaine-garrett/' + obj.gcs_filename +'<br /><a href="http://commondatastorage.googleapis.com/blaine-garrett/' + obj.gcs_filename +'"><img class="thumbnail" src="http://commondatastorage.googleapis.com/blaine-garrett/' + obj.gcs_filename +'" style="max-width:100px;max-height:50px;" alt="Placeholder Image" /></a>'
        return output


class BlogMediaGroupActions(object):
    def render_content(self):
        link = '/madmin/plugin/blog/images_create/'
        return '<a href="%s" class="action btn-primary btn">Create</a>' % link

class BlogMediaGrid(merkabah_datatable.Datatable):
    thumb = BlogMediaThumbnailColumn()
    filename = merkabah_datatable.DatatableColumn()
    gcs_filename = merkabah_datatable.DatatableColumn()
    content_type = merkabah_datatable.DatatableColumn()
    size = merkabah_datatable.DatatableColumn()
    actions = BlogImageActionColumn()
    column_order = ['thumb', 'filename', 'gcs_filename', 'content_type', 'size', 'actions']
    
    group_actions = BlogMediaGroupActions()



