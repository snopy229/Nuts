from django.db import models
from django.utils.translation import gettext_lazy as _


class TransactionStatus(models.TextChoices):
    APPROVED = "approved", _("Платеж принят")
    WAITING = "waiting", _("В ожидании оплаты")
