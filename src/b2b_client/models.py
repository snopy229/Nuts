# Create your models here.
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from src.core.blocks import PhotoBlock, TabBlock


class B2BClientPage(Page):
    upper_banner = StreamField([("banner", PhotoBlock())], max_num=1)
    title = models.CharField(max_length=255)
    description = models.TextField()
    big_supermarket = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
    )
    shops = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
    )
    horecd = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
    )
    fitness_club = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
    )
    cake_baker = StreamField(
        [
            ("supermarket", TabBlock()),
        ],
        max_num=1,
    )
    down_banners = StreamField(
        [
            ("supermarket", PhotoBlock()),
        ],
        max_num=1,
    )
    max_count = 1
    template = "b2b_client.html"
    parent_page_types = ["wagtailcore.Page"]
    content_panels = Page.content_panels + [
        FieldPanel("upper_banner"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("big_supermarket"),
        FieldPanel("shops"),
        FieldPanel("horecd"),
        FieldPanel("fitness_club"),
        FieldPanel("cake_baker"),
        FieldPanel("down_banners"),
    ]
