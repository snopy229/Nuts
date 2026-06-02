from django.db import models

from src.products.models import ProductDetailPage
from src.user.models import User


# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(ProductDetailPage, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def full_cost(self):
        return self.product.cost_with_discount * self.quantity

    class Meta:
        unique_together = ("user", "product")
