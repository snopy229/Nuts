# Create your models here.
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


class NewsAndArticlesPage(Page):
    page_title = models.CharField()
    description = models.TextField()

    content_panels = Page.content_panels + [
        FieldPanel("page_title", heading="Верхний баннер"),
        FieldPanel("description", heading="Оплата"),
    ]
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    template = "news_and_articles.html"
