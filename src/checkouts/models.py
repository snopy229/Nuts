from cities_light.models import Region, City, Country
from django.db import models

from src.checkouts.enum.payment_type import PaymentType
from src.checkouts.enum.delivert_type import DeliveryType
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


class Checkouts(models.Model):
    cart = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name="checkouts")
    delivery_type = models.CharField(
        verbose_name="Способ доставки",
        max_length=20,
        choices=DeliveryType.choices,
        default=DeliveryType.NEW_POST,
    )
    delivery_country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Страна"
    )
    delivery_region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Регион")
    delivery_city = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Город")
    courier_address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес")
    payment_type = models.CharField(
        verbose_name="Способ оплаты",
        max_length=20,
        choices=PaymentType.choices,
        default=PaymentType.BANK_TRANSFER,
    )
    created_at = models.DateTimeField(auto_now_add=True)
