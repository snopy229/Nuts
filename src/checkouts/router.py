from functools import wraps

from django.db.models import Sum
from django.http import HttpResponse
from ninja import Router, Form
from ninja.security import django_auth

from checkouts.models import CartItem

router = Router()


def not_staff(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return 403, {"detail": "Forbidden"}
        return func(request, *args, **kwargs)

    return wrapper


@router.post("/add-product", auth=django_auth)
@not_staff
def add_product(request, product_id: int, quantity: int):
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product_id=product_id, defaults={"quantity": quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save(update_fields=["quantity"])
    return {
        "quantity": cart_item.quantity,
        "total_items": CartItem.objects.filter(user=request.user).aggregate(total=Sum("quantity"))["total"] or 0,
    }


@router.post("/plus-product", auth=django_auth)
@not_staff
def plus_product(request, product_id: int):
    cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
    if not cart_item:
        return 404, {"detail": "Not found"}
    cart_item.quantity += 1
    cart_item.save(update_fields=["quantity"])
    return {
        "quantity": cart_item.quantity,
        "total_items": CartItem.objects.filter(user=request.user).aggregate(total=Sum("quantity"))["total"] or 0,
    }


@router.post("/minus-product", auth=django_auth)
@not_staff
def minus_product(request, product_id: int):
    cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
    if not cart_item:
        return 404, {"detail": "Not found"}
    cart_item.quantity -= 1
    if cart_item.quantity <= 0:
        cart_item.delete()
        return {
            "deleted": True,
            "total_items": CartItem.objects.filter(user=request.user).aggregate(total=Sum("quantity"))["total"] or 0,
        }
    cart_item.save(update_fields=["quantity"])
    return {
        "quantity": cart_item.quantity,
        "total_items": CartItem.objects.filter(user=request.user).aggregate(total=Sum("quantity"))["total"] or 0,
    }


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
    new_qty = quantity

    html_string = f"""
        <input type="text"
               name="quantity"
               value="{new_qty}"
               id="quantity-{product_id}"
               class="quantity_input"
               hx-post="/api/checkouts/set-quantity"
               hx-vals='{{"product_id": {product_id}}}'
               hx-trigger="change, keyup delay:500ms"
               hx-target="this"
               hx-swap="outerHTML">
    """
    return HttpResponse(html_string)
