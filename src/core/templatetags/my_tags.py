from django import template
from src.core.models import GardenInfo

register = template.Library()


@register.inclusion_tag("partials/gardens_info.html")
def render_garden_info():
    return {"snippet": GardenInfo.get()}
