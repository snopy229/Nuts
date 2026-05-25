# Create your models here.
import random

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from src.core.blocks import PhotoWithoutDescriptionBlock, TabBlock


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
    title = models.CharField("Упаковка", unique=True, max_length=255)

    def __str__(self):
        return self.title


class ProductTaste(models.Model):
    title = models.CharField("Название вкуса", unique=True, max_length=255)

    def __str__(self):
        return self.title


class ProductWeight(models.Model):
    title = models.CharField("Масса", unique=True, max_length=255)

    def __str__(self):
        return self.title


class ProductDetailPage(Page):
    gallery = StreamField([("images", ImageChooserBlock())], use_json_field=True)
    package = models.ForeignKey(ProductPackage, on_delete=models.PROTECT)
    taste = models.ForeignKey(ProductTaste, on_delete=models.PROTECT)
    nuts_type = models.CharField(max_length=255)
    nuts_title = models.CharField(max_length=255)
    compound = models.TextField()
    cost = models.IntegerField()
    mass = models.ForeignKey(ProductWeight, on_delete=models.PROTECT)
    energy_value = models.CharField(max_length=255)
    shelf_life = models.CharField(max_length=255)
    discount = models.IntegerField(null=True, blank=True)
    article = models.CharField(max_length=20, unique=True, blank=True, null=True)
    blocks = StreamField([("block", TabBlock())], max_num=4, min_num=1, use_json_field=True)
    created_at = models.DateTimeField(auto_now_add=True)
    template = "products_detail_page.html"
    parent_page_types = ["ProductsPage"]
    content_panels = Page.content_panels + [
        FieldPanel("gallery", heading="Галерея"),
        FieldPanel("package", heading="Упаковка"),
        FieldPanel("taste", heading="Вкус"),
        FieldPanel("nuts_type", heading="Вид ореха"),
        FieldPanel("nuts_title", heading="Название ореха"),
        FieldPanel("compound", heading="Состав"),
        FieldPanel("mass", heading="Масса"),
        FieldPanel("energy_value", heading="Энергетическая ценность"),
        FieldPanel("shelf_life", heading="Срок годности"),
        FieldPanel("discount", heading="Скидка(%)"),
        FieldPanel("blocks", heading="Разделы"),
    ]

    @property
    def cost_with_discount(self):
        if self.discount:
            return self.cost - self.discount
        return self.cost

    def save(self, *args, **kwargs):
        if self.article:
            return super().save()
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.article:  # nosec
            random_digit_count = random.randint(3, 5)  # nosec
            random_part = "".join([random.choice("0123456789") for i in range(random_digit_count)])  # nosec

            self.article = f"{self.id}{random_part}"  # nosec
            self.__class__.objects.filter(pk=self.id).update(article=self.article)
