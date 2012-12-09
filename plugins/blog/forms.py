from merkabah.core import forms as merkabah_forms
from django import forms
from plugins.blog import models as blog_models
import logging

class BlogPostForm(merkabah_forms.MerkabahBaseForm):
    
    slug = forms.CharField(label='Slug', max_length=100, required=True)    
    title = forms.CharField(label='Title', max_length=100, required=True)
    body = forms.CharField(label='Body', required=True, widget=forms.Textarea())
    
    categories = forms.MultipleChoiceField(required=False, choices=[])
    image_file  = forms.FileField(required=False)    
    
    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)
        
        categories_choices = []
        category_entities = blog_models.BlogCategory.query().fetch(1000)
        for category_entity in category_entities:
            categories_choices.append((category_entity.key.urlsafe(), category_entity.name))
        
        self.fields['categories'].choices = categories_choices
    
class BlogCategoryForm(merkabah_forms.MerkabahBaseForm):
    slug = forms.CharField(label='Slug', max_length=100, required=True)    
    name = forms.CharField(label='Name', max_length=100, required=True)
    