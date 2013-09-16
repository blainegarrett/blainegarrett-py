"""
Blog Plugin
"""

from plugins.blog.forms import BlogPostForm
from plugins.blog.internal.api import get_posts
#from plugins.blog.datatables import BlogPostGrid
from merkabah.core.controllers import TemplateResponse, FormDialogResponse, AlertResponse, FormResponse, FormErrorResponse

class BlogPlugin(object):
    name = 'Blog'
    entity_nice_name = 'post'
    entity_plural_name = 'posts'
    query_method = get_posts

    def process_index(self, request, context, *args, **kwargs):
        """
        Driver switchboard logic
        """
        
        #entities, cursor, more = get_posts()
        #context['grid'] = BlogPostGrid(entities, request, context)

        context['plugin'] = self
        return TemplateResponse('admin/plugin/index.html', context)

    
    
    def process_create(self, request, context, *args, **kwargs):
        form = BlogPostForm()

        if request.POST:
            form = BlogPostForm(request.POST)
            if form.is_valid():

                raise Exception('FORM VALID')
                
                c = Contact(firstname=form.cleaned_data['firstname'], lastname=form.cleaned_data['lastname'], email=form.cleaned_data['email'])
                c.put()

                return AlertResponse("Form Saved..."), merkabah_controllers.CloseFormResponse('create_form')
            else:
                return FormErrorResponse(form, id='create_form')

        if request.is_ajax():
            return FormResponse(form, id='create_form', title="Please Enter Contact Info", target_url='/madmin/plugin/blog/create/', target_action='create')
        return TemplateResponse('admin/plugin/inline_form_wrapper.html', context)
    
    
    '''
    def process_create(self, request, context, *args, **kwargs):
        """
        Handler for creating a post
        """
        
        context['form'] = BlogPostForm()
        

        
        context['plugin'] = self

        response = TemplateResponse('admin/plugin/form.html', context)
        rendered = unicode(response)

        if request.is_ajax():
            return FormResponse(form, id='create_form', title="Please Enter Contact Info", target_url='/test/', target_action='display_form')

            return FormDialogResponse('create_form', 'Create Post', rendered, context)

        context['rendered_form'] = rendered
        return TemplateResponse('admin/plugin/inline_form_wrapper.html', context)
    '''

# Register Plugin
pluginClass = BlogPlugin