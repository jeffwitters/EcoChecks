from django import template

register = template.Library()

@register.inclusion_tag("top_nav.html")
def top_nav(tab):
    return {"tab": tab}
