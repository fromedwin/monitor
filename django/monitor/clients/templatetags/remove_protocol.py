from django import template

register = template.Library()

@register.filter
def remove_protocol(value):
    return value.replace("http://","").replace("https://","")