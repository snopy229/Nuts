from django.db.models.signals import post_save
from django.dispatch import receiver

from src.transaction.models import Transaction
from .models import Orders


@receiver(post_save, sender=Orders)
def create_transaction(sender, instance, created, **kwargs):
    if created:
        cost = sum(item.product.cost_with_discount * item.quantity for item in instance.cart.all())
        Transaction.objects.create(order=instance, cost=cost)
