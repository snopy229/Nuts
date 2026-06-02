from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryType(models.TextChoices):
    NEW_POST = "new_post", _("Новая почта")
    COURIER = "courier", _("Курьер по Одессе")
    PICKUP = "pickup", _("Самовывоз")
