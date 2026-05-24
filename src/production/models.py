from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from src.core.blocks import PhotoBlock, VideoBlock


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
            ("gallery", ImageChooserBlock()),
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
    down_banner = StreamField(
        [
            ("banner", PhotoBlock()),
        ],
        max_num=1,
        min_num=1,
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("upper_banner", heading="Верхний баннер"),
        FieldPanel("upper_banner", heading="Название страницы"),
        FieldPanel("upper_banner", heading="Описание"),
        FieldPanel("upper_banner", heading="Галерея"),
        FieldPanel("upper_banner", heading="Фото основателя"),
        FieldPanel("upper_banner", heading="Имя основателя"),
        FieldPanel("upper_banner", heading="Информация о основателе"),
        FieldPanel("upper_banner", heading="Цитата основателя"),
        FieldPanel("upper_banner", heading="Нижний баннер"),
    ]
    template = "production_page.html"
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
