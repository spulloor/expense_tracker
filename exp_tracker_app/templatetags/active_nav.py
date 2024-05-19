from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag(takes_context=True)
def active_url(context, url_name):
    request = context['request']
    if resolve(request.path_info).url_name == url_name:
        return 'active'
    return ''