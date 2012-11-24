from merkabah.core import grids as merkabah_datatable
from django.core import urlresolvers

class BlogPostActionColumn(merkabah_datatable.DatatableColumn):
    def render_content(self, obj):
        link = urlresolvers.reverse('merkabah_admin_blog_post_edit', args=(obj.key.urlsafe(),))
        return '<a href="%s" class="button">Edit</a>' % link


class BlogCategoryActionColumn(merkabah_datatable.DatatableColumn):
    def render_content(self, obj):
        link = urlresolvers.reverse('merkabah_admin_blog_category_edit', args=(obj.key.urlsafe(),))
        return '<a href="%s" class="button">Edit</a>' % link
        

class BlogPostGrid(merkabah_datatable.Datatable):
    
    # Column Definitions
	title = merkabah_datatable.DatatableColumn()
	slug = merkabah_datatable.DatatableColumn()
	created_date = merkabah_datatable.DatatableColumn()
	actions = BlogPostActionColumn()
		
	column_order = ['title' , 'slug' , 'created_date', 'actions']
	
	
class BlogCategoryGrid(merkabah_datatable.Datatable):

        # Column Definitions
    	name = merkabah_datatable.DatatableColumn()
    	slug = merkabah_datatable.DatatableColumn()
    	actions = BlogCategoryActionColumn()

    	column_order = ['name', 'slug', 'actions']
    