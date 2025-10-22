import humanize
from django.utils import timezone
from django import template

register = template.Library()

@register.filter
def get_obj_attr(obj, attr):
    try:
        return obj[str(attr)]
    except Exception as err:
        return None

@register.filter()
def timestamp_to_date(obj):
    return timezone.datetime.fromtimestamp(int(obj))

@register.filter()
def naturaldelta(obj):
    return humanize.naturaldelta(obj)

@register.filter()
def split(value, arg):
    """
    Split a string by the given delimiter
    Usage: {{ value|split:"," }}
    """
    return value.split(arg)

@register.filter()
def mul(value, arg):
    """
    Multiply a value by the given argument
    Usage: {{ value|mul:100 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter()
def http_status_20x_only(pages):
    """
    Filter pages to only include those with 20x HTTP status codes (200-299)
    Usage: {{ data.pages|http_status_20x_only }}
    """
    if not pages:
        return []
    
    filtered_pages = []
    for page in pages:
        if isinstance(page, dict) and 'http_status' in page:
            http_status = page['http_status']
            # Check if status code is in 200-299 range
            if isinstance(http_status, int) and 200 <= http_status <= 299:
                filtered_pages.append(page)
    
    return filtered_pages

@register.filter()
def http_status_300x_only(pages):
    """
    Filter pages to only include those with 300x HTTP status codes (300-399)
    Usage: {{ data.pages|http_status_300x_only }}
    """
    if not pages:
        return []
    
    filtered_pages = []
    for page in pages:
        if isinstance(page, dict) and 'http_status' in page:
            http_status = page['http_status']
            # Check if status code is in 300-399 range
            if isinstance(http_status, int) and 300 <= http_status <= 399:
                filtered_pages.append(page)
    
    return filtered_pages

@register.filter()
def http_status_400x_only(pages):
    """
    Filter pages to only include those with 400x HTTP status codes (400-499)
    Usage: {{ data.pages|http_status_400x_only }}
    """
    if not pages:
        return []
    
    filtered_pages = []
    for page in pages:
        if isinstance(page, dict) and 'http_status' in page:
            http_status = page['http_status']
            # Check if status code is in 400-499 range
            if isinstance(http_status, int) and 400 <= http_status <= 499:
                filtered_pages.append(page)
    
    return filtered_pages
