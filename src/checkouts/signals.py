from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Orders, Transaction


@receiver(post_save, sender=Orders)
def create_transaction(sender, instance, created, **kwargs):
    if created:
        cost = sum(item.product.price * item.quantity for item in instance.cart.all())
        Transaction.objects.create(order=instance, cost=cost)
