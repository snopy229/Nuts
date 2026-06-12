import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from src.products.models import ProductDetailPage

COOKIE_NAME = "guest_cart"


def get_guest_cart(request) -> dict[int, int]:
    raw = request.COOKIES.get(COOKIE_NAME, "{}")
    print("COOKIES:", request.COOKIES)
    print("RAW:", raw)
    try:
        result = {int(k): v for k, v in json.loads(raw).items()}
        print("PARSED:", result)
        return result
    except (json.JSONDecodeError, ValueError):
        return {}


def set_guest_cart(response, cart: dict[int, int]):
    response.set_cookie(
        COOKIE_NAME,
        json.dumps(cart),
        max_age=60 * 60 * 24 * 30,
        httponly=True,
        samesite="Lax",
    )


def render_quantity_input_guest(request, product_id: int, quantity: int, cart: dict) -> HttpResponse:
    product = get_object_or_404(ProductDetailPage, id=product_id)
    full_cost = product.cost_with_discount * quantity
    total_items = sum(cart.values())
    products = {p.id: p for p in ProductDetailPage.objects.filter(id__in=cart.keys())}
    total_sum = sum(products[pid].cost_with_discount * qty for pid, qty in cart.items() if pid in products)

    response = HttpResponse(f"""
        <input type="text"
               name="quantity"
               value="{quantity}"
               class="quantity_input"
               data-product-id="{product_id}"
               hx-post="/api/checkouts/set-quantity"
               hx-vals='{{"product_id": {product_id}}}'
               hx-trigger="change, keyup delay:500ms"
               hx-target="this"
               hx-swap="outerHTML">
    """)
    response["HX-Trigger"] = json.dumps(
        {
            "cartUpdated": {
                "total_items": total_items,
                "total_sum": str(total_sum),
                "product_id": product_id,
                "quantity": quantity,
                "full_cost": str(full_cost),
            }
        }
    )
    return response


def _make_guest_item(product, quantity):
    return type(
        "GuestCartItem",
        (),
        {
            "product": product,
            "quantity": quantity,
            "product_id": product.id,
        },
    )()
