from django.template import Library, Node, Variable, TemplateSyntaxError, VariableDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django import forms
from django.template.loader import render_to_string

register = Library()

@register.simple_tag
def carousel():
    panels = [
        {'image_path' : '/static/mural_.jpg',
        'title': u'Se\u00F1or Wong Mural',
        'description' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In pretium pretium turpis.'
        },
        {'image_path' : '/static/aotw_.jpg',
        'title': 'All Over the Walls',
        'description' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In pretium pretium turpis.'
        },
        {'image_path' : '/static/livingpainting_.jpg',
        'title': 'Living Painting',
        'description' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In pretium pretium turpis.'
        },
        
    ]    
    return mark_safe(render_to_string('homepage_carousel.html', {'panels' : panels}))
