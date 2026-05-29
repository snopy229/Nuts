from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import PaymentAndDeliveryPage


@register(PaymentAndDeliveryPage)
class PaymentAndDeliveryPageTR(TranslationOptions):
    fields = ("upper_banner", "payment", "delivery", "refund", "down_banner")
