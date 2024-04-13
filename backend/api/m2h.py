from markdown import Markdown
from bleach import clean,css_sanitizer
import re
url_pattern = r'^https://www\.youtube\.com/embed/[\w-]+(\?.*)?$'
def sanitize_src(tag, name, value):
    if name == 'src' and not re.match(url_pattern, value):
        return None
    return value
def m2h(data:str) -> str:
    md = Markdown(extensions=["pymarkdown-video", "extra"])
    tags = {
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul', 'div', 'iframe'
    }
    attr = {
        'a': ['href', 'title'],
        'abbr': ['title'],
        'acronym': ['title'],
        "*":"style",
        'iframe': ['src', 'width', 'height', 'frameborder', 'allowfullscreen']
    }
    css = css_sanitizer.CSSSanitizer(allowed_css_properties=["color", "font-weight","font-family","font-size"])

    data = clean(data, tags=tags, attributes=sanitize_src,css_sanitizer=css)
    data = md.convert(data)
    return data

