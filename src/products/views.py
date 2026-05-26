from django.template.response import TemplateResponse

from src.products.models import ProductDetailPage


def products_more(request):
    offset = int(request.GET.get("offset") or 0)
    limit = 6

    qs = ProductDetailPage.objects.live()

    taste = request.GET.get("taste")
    mass = request.GET.get("mass")
    order = request.GET.get("order", "asc")

    if taste:
        qs = qs.filter(taste__id=taste)
    if mass:
        qs = qs.filter(mass__id=mass)

    if order == "desc":
        qs = qs.order_by("-cost")
    else:
        qs = qs.order_by("cost")

    total = qs.count()
    blocks = qs[offset : offset + limit]
    has_more = total > offset + limit

    return TemplateResponse(
        request,
        "partials/product_more.html",
        {
            "products": blocks,
            "next_offset": offset + limit,
            "has_more": has_more,
            "taste": taste or "",
            "mass": mass or "",
            "order": order,
        },
    )
