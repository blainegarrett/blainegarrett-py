from django.template import Library, Node, Variable, TemplateSyntaxError, VariableDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.template.loader import render_to_string
import logging
import re

from plugins.blog.internal import api as blog_api

register = Library()


@register.simple_tag
def newest_blog_posts():
    # TODO: Make this a cached node eventually
    
    posts, cursor, more = blog_api.get_published_posts(page_number=1)
    output = '<div class="posts">\
        <div class="headline"><h2>Recent Blog Entries</h2></div>'
    for post in posts[:2]:
        image_filename = ''
        if post.primary_media_image:
            image_filename = post.primary_media_image.get().gcs_filename

        output += '<dl class="dl-horizontal">\
            <dt><a href="%s"><img src="http://commondatastorage.googleapis.com/blaine-garrett/%s" alt="%s" /></a></dt>\
            <dd>\
                <p><a href="%s" title="%s">%s</a></p> \
            </dd>\
        </dl>' % (post.get_permalink(), image_filename, post.title, post.get_permalink(), post.title, post.title)

    output += '</div>'
    
    
    return output

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
    from bs4 import BeautifulSoup
    from django.utils import text, html
    
    VALID_TAGS = ['p']

    content = post.content

    content = re.sub(r"(\[caption)([^\]]*)(])(.*)(\[/caption\])", '', content)
    content = re.sub(r'(\[source((code)*? lang(uage)*?)*?=([\'"]*?)(python)([\'"]*?)])(.*?)(\[/source(code)*?\])', '', content, flags=re.MULTILINE|re.DOTALL)

    content = re.sub(r"(\[caption)([^\]]*)(])(.*)(\[/caption\])", '', content)
    content = re.sub(r"(\[youtube:)([^\]]*)(])", '', content)
    
    soup = BeautifulSoup(content, "html.parser")

    for tag in soup.findAll(True):
        if tag.name not in VALID_TAGS:
            tag.replaceWithChildren()
            
    stripped_html = force_unicode(soup.renderContents())
    return force_unicode(text.truncate_html_words(stripped_html, 50))


@register.simple_tag
def render_content(content):
    # Apply rendering filter plugins
    #TODO: Make this more modular
    
    def wp_youtube_shortcode_proc(m):
        
        if m.group(2):
            video_id = m.group(2).split('watch?v=')[1]
            return '<iframe width="420" height="315" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>' % (video_id)
        else:
            return m.group(0)

    def wp_code_shortcode_proc(m):
        if m.group(8) and m.group(6):
            attrs = 'class="brush: %s;"' % m.group(6)
            code = m.group(8).replace('\n','<NEWLINE />')
            return '<pre ' + attrs + '>' + code + '</pre>'
        else:
            code = m.group(8).replace('\n','<NEWLINE />')
            return '<pre>' + code + '</pre>'

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
    content = re.sub(r'(\[source((code)*? lang(uage)*?)*?=([\'"]*?)(python)([\'"]*?)])(.*?)(\[/source(code)*?\])', wp_code_shortcode_proc, content, flags=re.MULTILINE|re.DOTALL)

    content = re.sub(r"(\[caption)([^\]]*)(])(.*)(\[/caption\])", wp_caption_shortcode_proc, content)
    content = re.sub(r"(\[youtube:)([^\]]*)(])", wp_youtube_shortcode_proc, content)
    
    
    # nl2br
    content = content.replace('\n','<br />\n')
    content = content.replace('<NEWLINE />','\n')

    return mark_safe(content)    