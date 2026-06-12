from django.db import models

from src.checkouts.models import Orders
from src.transaction.enum.transaction_status import TransactionStatus
from src.user.models import User


# Create your models here.
class Transaction(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="transactions", verbose_name="Заказ")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions", verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(
        verbose_name="Статус",
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.WAITING,
    )
