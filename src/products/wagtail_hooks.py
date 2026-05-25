from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from src.products.models import ProductTaste, ProductPackage


class ProductTasteViewSet(SnippetViewSet):
    model = ProductTaste
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Вкусы"
    menu_order = 300
    list_display = ["title"]
    search_fields = ["title"]


register_snippet(ProductTasteViewSet)


class ProductPackageViewSet(SnippetViewSet):
    model = ProductPackage
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Упаковка"
    menu_order = 300
    list_display = ["title"]
    search_fields = ["title"]


register_snippet(ProductPackageViewSet)
