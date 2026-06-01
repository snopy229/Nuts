from cities_light.models import City, Country, Region
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.fields import StreamField

from src.core.blocks import PhotoBlock


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    fullname = models.CharField(max_length=255, verbose_name="ФИО")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Номер телефона")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Страна")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Регион")
    city = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Город")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес")
    avatar = models.FileField(upload_to="avatars", blank=True, null=True, verbose_name="Аватар")
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def __str__(self):
        return self.email


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


@register_setting
class UserAccountSettings(BaseSiteSetting):
    manager_name = models.CharField(max_length=255, verbose_name="Имя менеджера")
    manager_phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Номер телефона менеджера")
    banner = StreamField(
        [("banner", PhotoBlock(label="Баннер"))],
        max_num=1,
        min_num=1,
        use_json_field=True,
        verbose_name="Баннер",
    )

    panels = [
        FieldPanel("manager_name"),
        FieldPanel("manager_phone_number"),
        FieldPanel("banner"),
    ]

    class Meta:
        verbose_name = "Настройки сайта"
