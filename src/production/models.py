from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from src.news_and_articles.models import NewsAndArticlesDetailPage, NewsAndArticlesPage
from src.core.blocks import VideoBlock, VideoWithPreviewBlock


class ProductionPage(Page):
    upper_banner = StreamField(
        [
            ("banner", VideoBlock()),
        ],
        max_num=1,
        min_num=1,
        use_json_field=True,
    )
    page_title = models.CharField(max_length=255)
    description = models.TextField()
    gallery = StreamField(
        [
            ("photo", ImageChooserBlock()),
            ("video", VideoWithPreviewBlock()),
        ],
        min_num=1,
        use_json_field=True,
    )
    founder_photo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
    )
    founder_fullname = models.CharField(max_length=255)
    founder_information = models.TextField()
    founder_quote = models.TextField()
    history = models.TextField()
    down_banner = StreamField(
        [
            ("banner", VideoBlock()),
        ],
        max_num=1,
        min_num=1,
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("upper_banner", heading="Верхний баннер"),
        FieldPanel("page_title", heading="Название страницы"),
        FieldPanel("description", heading="Описание"),
        FieldPanel("gallery", heading="Галерея"),
        FieldPanel("founder_photo", heading="Фото основателя"),
        FieldPanel("founder_fullname", heading="Имя основателя"),
        FieldPanel("founder_information", heading="Информация о основателе"),
        FieldPanel("founder_quote", heading="Цитата основателя"),
        FieldPanel("down_banner", heading="Нижний баннер"),
    ]
    template = "production_page.html"
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]

    def get_context(self, request):
        context = super().get_context(request)

        news_queryset = NewsAndArticlesDetailPage.objects.live().order_by("-created_at")
        previous_news_list = list(news_queryset[:4])

        for news in previous_news_list:
            news_text = ""
            for block in news.description:
                if block.block_type == "text":
                    news_text = block.value
                    break
            news.first_text = news_text

        context["news"] = previous_news_list
        news_page = NewsAndArticlesPage.objects.live().first()
        if news_page:
            context["news_page"] = news_page

        return context
