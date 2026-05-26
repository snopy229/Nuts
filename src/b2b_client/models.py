# Create your models here.
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from src.core.blocks import PhotoBlock, TabBlock, TwoColumnsBlock


class B2BClientPage(Page):
    upper_banner = StreamField(
        [("banner", PhotoBlock())],
        max_num=1,
        use_json_field=True,
        verbose_name="Верхний баннер",
    )
    page_title = models.CharField(max_length=255, verbose_name="Название страницы")
    description = StreamField(
        [
            ("two_columns", TwoColumnsBlock()),
        ],
        max_num=1,
        use_json_field=True,
        verbose_name="Описание",
    )
    big_supermarket = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
        use_json_field=True,
        verbose_name="Крупные супермаркеты",
    )
    shops = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
        use_json_field=True,
        verbose_name="Магазины",
    )
    horecd = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
        use_json_field=True,
        verbose_name="HoReCa",
    )
    fitness_club = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
        use_json_field=True,
        verbose_name="Фитнес клубы",
    )
    cake_baker = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
        use_json_field=True,
        verbose_name="Пекарни и кондитерские",
    )
    down_banner = StreamField(
        [
            ("supermarket", PhotoBlock()),
        ],
        max_num=1,
        use_json_field=True,
        verbose_name="Нижние баннеры",
    )
    max_count = 1
    template = "b2b_client_page.html"
    parent_page_types = ["wagtailcore.Page"]
    content_panels = Page.content_panels + [
        FieldPanel("upper_banner"),
        FieldPanel("page_title"),
        FieldPanel("description"),
        FieldPanel("big_supermarket"),
        FieldPanel("shops"),
        FieldPanel("horecd"),
        FieldPanel("fitness_club"),
        FieldPanel("cake_baker"),
        FieldPanel("down_banner"),
    ]
