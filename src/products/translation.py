from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import ProductsPage, ProductDetailPage, ProductPackage, ProductWeight, ProductTaste


@register(ProductPackage)
class ProductPackageTR(TranslationOptions):
    fields = ("title",)


@register(ProductWeight)
class ProductWeightTR(TranslationOptions):
    fields = ("title",)


@register(ProductTaste)
class ProductTasteTR(TranslationOptions):
    fields = ("title",)


@register(ProductsPage)
class ProductsPageTR(TranslationOptions):
    fields = (
        "upper_banner",
        "description",
    )


@register(ProductDetailPage)
class ProductDetailPageTR(TranslationOptions):
    pass
