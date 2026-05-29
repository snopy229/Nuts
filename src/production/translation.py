from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import ProductionPage


@register(ProductionPage)
class ProductionPageTR(TranslationOptions):
    fields = (
        "upper_banner",
        "page_title",
        "description",
        "founder_fullname",
        "founder_information",
        "founder_quote",
        "history",
        "down_banner",
    )
