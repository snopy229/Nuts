from typing import List, Any
from django import template

register = template.Library()


@register.filter
def split(value: Any, arg: str) -> List[str]:
    return str(value).split(arg)
