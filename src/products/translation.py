from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import ProductsPage, ProductDetailPage


@register(ProductsPage)
class ProductsPageTR(TranslationOptions):
    fields = (
        "upper_banner",
        "description",
    )


@register(ProductDetailPage)
class ProductDetailPageTR(TranslationOptions):
    pass
