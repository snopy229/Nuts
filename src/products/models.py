# Create your models here.

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from src.core.blocks import PhotoWithoutDescriptionBlock


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


class ProductDetailPage(models.Model):
    title = models.CharField
    gallery = models.ManyToManyField("core.Gallery", verbose_name="gallery")
    mass = models.ForeignKey(ProductWeight, on_delete=models.CASCADE, verbose_name="Масса")
    energy_value = models.IntegerField(verbose_name="Энергетическая ценность")
    taste = models.ForeignKey(ProductTaste, on_delete=models.CASCADE, verbose_name="Вкус")
    package = models.ForeignKey(ProductPackage, on_delete=models.CASCADE, verbose_name="Упаковка")
    shelf_life = models.TextField(verbose_name="Срок годности")
    description = models.TextField(verbose_name="Описание")
    description_photo = models.ImageField("/product/description")
    package_description = models.TextField(verbose_name="Упаковка")
    package_photo = models.ImageField("/product/package")
    payment = models.TextField(verbose_name="Оплата")
    payment_photo = models.ImageField("/product/payment")
    delivery = models.TextField(verbose_name="Доставка")
    delivery_photo = models.ImageField("/product/delivery")
