# Create your models here.
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from src.core.blocks import VideoWithPreviewBlock


class NewsAndArticlesPage(Page):
    page_title = models.CharField(max_length=255)
    description = models.TextField()

    content_panels = Page.content_panels + [
        FieldPanel("page_title", heading="Верхний баннер"),
        FieldPanel("description", heading="Описание"),
    ]
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
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

        return context


class NewsAndArticlesDetailPage(Page):
    preview = StreamField(
        [
            ("image", ImageChooserBlock()),
            ("video", VideoWithPreviewBlock()),
        ],
        max_num=1,
        min_num=1,
        use_json_field=True,
    )
    page_title = models.CharField()
    description = StreamField(
        [
            ("text", RichTextBlock(min_num=1)),
            ("image", ImageChooserBlock()),
        ]
    )
    created_at = models.DateField(auto_now_add=True)

    content_panels = Page.content_panels + [
        FieldPanel("preview", heading="Превью"),
        FieldPanel("page_title", heading="Название"),
        FieldPanel("description", heading="Информация"),
    ]

    parent_page_types = ["NewsAndArticlesPage"]
    template = "news_and_articles_detail.html"
