from merkabah.core import grids as merkabah_datatable
from django.core import urlresolvers

class BlogPostActionColumn(merkabah_datatable.DatatableColumn):
    def render_content(self, obj):
        #link = urlresolvers.reverse('merkabah_admin_blog_post_edit', args=(obj.key.urlsafe(),))
        #output = '<a href="%s" class="button">Edit</a>' % link
        output = ''
        link = '#'
        #link = obj.get_permalink()
        output += '<a href="%s" class="button">View</a>' % link
        
        return output        

class BlogCategoryActionColumn(merkabah_datatable.DatatableColumn):
    def render_content(self, obj):
        link = '#'
        #link = urlresolvers.reverse('merkabah_admin_blog_category_edit', args=(obj.key.urlsafe(),))
        return '<a href="%s" class="button">Edit</a>' % link
        

class BlogPostGrid(merkabah_datatable.Datatable):
    
    # Column Definitions
	title = merkabah_datatable.DatatableColumn()
	slug = merkabah_datatable.DatatableColumn()
	created_date = merkabah_datatable.DatatableColumn()
	published_date = merkabah_datatable.DatatableColumn()
	actions = BlogPostActionColumn()
		
	column_order = ['title' , 'slug', 'published_date', 'created_date', 'actions']
	
	
class BlogCategoryGrid(merkabah_datatable.Datatable):
    # Column Definitions
    name = merkabah_datatable.DatatableColumn()
    slug = merkabah_datatable.DatatableColumn()
    actions = BlogCategoryActionColumn()

    column_order = ['name', 'slug', 'actions']
    

class BlogMediaThumbnailColumn(merkabah_datatable.DatatableColumn):
    def render_content(self, obj):
        output = '<a href="/blog_image/%s/"><img class="thumbnail" src="/blog_image/%s/" style="max-width:100px;max-height:50px;" alt="Placeholder Image" /></a>' % (obj.key.urlsafe(),obj.key.urlsafe())
        return output


class BlogMediaGrid(merkabah_datatable.Datatable):
    thumb = BlogMediaThumbnailColumn()
    filename = merkabah_datatable.DatatableColumn()
    content_type = merkabah_datatable.DatatableColumn()
    size = merkabah_datatable.DatatableColumn()
    actions = BlogCategoryActionColumn()
    column_order = ['thumb', 'filename', 'content_type', 'size', 'actions']