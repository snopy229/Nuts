from typing import Any

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import CharBlock
from wagtail.contrib.settings.models import BaseGenericSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.fields import StreamField
from wagtailgeowidget.helpers import geosgeometry_str_to_struct
from wagtailgeowidget.panels import LeafletPanel


@register_setting
class Contacts(BaseGenericSetting):
    phone_number = StreamField(
        [
            ("phone_number", CharBlock(max_length=20)),
        ],
        blank=True,
        use_json_field=True,
    )
    viber_url = models.URLField(blank=True)
    telegram_url = models.URLField(blank=True)
    whatsapp_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    office_address = models.CharField(max_length=255, blank=True)
    production_address = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=250, blank=True)
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
