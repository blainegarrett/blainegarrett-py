from merkabah.core import forms as merkabah_forms
from django import forms

class BlogPostForm(merkabah_forms.MerkabahBaseForm):
    slug = forms.CharField(label='Slug', max_length=100, required=True)    
    title = forms.CharField(label='Title', max_length=100, required=True)
    body = forms.CharField(label='Body', required=True, widget=forms.Textarea())
    
    
class BlogCategoryForm(merkabah_forms.MerkabahBaseForm):
    slug = forms.CharField(label='Slug', max_length=100, required=True)    
    name = forms.CharField(label='Name', max_length=100, required=True)