from django.db.models.signals import post_save
from django.dispatch import receiver

from src.transaction.models import Transaction
from .models import Orders


@receiver(post_save, sender=Orders)
def create_transaction(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(order=instance, user=instance.user)
