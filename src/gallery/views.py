from django.template.response import TemplateResponse

from src.gallery.models import Gallery


def gallery_more(request):
    offset = int(request.GET.get("offset") or 0)
    limit = 6
    gallery = Gallery.get()
    all_blocks = list(gallery.content)
    blocks = all_blocks[offset : offset + limit]
    has_more = len(all_blocks) > offset + limit

    return TemplateResponse(
        request,
        "partials/gallery_more.html",
        {
            "blocks": blocks,
            "next_offset": offset + limit,
            "has_more": has_more,
            "offset": offset,
        },
    )
