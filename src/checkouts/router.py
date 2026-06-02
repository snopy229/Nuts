import json
from functools import wraps

from django.http import HttpResponse
from django.template.loader import render_to_string
from ninja import Router, Form
from ninja.security import django_auth

from src.checkouts.models import CartItem

router = Router()


def get_cart_totals(user):
    items = list(CartItem.objects.filter(user=user).select_related("product"))
    total_items = sum(item.quantity for item in items)
    total_sum = sum(item.product.cost_with_discount * item.quantity for item in items)
    return total_items, str(total_sum)


def not_staff(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return 403, {"detail": "Forbidden"}
        return func(request, *args, **kwargs)

    return wrapper


def render_quantity_input(request, product_id: int, quantity: int) -> HttpResponse:
    total_items, total_sum = get_cart_totals(request.user)
    cart_item = CartItem.objects.select_related("product").get(user=request.user, product_id=product_id)
    full_cost = cart_item.product.cost_with_discount * quantity
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
                "total_sum": total_sum,
                "product_id": product_id,
                "quantity": quantity,
                "full_cost": str(full_cost),
            }
        }
    )
    return response


@router.post("/add-product", auth=django_auth)
@not_staff
def add_product(request, product_id: int = Form(...)):
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product_id=product_id, defaults={"quantity": 1}
    )
    if not created:
        pass

    total_items, total_sum = get_cart_totals(request.user)

    if not created:
        response = HttpResponse(status=204)
        response["HX-Trigger"] = json.dumps({"cartUpdated": {"total_items": total_items, "total_sum": total_sum}})
        return response

    html = render_to_string("partials/cart_item.html", {"item": cart_item}, request=request)
    response = HttpResponse(html)
    response["HX-Trigger"] = json.dumps({"cartUpdated": {"total_items": total_items, "total_sum": total_sum}})
    return response


@router.post("/plus-product", auth=django_auth)
@not_staff
def plus_product(request, product_id: int = Form(...)):
    cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
    if not cart_item:
        return 404, {"detail": "Not found"}
    cart_item.quantity += 1
    cart_item.save(update_fields=["quantity"])
    return render_quantity_input(request, product_id, cart_item.quantity)


@router.post("/minus-product", auth=django_auth)
@not_staff
def minus_product(request, product_id: int = Form(...)):
    cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
    if not cart_item:
        return 404, {"detail": "Not found"}
    cart_item.quantity -= 1
    if cart_item.quantity <= 0:
        cart_item.delete()
        total_items, total_sum = get_cart_totals(request.user)
        response = HttpResponse("")
        response["HX-Trigger"] = json.dumps({"cartUpdated": {"total_items": total_items, "total_sum": total_sum}})
        return response
    cart_item.save(update_fields=["quantity"])
    return render_quantity_input(request, product_id, cart_item.quantity)


@router.post("/set-quantity", auth=django_auth)
@not_staff
def set_quantity(request, product_id: int = Form(...), quantity: int = Form(...)):
    if quantity < 1:
        quantity = 1

    cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
    if not cart_item:
        return 404, {"detail": "Not found"}

    cart_item.quantity = quantity
    cart_item.save(update_fields=["quantity"])
    return render_quantity_input(request, product_id, quantity)


@router.post("/delete-product", auth=django_auth)
@not_staff
def delete_product(request, product_id: int = Form(...)):
    cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
    if not cart_item:
        return 404, ""
    cart_item.delete()
    total_items, total_sum = get_cart_totals(request.user)
    response = HttpResponse("")
    response["HX-Trigger"] = json.dumps({"cartUpdated": {"total_items": total_items, "total_sum": total_sum}})
    return response
