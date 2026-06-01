from django.db.models import Sum
from ninja import Router
from ninja.security import django_auth

from checkouts.models import CartItem

router = Router()


@router.post("/add-product")
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
def minus_product(request, product_id: int):
    cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
    if not cart_item:
        return 404, {"detail": "Not found"}
    cart_item.quantity -= 1
    if cart_item.quantity <= 0:
        cart_item.delete()
        return {"deleted": True}
    cart_item.save(update_fields=["quantity"])
    return {
        "deleted": True,
        "total_items": CartItem.objects.filter(user=request.user).aggregate(total=Sum("quantity"))["total"] or 0,
    }
