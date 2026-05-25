# Create your models here.
from django.db import models
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from src.core.blocks import PhotoWithoutDescriptionBlock


class ProductsPage(Page):
    upper_banner = StreamField([("banner", PhotoWithoutDescriptionBlock())], max_num=1, min_num=1, use_json_field=True)
    description = RichTextBlock()
    gallery = StreamField(
        [
            ("gallery", ImageChooserBlock()),
        ]
    )


class ProductPackage(models.Model):
    title = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.title


class ProductTaste(models.Model):
    title = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.title
