from django import template  #for this see in template layer documentation ,for programmers->custom filters and tags
from math import floor


register = template.Library()


 
@register.simple_tag
def get_order_status_class(status):   #tshirt is object
    if status == 'COMPLETED':
        return "success"          #means returning a CSS class
    elif status == 'PENDING':
        return "warning"
    else:
        return 'info'
