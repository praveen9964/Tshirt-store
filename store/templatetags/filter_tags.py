from django import template  #for this see in template layer documentation ,for programmers->custom filters and tags
from math import floor


register = template.Library()


 
@register.simple_tag
def selected_attr(request_slug,slug):   
    if request_slug == slug:     #rhs slug if from the database
        return "selected"          
    else:
        return ""
