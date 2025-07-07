from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def url_is(context, url_name, project_id):
    url = reverse(url_name, kwargs={'id': project_id})
    if context['request'].path == url:
        return True
    return False

@register.simple_tag(takes_context=True)
def url_start_with(context, url_name, project_id):
    url = reverse(url_name, kwargs={'id': project_id})
    if context['request'].path.startswith(url):
        return True
    return False
