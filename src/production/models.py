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
            ("banner", VideoBlock(label="Баннер")),
        ],
        max_num=1,
        min_num=1,
        use_json_field=True,
        verbose_name="Верхний баннер",
    )
    page_title = models.CharField(max_length=255, verbose_name="Название страницы")
    description = models.TextField(verbose_name="Описание")
    gallery = StreamField(
        [
            ("photo", ImageChooserBlock(label="Фото")),
            ("video", VideoWithPreviewBlock(label="Видео")),
        ],
        min_num=1,
        use_json_field=True,
        verbose_name="Галерея",
    )
    founder_photo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        verbose_name="Фото основателя",
    )
    founder_fullname = models.CharField(max_length=255, verbose_name="Имя основателя")
    founder_information = models.TextField(verbose_name="Информация об основателе")
    founder_quote = models.TextField(verbose_name="Цитата основателя")
    history = models.TextField(verbose_name="История")
    down_banner = StreamField(
        [
            ("banner", VideoBlock(label="Баннер")),
        ],
        max_num=1,
        min_num=1,
        use_json_field=True,
        verbose_name="Нижний баннер",
    )
    content_panels = Page.content_panels + [
        FieldPanel("upper_banner"),
        FieldPanel("page_title"),
        FieldPanel("description"),
        FieldPanel("gallery"),
        FieldPanel("founder_photo"),
        FieldPanel("founder_fullname"),
        FieldPanel("founder_information"),
        FieldPanel("founder_quote"),
        FieldPanel("history"),
        FieldPanel("down_banner"),
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
