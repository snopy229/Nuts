from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from src.transaction.models import Transaction
from .models import Orders, CartItem


@receiver(post_save, sender=Orders)
def create_transaction(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(order=instance, user=instance.user)


@receiver(post_save, sender=CartItem)
def update_order_cost_on_cartitem_change(sender, instance, **kwargs):
    for order in instance.checkouts.all():
        order.cost = sum(item.full_cost for item in order.cart.all())
        order.save(update_fields=["cost"])


@receiver(m2m_changed, sender=Orders.cart.through)
def update_order_cost_on_cart_change(sender, instance, action, **kwargs):
    if action in ("post_add", "post_remove", "post_clear"):
        instance.cost = sum(item.full_cost for item in instance.cart.all())
        instance.save(update_fields=["cost"])
