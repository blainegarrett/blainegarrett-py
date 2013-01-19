from django.template import Library, Node, Variable, TemplateSyntaxError, VariableDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.template.loader import render_to_string
from bs4 import BeautifulSoup
import logging    
import re
register = Library()

@register.simple_tag
def newest_blog_posts():
    # TODO: Make this a cached node eventually
    from plugins.blog import utils as blog_utils

    posts = blog_utils.get_published_posts()
    output = ''
    for post in posts:
        output += '<li><a href="%s" title="%s">%s</a></li>' % (post.get_permalink(), post.title, post.title)    
    output = '<div class="footer-heading"><h3>From the Blog</h3></div><div class="row-fluid"><div class="span12"><ul>%s</ul></div></div>' % output
    return output

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

def truncate_html_words(s, num, end_text='...'):
    """Truncates HTML to a certain number of words (not counting tags and
    comments). Closes opened tags if they were correctly closed in the given
    html. Takes an optional argument of what should be used to notify that the
    string has been truncated, defaulting to ellipsis (...).

    Newlines in the HTML are preserved.
    """
    s = force_unicode(s)
    length = int(num)
    if length <= 0:
        return u''
    html4_singlets = ('br', 'col', 'link', 'base', 'img', 'param', 'area', 'hr', 'input')
    # Set up regular expressions
    re_words = re.compile(r'&.*?;|<.*?>|(\w[\w-]*)', re.U)
    re_tag = re.compile(r'<(/)?([^ ]+?)(?: (/)| .*?)?>')
    # Count non-HTML words and keep note of open tags
    pos = 0
    prev_pos = 0
    end_text_pos = 0
    words = 0
    open_tags = []
    while words <= length or word_not_found:
        prev_pos = pos
        m = re_words.search(s, pos)
        if not m:
            # Checked through whole string
            break
        pos = m.end(0)
        
        if m.group(0) == '<!--more-->':
            end_text_pos = prev_pos
            word_not_found = False
            break
                    
        if m.group(1):
            # It's an actual non-HTML word
            words += 1
            if words == length:
                end_text_pos = pos
            continue
        # Check for tag
        tag = re_tag.match(m.group(0))
        if not tag or end_text_pos:
            # Don't worry about non tags or tags after our truncate point
            continue
        closing_tag, tagname, self_closing = tag.groups()
        tagname = tagname.lower()  # Element names are always case-insensitive
        if self_closing or tagname in html4_singlets:
            pass
        elif closing_tag:
            # Check for match in open tags list
            try:
                i = open_tags.index(tagname)
            except ValueError:
                pass
            else:
                # SGML: An end tag closes, back to the matching start tag, all unclosed intervening start tags with omitted end tags
                open_tags = open_tags[i+1:]
        else:
            # Add it to the start of the open tags list
            open_tags.insert(0, tagname)
    if words <= length and word_not_found:
        # Don't try to close tags if we don't need to truncate
        return s
    out = s[:end_text_pos]
    if end_text:
        out += ' ' + end_text
    # Close any tags still open
    for tag in open_tags:
        out += '</%s>' % tag
    # Return string
    return out


@register.simple_tag
def render_excerpt(post):
    from django.utils import text, html
    
    VALID_TAGS = ['p']
    
    soup = BeautifulSoup(post.content, "html.parser")

    for tag in soup.findAll(True):
        if tag.name not in VALID_TAGS:
            tag.replaceWithChildren()
            
    stripped_html = force_unicode(soup.renderContents())
    return force_unicode(text.truncate_html_words(stripped_html, 100))


@register.simple_tag
def render_content(content):
    # Apply rendering filter plugins
    #TODO: Make this more modular
    def wp_caption_shortcode_proc(m):
        classes = ['thumbnail']
        attrs = str(m.group(2))
        if 'align="alignleft"' in attrs:
            classes.append('alignleft')
        elif 'align="alignright"' in attrs:
                classes.append('alignright')
        
        if classes:
            attrs += ' class="%s"' %  " ".join(classes)
        
        #return '<div' + attrs + '>' + m.group(4) + '<div class="caption"><h4>Brad Majors, CEO</h4><p>Etiam fermentum convallis ullamcorper. Curabitur vel vestibulum leo.</p></div></div>'
        return '<div' + attrs + '>' + m.group(4) + '</div>'
    
    # WP Caption shortcode
    content = re.sub(r"(\[caption)([^\]]*)(])(.*)(\[/caption\])", wp_caption_shortcode_proc, content)
    
    # nl2br
    content = content.replace('\n','<br />\n')
    return mark_safe(content)    