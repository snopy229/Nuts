from django.db import models

from src.checkouts.models import Orders
from src.transaction.enum.transaction_status import TransactionStatus


# Create your models here.
class Transaction(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="transactions")
    cost = models.IntegerField(verbose_name="Стоимость")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        verbose_name="Статус",
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.WAITING,
    )
