from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentType(models.TextChoices):
    BANK_TRANSFER = "bank_transfer", _("Безналичный расчет")
    LIQPAY = "liqpay", _("LiqPay / Приват24")
    CASH = "cash", _("Наличными при получении")
