from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductTags(models.TextChoices):
    NONE = "none", _("Нету")
    NEW = "new", _("Новый")
    DISCOUNT = "discount", _("Скидка")
