from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Dodaje lub aktualizuje parametry w URL
    """
    query_params = context['request'].GET.copy()
    
    # Update with new parameters
    for key, value in kwargs.items():
        query_params[key] = value
    
    # Remove empty parameters if needed
    query_dict = {k: v for k, v in query_params.items() if v}
    
    return urlencode(query_dict)