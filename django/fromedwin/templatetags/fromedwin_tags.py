from django import template

register = template.Library()

@register.filter
def get_obj_attr(obj, attr):
    try:
        return obj[str(attr)]
    except Exception as err:
        return None
