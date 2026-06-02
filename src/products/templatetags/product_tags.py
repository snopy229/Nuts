from django import template


from src.products.models import ProductDetailPage

register = template.Library()


@register.inclusion_tag("partials/products.html", takes_context=True)
def render_product(context):
    request = context["request"]
    products = ProductDetailPage.objects.all()
    taste = request.GET.get("taste")
    mass = request.GET.get("mass")

    if taste:
        products = products.filter(taste=taste)
    if mass:
        products = products.filter(mass=mass)

    preview = products[:6]
    has_more = products.count() > 6
    return {
        "products": preview,
        "has_more": has_more,
    }
