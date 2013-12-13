from merkabah.core import forms as merkabah_forms
from django import forms
from plugins.blog.internal import models as blog_models

class ImageUploadForm(merkabah_forms.MerkabahBaseForm):
    title = forms.CharField(max_length=50)
    the_file  = forms.FileField()


class BlogPostForm(merkabah_forms.MerkabahBaseForm):
    slug = forms.CharField(label='Slug', max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Slug'}))
    title = forms.CharField(label='Title', max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(label='Content', required=True, widget=forms.Textarea(attrs={'placeholder': 'Content', 'class': 'ckeditor'}))
    publish = forms.BooleanField(required=False)
        
    categories = forms.MultipleChoiceField(required=False, choices=[])
    primary_media_image  = forms.ChoiceField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)

        # Primary Image
        media_choices = [('', 'None Selected')]
        media_entities = blog_models.BlogMedia.query().fetch(1000)
        for media_entity in media_entities:
            media_choices.append((media_entity.key.urlsafe(), media_entity.filename))
        
        self.fields['primary_media_image'].choices = media_choices
        
        # Categories
        categories_choices = []
        category_entities = blog_models.BlogCategory.query().fetch(1000)
        for category_entity in category_entities:
            categories_choices.append((category_entity.key.urlsafe(), category_entity.name))
        
        self.fields['categories'].choices = categories_choices
    
class BlogCategoryForm(merkabah_forms.MerkabahBaseForm):
    slug = forms.CharField(label='Slug', max_length=100, required=True)    
    name = forms.CharField(label='Name', max_length=100, required=True)
    

class BlogMediaForm(merkabah_forms.MerkabahBaseForm):
    image_file  = forms.FileField(required=False)
    is_upload  = forms.CharField(required=True)