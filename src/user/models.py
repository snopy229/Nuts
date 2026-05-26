from cities_light.models import City, Country, Region
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class User(AbstractUser):
    fullname = models.CharField(max_length=255, verbose_name="ФИО")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Номер телефона")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Страна")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Регион")
    city = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Город")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес")
    avatar = models.FileField(upload_to="avatars", blank=True, null=True, verbose_name="Аватар")
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = ["username"]


class Individual(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    is_sole_proprietor = models.BooleanField(verbose_name="Является ФОП")

    class Meta:
        verbose_name = "Физическое лицо"
        verbose_name_plural = "Физические лица"


class LegalEntity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    edrpou = models.CharField(max_length=8, blank=True, null=True, verbose_name="ЕДРПОУ")
    legal_country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="legal_country",
        verbose_name="Юр. страна",
    )
    legal_region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="legal_region",
        verbose_name="Юр. регион",
    )
    legal_city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="legal_city",
        verbose_name="Юр. город",
    )
    legal_address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Юр. адрес")
    postal_card = models.CharField(max_length=5, blank=True, verbose_name="Почтовый индекс")
    reg_number = models.CharField(max_length=8, blank=True, null=True, verbose_name="Рег. номер")
    sp_country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="sp_country",
        verbose_name="Страна (СП)",
    )
    sp_region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="sp_region",
        verbose_name="Регион (СП)",
    )
    sp_city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="sp_city",
        null=True,
        blank=True,
        verbose_name="Город (СП)",
    )
    sp_address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес (СП)")

    class Meta:
        verbose_name = "Юридическое лицо"
        verbose_name_plural = "Юридические лица"


class TermsPage(Page):
    content = RichTextField(verbose_name="Условия")
    page_title = models.CharField(max_length=255, verbose_name="Соглашение")
    content_panels = Page.content_panels + [
        FieldPanel("page_title"),
        FieldPanel("content"),
    ]

    template = "terms-of-use.html"
    max_count = 1
    min_count = 1
    parent_page_types = ["wagtailcore.Page"]
