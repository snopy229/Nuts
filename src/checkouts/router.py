from ninja import Router

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
    return {"quantity": cart_item.quantity}
