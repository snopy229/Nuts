# Create your models here.
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from src.core.blocks import VideoBlock, PhotoBlock


class GalleryPage(Page):
    banner = StreamField([("banner", VideoBlock())], max_num=1, blank=True)

    parent_page_types = ["wagtailcore.Page"]
    max_count = 1
    template = "gallery_page.html"
    content_panels = Page.content_panels + [
        FieldPanel("banner"),
    ]


class Gallery(models.Model):
    content = StreamField(
        [
            ("image", PhotoBlock()),
            ("video", VideoBlock()),
        ],
        use_json_field=True,
    )
    panels = [
        FieldPanel("content"),
    ]

    def __str__(self):
        return "Галерея"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name = "Галерея"


class GalleryViewSet(SnippetViewSet):
    model = Gallery
    menu_label = "Галерея"
    icon = "image"
    add_to_admin_menu = True

    def index_view(self):
        gallery = Gallery.get()
        url = reverse(f"{self.url_namespace}:edit", args=[gallery.pk])
        return redirect(url)


register_snippet(Gallery, viewset=GalleryViewSet)
