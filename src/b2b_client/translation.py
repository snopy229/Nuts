from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from src.b2b_client.models import B2BClientPage


@register(B2BClientPage)
class B2BClientPageTR(TranslationOptions):
    fields = (
        "upper_banner",
        "page_title",
        "description",
        "big_supermarket",
        "shops",
        "horecd",
        "fitness_club",
        "cake_baker",
        "down_banner",
    )
