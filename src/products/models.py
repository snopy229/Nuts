# Create your models here.
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from transliterate import translit

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
    title = models.CharField(verbose_name="Заголовок", max_length=255)
    slug = models.SlugField(verbose_name="Slug", max_length=255, unique=True, blank=True)
    cost = models.IntegerField(verbose_name="Цена")
    compound = models.TextField(verbose_name="Состав")
    nuts_type = models.CharField(verbose_name="Тип ореха", max_length=255)
    article = models.IntegerField(verbose_name="Артикул")
    discount = models.IntegerField(verbose_name="Скидка(грн)", blank=True, null=True)
    gallery = models.ManyToManyField("core.Gallery", verbose_name="gallery")
    mass = models.ForeignKey(ProductWeight, on_delete=models.CASCADE, verbose_name="Масса")
    energy_value = models.IntegerField(verbose_name="Энергетическая ценность")
    taste = models.ForeignKey(ProductTaste, on_delete=models.CASCADE, verbose_name="Вкус")
    package = models.ForeignKey(ProductPackage, on_delete=models.CASCADE, verbose_name="Упаковка")
    shelf_life = models.TextField(verbose_name="Срок годности")
    description = models.TextField(verbose_name="Описание")
    description_photo = models.ImageField(upload_to="product/description", verbose_name="Описание фото")
    package_description = models.TextField(verbose_name="Упаковка")
    package_photo = models.ImageField(upload_to="product/package", verbose_name="Упаковка фото")
    payment = models.TextField(verbose_name="Оплата")
    payment_photo = models.ImageField(upload_to="product/payment", verbose_name="Оплата фото")
    delivery = models.TextField(verbose_name="Доставка")
    delivery_photo = models.ImageField(upload_to="product/delivery", verbose_name="Доставка фото")
    created_at = models.DateField(
        auto_now_add=True,
    )

    def _transliterate(self, text):
        try:
            return translit(text, reversed=True)
        except Exception:
            return text

    def generate_slug(self):
        base = self.title_uk or self.title_ru or self.title_en or self.title
        slug = slugify(self._transliterate(base))
        if not slug:
            slug = "product"
        original = slug
        count = 1
        qs = ProductDetailPage.objects.all()
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        while qs.filter(slug=slug).exists():
            slug = f"{original}-{count}"
            count += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    @property
    def cost_with_discount(self):
        if self.discount:
            return self.cost - self.discount
        return self.cost

    @property
    def is_new(self):
        if not self.created_at:
            return False

        current_date = timezone.now().date()
        seven_days_ago = current_date - timedelta(days=7)

        object_date = getattr(self.created_at, "date", lambda: self.created_at)()

        return object_date >= seven_days_ago
