from django import template
import docutils

register = template.Library()

@register.filter
def rstify(text):
    return docutils.core.publish_parts(text, writer_name='html')['html_body']