# Create your models here.
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtailmedia.blocks import VideoChooserBlock


class NewsAndArticlesPage(Page):
    page_title = models.CharField(max_length=255)
    description = models.TextField()

    content_panels = Page.content_panels + [
        FieldPanel("page_title", heading="Верхний баннер"),
        FieldPanel("description", heading="Оплата"),
    ]
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["NewsAndArticlesDetailPage"]
    template = "news_and_articles.html"


class NewsAndArticlesDetailPage(Page):
    preview = StreamField(
        [
            ("image", ImageChooserBlock()),
            ("video", VideoChooserBlock()),
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
