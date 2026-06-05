from django.db import models

from src.checkouts.models import Orders
from src.transaction.enum.transaction_status import TransactionStatus
from src.user.models import User


# Create your models here.
class Transaction(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="transactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        verbose_name="Статус",
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.WAITING,
    )

    @property
    def cost(self):
        return sum(item.product.cost_for_user(item.user) * item.quantity for item in self.order.cart.all())
