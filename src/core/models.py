from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from wagtail.fields import StreamField
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from src.core.blocks import GardenInfoBlock


class GardenInfo(models.Model):
    tab_1 = StreamField(
        [("block", GardenInfoBlock())],
        use_json_field=True,
        max_num=1,
    )
    tab_2 = StreamField(
        [("block", GardenInfoBlock())],
        use_json_field=True,
        max_num=1,
    )
    tab_3 = StreamField(
        [("block", GardenInfoBlock())],
        use_json_field=True,
        max_num=1,
    )
    tab_4 = StreamField(
        [("block", GardenInfoBlock())],
        use_json_field=True,
        max_num=1,
    )

    def __str__(self):
        return "Информация о саде"

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
        verbose_name = "Информация о саде"


class GardenInfoViewSet(SnippetViewSet):
    model = GardenInfo
    menu_label = "Информация о саде"
    icon = "image"
    add_to_admin_menu = True

    def index_view(self, request):
        gallery = GardenInfo.get()
        url = reverse(f"{self.url_namespace}:edit", args=[gallery.pk])
        return redirect(url)


register_snippet(GardenInfo, viewset=GardenInfoViewSet)
