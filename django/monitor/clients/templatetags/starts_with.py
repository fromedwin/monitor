from django import template

register = template.Library()

@register.simple_tag
def starts_with(value, arg):
    return value.startswith(arg)