from typing import Any

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import CharBlock
from wagtail.contrib.settings.models import BaseGenericSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtailgeowidget.helpers import geosgeometry_str_to_struct
from wagtailgeowidget.panels import LeafletPanel

from src.production.models import ProductionPage
from src.news_and_articles.models import NewsAndArticlesDetailPage
from src.products.models import ProductDetailPage, ProductsPage
from src.core.blocks import VideoBlock, VideoWithoutDescriptionBlock, TabBlock


@register_setting
class Contacts(BaseGenericSetting):
    phone_number = StreamField(
        [
            ("phone_number", CharBlock(max_length=20, label="Номер")),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Номера телефонов",
    )
    viber_url = models.URLField(blank=True, verbose_name="Viber")
    telegram_url = models.URLField(blank=True, verbose_name="Telegram")
    whatsapp_url = models.URLField(blank=True, verbose_name="WhatsApp")
    facebook_url = models.URLField(blank=True, verbose_name="Facebook")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube")
    office_address = models.CharField(max_length=255, blank=True, verbose_name="Адрес офиса")
    production_address = models.CharField(max_length=255, blank=True, verbose_name="Адрес производства")
    location = models.CharField(max_length=250, blank=True, verbose_name="Местоположение")
    panels = [
        FieldPanel("phone_number"),
        FieldPanel("viber_url"),
        FieldPanel("telegram_url"),
        FieldPanel("whatsapp_url"),
        FieldPanel("facebook_url"),
        FieldPanel("instagram_url"),
        FieldPanel("youtube_url"),
        FieldPanel("office_address"),
        FieldPanel("production_address"),
        LeafletPanel("location"),
    ]

    @property
    def point(self) -> Any:
        return geosgeometry_str_to_struct(self.location)

    @property
    def lat(self) -> Any:
        return self.point["y"]

    @property
    def lng(self) -> Any:
        return self.point["x"]

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"


class MainPage(Page):
    upper_banner = StreamField(
        [
            ("banner", VideoBlock(label="Видео блок")),
        ],
        max_num=1,
        min_num=1,
        blank=True,
        verbose_name="Верхний баннер",
    )
    products_title = models.CharField(max_length=20, verbose_name="Названия блока с продукцией")
    products_description = models.TextField(verbose_name="Описание блока продукции")
    middle_banner = StreamField(
        [("banner", VideoWithoutDescriptionBlock(label="Видео блок"))],
        max_num=1,
        min_num=1,
        blank=True,
        verbose_name="Баннер посередине",
    )
    benefits_title = models.CharField(max_length=30, verbose_name="Название блока с пользой")
    benefits_description = models.TextField(verbose_name="Описание блока с пользой")
    walnut = StreamField(
        [
            ("card", TabBlock(label="Карточка")),
        ],
        max_num=1,
        min_num=1,
        blank=True,
        verbose_name="Карточка грецкого ореха",
    )
    hazelnut = StreamField(
        [
            ("card", TabBlock(label="Карточка")),
        ],
        max_num=1,
        min_num=1,
        blank=True,
        verbose_name="Карточка лесного ореха",
    )
    rose_hip = StreamField(
        [
            ("card", TabBlock(label="Карточка")),
        ],
        max_num=1,
        min_num=1,
        blank=True,
        verbose_name="Карточка шиповника",
    )
    down_banner = StreamField(
        [
            ("banner", VideoBlock(label="Блок")),
        ],
        max_num=1,
        min_num=1,
        blank=True,
        verbose_name="Нижний баннер",
    )

    template = "main_page.html"
    parent_page_types = ["wagtailcore.Page"]
    max_count = 1
    content_panels = Page.content_panels + [
        FieldPanel("upper_banner"),
        FieldPanel("products_title"),
        FieldPanel("products_description"),
        FieldPanel("middle_banner"),
        FieldPanel("benefits_title"),
        FieldPanel("benefits_description"),
        FieldPanel("walnut"),
        FieldPanel("hazelnut"),
        FieldPanel("rose_hip"),
        FieldPanel("down_banner"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        products = ProductDetailPage.objects.live()
        context["products"] = products[:6]
        context["product_page"] = ProductsPage.objects.live().first()
        news = NewsAndArticlesDetailPage.objects.live()
        context["news"] = news[:6]
        context["news_page"] = NewsAndArticlesDetailPage.objects.live().first()
        context["production"] = ProductionPage.objects.live().first()
        return context
