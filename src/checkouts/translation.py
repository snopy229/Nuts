from modeltranslation.translator import TranslationOptions

from src.checkouts.models import ThanksForOrderPage
from modeltranslation.decorators import register


@register(ThanksForOrderPage)
class ThanksForOrderPageTR(TranslationOptions):
    fields = ("banner",)
