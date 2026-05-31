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
                "fields": [
                    "title_ru",
                    "title_uk",
                    "title_en",
                    "cost",
                    "discount",
                    "mass",
                    "energy_value",
                    "taste",
                    "package",
                    "shelf_life_ru",
                    "shelf_life_uk",
                    "shelf_life_en",
                ],
            },
        ),
        (
            "Описание продукта",
            {
                "classes": ["tab"],
                "fields": [
                    "description_ru",
                    "description_uk",
                    "description_en",
                    "description_photo",
                ],
            },
        ),
        (
            "Упаковка",
            {
                "classes": ["tab"],
                "fields": [
                    "package_description_ru",
                    "package_description_uk",
                    "package_description_en",
                    "package_photo",
                ],
            },
        ),
        (
            "Оплата",
            {
                "classes": ["tab"],
                "fields": [
                    "payment_ru",
                    "payment_uk",
                    "payment_en",
                    "payment_photo",
                ],
            },
        ),
        (
            "Доставка",
            {
                "classes": ["tab"],
                "fields": [
                    "delivery_ru",
                    "delivery_uk",
                    "delivery_en",
                    "delivery_photo",
                ],
            },
        ),
    ]
    exclude = ["gallery"]

    def save_formset(self, request, form, formset, change):
        if formset.model == ProductDetailPage.gallery.through:
            for inline_form in formset.forms:
                if inline_form.cleaned_data.get("image") and not inline_form.cleaned_data.get("DELETE"):
                    gallery = Gallery.objects.create(images=inline_form.cleaned_data["image"])
                    inline_form.instance.gallery = gallery
        super().save_formset(request, form, formset, change)
