from ninja import Router, Query
from django.template.loader import render_to_string
from django.http import HttpResponse
from src.products.models import ProductDetailPage

router = Router()


@router.get("/products-more")
def products_more(
    request,
    offset: int = Query(0),
    taste: str | None = Query(None),
    mass: str | None = Query(None),
    order: str | None = Query(None),
):
    limit = 6
    qs = ProductDetailPage.objects.all()
    if taste:
        qs = qs.filter(taste__id=taste)
    if mass:
        qs = qs.filter(mass__id=mass)

    qs = qs.order_by("-cost" if order == "desc" else "cost")
    total = qs.count()
    blocks = qs[offset : offset + limit]
    has_more = total > offset + limit

    html = render_to_string(
        "partials/product_more.html",
        {
            "products": blocks,
            "next_offset": offset + limit,
            "has_more": has_more,
            "taste": taste or "",
            "mass": mass or "",
            "order": order or "",
        },
        request=request,
    )
    return HttpResponse(html)
