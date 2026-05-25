# Create your models here.
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from src.core.blocks import PhotoWithoutDescriptionBlock


class ProductsPage(Page):
    upper_banner = StreamField([("banner", PhotoWithoutDescriptionBlock())], max_num=1, min_num=1, use_json_field=True)
    description = RichTextField()
    gallery = StreamField(
        [
            ("gallery", ImageChooserBlock()),
        ]
    )
    template = "products_page.html"
    parent_page_types = ["wagtailcore.Page"]
    content_panels = Page.content_panels + [
        FieldPanel("upper_banner", heading="Верхний баннер"),
        FieldPanel("description", heading="Описание"),
        FieldPanel("gallery", heading="Галерея"),
    ]


class ProductPackage(models.Model):
    title = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.title


class ProductTaste(models.Model):
    title = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.title
