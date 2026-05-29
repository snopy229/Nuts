# Create your models here.
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from src.gallery.models import Gallery
from src.core.blocks import VideoWithPreviewBlock


class NewsAndArticlesPage(Page):
    page_title = models.CharField(max_length=255, verbose_name="Заголовок страницы")
    description = models.TextField(verbose_name="Описание")

    content_panels = Page.content_panels + [
        FieldPanel("page_title"),
        FieldPanel("description"),
    ]
    min_count = 1
    max_count = 1
    parent_page_types = ["main.MainPage"]
    subpage_types = ["NewsAndArticlesDetailPage"]
    template = "news_and_articles.html"

    def get_context(self, request):
        context = super().get_context(request)

        news_queryset = NewsAndArticlesDetailPage.objects.live().order_by("-created_at")

        top_news = news_queryset[:1].first()
        context["latest_news"] = top_news

        previous_news_list = list(news_queryset[1:4])

        if top_news:
            first_text = ""
            for block in top_news.description:
                if block.block_type == "text":
                    first_text = block.value
                    break
            context["latest_news_first_text"] = first_text

        for news in previous_news_list:
            news_text = ""
            for block in news.description:
                if block.block_type == "text":
                    news_text = block.value
                    break
            news.first_text = news_text

        context["previous_news"] = previous_news_list
        gallery = Gallery.objects.first()
        if gallery and gallery.content:
            context["first_block"] = gallery.content[0]
        else:
            context["first_block"] = None

        return context


class NewsAndArticlesDetailPage(Page):
    preview = StreamField(
        [
            ("image", ImageChooserBlock(label="Изображение")),
            ("video", VideoWithPreviewBlock(label="Видео")),
        ],
        max_num=1,
        min_num=1,
        use_json_field=True,
        verbose_name="Превью",
    )
    page_title = models.CharField(verbose_name="Название")
    description = StreamField(
        [
            ("text", RichTextBlock(min_num=1, label="Текст")),
            ("image", ImageChooserBlock(label="Изображение")),
        ],
        verbose_name="Информация",
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    content_panels = Page.content_panels + [
        FieldPanel("preview"),
        FieldPanel("page_title"),
        FieldPanel("description"),
    ]

    parent_page_types = ["NewsAndArticlesPage"]
    template = "news_and_articles_detail.html"

    def get_context(self, request):
        context = super().get_context(request)
        news_queryset = NewsAndArticlesDetailPage.objects.live().order_by("-created_at")

        context["latest_news"] = news_queryset[:3]
        return context
