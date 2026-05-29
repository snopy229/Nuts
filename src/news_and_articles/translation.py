from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import NewsAndArticlesPage, NewsAndArticlesDetailPage


@register(NewsAndArticlesPage)
class NewsAndArticlesPageTR(TranslationOptions):
    fields = ("page_title", "description")


@register(NewsAndArticlesDetailPage)
class NewsAndArticlesDetailPage(TranslationOptions):
    fields = (
        "page_title",
        "description",
    )
