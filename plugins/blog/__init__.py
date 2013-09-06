"""
Blog Plugin
"""
from plugins.blog.internal.api import get_posts
from plugins.blog.datatables import BlogPostGrid
from merkabah.admin.controllers import TemplateResponse

class BlogPlugin(object):
    name = 'Blog'
    entity_nice_name = 'post'
    entity_plural_name = 'posts'
    query_method = get_posts

    def process_index(self, request, context, *args, **kwargs):
        """
        Driver switchboard logic
        """

        entities, cursor, more = get_posts()
        context['grid'] = BlogPostGrid(entities, request, context)
        return TemplateResponse(self, 'admin/plugin/index.html', context)
        
    
    #def process_create(self, request, context, *args, **kwargs):
    #    context['form'] = 'main'
    #    return TemplateResponse(self, 'admin/plugin/form.html', context)


# Register Plugin
pluginClass = BlogPlugin