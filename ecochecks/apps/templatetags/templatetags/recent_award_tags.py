from django import template
from domains.models import Domain

register = template.Library()

@register.inclusion_tag("recent_award.html")
def recent_award():
    recent_award_list = Domain.objects.filter(awarded_date__isnull=False).order_by("-awarded_date")[0:7]
    return {"recent_award_list": recent_award_list}
