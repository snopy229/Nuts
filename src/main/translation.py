from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import MainPage, Contacts


@register(Contacts)
class ContactsTR(TranslationOptions):
    fields = ("office_address", "production_address")


@register(MainPage)
class MainPageTR(TranslationOptions):
    fields = (
        "upper_banner",
        "products_title",
        "products_description",
        "middle_banner",
        "benefits_title",
        "benefits_description",
        "walnut",
        "hazelnut",
        "rose_hip",
        "down_banner",
    )
