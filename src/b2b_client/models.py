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
    )
    page_title = models.CharField(max_length=255)
    description = StreamField(
        [
            ("two_columns", TwoColumnsBlock()),
        ],
        max_num=1,
        use_json_field=True,
    )
    big_supermarket = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
        use_json_field=True,
    )
    shops = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
        use_json_field=True,
    )
    horecd = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
        use_json_field=True,
    )
    fitness_club = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
        use_json_field=True,
    )
    cake_baker = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
        use_json_field=True,
    )
    down_banner = StreamField(
        [
            ("supermarket", PhotoBlock()),
        ],
        max_num=1,
        use_json_field=True,
    )
    max_count = 1
    template = "b2b_client_page.html"
    parent_page_types = ["wagtailcore.Page"]
    content_panels = Page.content_panels + [
        FieldPanel("upper_banner", heading="Верхний баннер"),
        FieldPanel("page_title", heading="Название страницы"),
        FieldPanel("description", heading="Описание"),
        FieldPanel("big_supermarket", heading="Крупные супермаркеты"),
        FieldPanel("shops", heading="Магазины"),
        FieldPanel("horecd", heading="HoReCa"),
        FieldPanel("fitness_club", heading="Фитнес клубы"),
        FieldPanel("cake_baker", heading="Пекарни и кондитерские"),
        FieldPanel("down_banner", heading="Нижние баннеры"),
    ]
