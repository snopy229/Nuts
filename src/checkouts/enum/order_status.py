from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderStatus(models.TextChoices):
    WAITING = "waiting", _("В ожидании")
    SENT = "sent", _("Отправлено")
