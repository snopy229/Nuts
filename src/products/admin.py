# Register your models here.
from django.contrib import admin

from src.products.models import ProductPackage, ProductWeight, ProductTaste


@admin.register(ProductPackage)
class ProductPackageAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_display_links = ["title"]
    search_fields = ("title",)


@admin.register(ProductWeight)
class ProductWeightAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_display_links = ["title"]
    search_fields = ("title",)


@admin.register(ProductTaste)
class ProductTasteAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_display_links = ["title"]
    search_fields = ("title",)
