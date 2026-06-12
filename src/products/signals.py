from django.db.models.signals import post_save
from django.dispatch import receiver

from src.checkouts.models import CartItem
from src.products.models import ProductDetailPage
from src.user.models import User


@receiver(post_save, sender=User)
def update_cart_prices(sender, instance, **kwargs):
    cart_items = CartItem.objects.filter(user=instance).select_related("product")
    for item in cart_items:
        item.unit_cost = item.product.cost_for_user(instance)
    CartItem.objects.bulk_update(cart_items, ["saved_cost"])


@receiver(post_save, sender=ProductDetailPage)
def update_cart_prices_on_product_change(sender, instance, **kwargs):
    cart_items = CartItem.objects.filter(product=instance).select_related("user")
    for item in cart_items:
        item.unit_cost = instance.cost_for_user(item.user)
    CartItem.objects.bulk_update(cart_items, ["saved_cost"])
