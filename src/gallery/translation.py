from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import GalleryPage, Gallery


@register(GalleryPage)
class GalleryPageTR(TranslationOptions):
    fields = ("banner",)


@register(Gallery)
class GalleryTR(TranslationOptions):
    fields = ("content",)
