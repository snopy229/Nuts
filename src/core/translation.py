from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import GardenInfo


@register(GardenInfo)
class GardenInfoTR(TranslationOptions):
    fields = (
        "tab_1",
        "tab_2",
        "tab_3",
        "tab_4",
    )
