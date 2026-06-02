from django.db import models

from src.checkouts.models import Orders


# Create your models here.
class Transaction(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="transactions")
    cost = models.IntegerField(verbose_name="Стоимость")
    created_at = models.DateTimeField(auto_now_add=True)
