"""
Blog Plugin
"""

from plugins.blog.forms import BlogPostForm
from plugins.blog.internal.api import get_posts
from plugins.blog.internal.api import create_post

from plugins.blog.datatables import BlogPostGrid

from merkabah.core.controllers import TemplateResponse, FormDialogResponse, AlertResponse, FormResponse, FormErrorResponse, CloseFormResponse

class BlogPlugin(object):
    name = 'Blog'
    entity_nice_name = 'post'
    entity_plural_name = 'posts'
    query_method = get_posts

    def process_index(self, request, context, *args, **kwargs):
        """
        Driver switchboard logic
        """
        
        entities, cursor, more = get_posts(limit=1000)
        context['grid'] = BlogPostGrid(entities, request, context)

        context['plugin'] = self
        return TemplateResponse('admin/plugin/index.html', context)


    def process_create(self, request, context, *args, **kwargs):
        form = BlogPostForm()

        if request.POST:
            form = BlogPostForm(request.POST)
            if form.is_valid():

                p = create_post(form.cleaned_data)
                return AlertResponse("Form Saved..."), CloseFormResponse('create_form')

                return AlertResponse("Form Saved..."), merkabah_controllers.CloseFormResponse('create_form')
            else:
                return FormErrorResponse(form, id='create_form')

        if request.is_ajax():
            return FormResponse(form, id='create_form', title="Create a new Blog Post", target_url='/madmin/plugin/blog/create/', target_action='create')
        return TemplateResponse('admin/plugin/inline_form_wrapper.html', context)


# Register Plugin
pluginClass = BlogPlugin