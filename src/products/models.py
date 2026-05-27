# Create your models here.
import random
from datetime import timedelta

from django.db import models
from django.utils import timezone
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from src.core.blocks import PhotoWithoutDescriptionBlock, TabBlock


class ProductsPage(Page):
    upper_banner = StreamField(
        [("banner", PhotoWithoutDescriptionBlock(label="Баннер"))],
        max_num=1,
        min_num=1,
        use_json_field=True,
        verbose_name="Верхний баннер",
    )
    description = RichTextField(verbose_name="Описание")
    gallery = StreamField(
        [
            ("gallery", ImageChooserBlock(label="Изображение")),
        ],
        verbose_name="Галерея",
    )
    template = "products_page.html"
    parent_page_types = ["main.MainPage"]
    max_count = 1
    content_panels = Page.content_panels + [
        FieldPanel("upper_banner"),
        FieldPanel("description"),
        FieldPanel("gallery"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        tastes = ProductTaste.objects.all()
        weights = ProductWeight.objects.all()
        context["tastes"] = tastes
        context["weights"] = weights
        return context


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
    gallery = StreamField(
        [("images", ImageChooserBlock(label="Изображение"))],
        use_json_field=True,
        verbose_name="Галерея",
    )
    package = models.ForeignKey(ProductPackage, on_delete=models.PROTECT, verbose_name="Упаковка")
    taste = models.ForeignKey(ProductTaste, on_delete=models.PROTECT, verbose_name="Вкус")
    nuts_type = models.CharField(max_length=255, verbose_name="Вид ореха")
    nuts_title = models.CharField(max_length=255, verbose_name="Название ореха")
    compound = models.TextField(verbose_name="Состав")
    cost = models.IntegerField(verbose_name="Цена")
    mass = models.ForeignKey(ProductWeight, on_delete=models.PROTECT, verbose_name="Масса")
    energy_value = models.CharField(max_length=255, verbose_name="Энергетическая ценность")
    shelf_life = models.CharField(max_length=255, verbose_name="Срок годности")
    discount = models.IntegerField(null=True, blank=True, verbose_name="Скидка (%)")
    article = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Артикул")
    blocks = StreamField(
        [("block", TabBlock(label="Раздел"))],
        max_num=4,
        min_num=1,
        use_json_field=True,
        verbose_name="Разделы",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    template = "products_detail_page.html"
    parent_page_types = ["ProductsPage"]
    content_panels = Page.content_panels + [
        FieldPanel("gallery"),
        FieldPanel("package"),
        FieldPanel("cost"),
        FieldPanel("taste"),
        FieldPanel("nuts_type"),
        FieldPanel("nuts_title"),
        FieldPanel("compound"),
        FieldPanel("mass"),
        FieldPanel("energy_value"),
        FieldPanel("shelf_life"),
        FieldPanel("discount"),
        FieldPanel("blocks"),
    ]

    @property
    def cost_with_discount(self):
        if self.discount:
            return self.cost - self.discount
        return self.cost

    @property
    def is_new(self):
        return timezone.now() - self.created_at <= timedelta(days=30)

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
