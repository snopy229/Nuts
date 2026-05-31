# Register your models here.
from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget

from src.core.models import Gallery
from .forms import GalleryInlineForm
from src.products.models import ProductPackage, ProductWeight, ProductTaste, ProductDetailPage


@admin.register(ProductPackage)
class ProductPackageAdmin(ModelAdmin):
    list_display = ("title",)
    list_display_links = ["title"]
    search_fields = ("title",)


@admin.register(ProductWeight)
class ProductWeightAdmin(ModelAdmin):
    list_display = ("title",)
    list_display_links = ["title"]
    search_fields = ("title",)


@admin.register(ProductTaste)
class ProductTasteAdmin(ModelAdmin):
    list_display = ("title",)
    list_display_links = ["title"]
    search_fields = ("title",)


class GalleryInline(TabularInline):
    model = ProductDetailPage.gallery.through
    form = GalleryInlineForm
    extra = 1
    fields = ["image"]
    verbose_name = "Фото"
    verbose_name_plural = "Галерея"

    def save_new_objects(self, formset, commit=True):
        saved = super().save_new_objects(formset, commit)
        for form in formset.extra_forms:
            if form.cleaned_data.get("image"):
                gallery = Gallery.objects.create(images=form.cleaned_data["image"])
                form.instance.gallery = gallery
        return saved


@admin.register(ProductDetailPage)
class ProductDetailPageAdmin(ModelAdmin):
    inlines = [GalleryInline]
    list_display = ("title", "taste", "package", "mass")
    list_filter = ["taste", "package", "mass"]
    search_fields = ("title",)

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    tabs = True

    fieldsets = [
        (
            "Основная информация",
            {
                "classes": ["tab"],
                "fields": ["title", "cost", "discount", "mass", "energy_value", "taste", "package", "shelf_life"],
            },
        ),
        ("Описание продукта", {"classes": ["tab"], "fields": ["description", "description_photo"]}),
        ("Упаковка", {"classes": ["tab"], "fields": ["package_description", "package_photo"]}),
        ("Оплата", {"classes": ["tab"], "fields": ["payment", "payment_photo"]}),
        ("Доставка", {"classes": ["tab"], "fields": ["delivery", "delivery_photo"]}),
    ]
    exclude = ["gallery"]
