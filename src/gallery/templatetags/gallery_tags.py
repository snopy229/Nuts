from django import template
from src.gallery.models import Gallery

register = template.Library()


@register.inclusion_tag("partials/gallery.html")
def render_gallery():
    gallery = Gallery.get()
    blocks = list(gallery.content)
    preview = blocks[:6]
    has_more = len(blocks) > 6
    return {
        "gallery_blocks": preview,
        "has_more": has_more,
    }


@register.filter
def mod(value, arg):
    return value % arg
