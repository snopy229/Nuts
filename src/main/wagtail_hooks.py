from typing import List

from django.http import HttpRequest
from django.urls import reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem


@hooks.register("register_admin_menu_item")
def register_contacts_menu_item() -> MenuItem:
    return MenuItem("Контакты", reverse("wagtailsettings:edit", args=("main", "contacts")), icon_name="mail", order=600)


# @hooks.register("construct_main_menu")
# def hide_settings_menu_item(request: HttpRequest, menu_items: List[MenuItem]) -> None:
#     menu_items[:] = [item for item in menu_items if item.name != "settings"]


@hooks.register("construct_main_menu")
def hide_reports_menu_item(request: HttpRequest, menu_items: List[MenuItem]) -> None:
    menu_items[:] = [item for item in menu_items if item.name != "reports"]


@hooks.register("construct_main_menu")
def hide_help_menu_item(request: HttpRequest, menu_items: List[MenuItem]) -> None:
    menu_items[:] = [item for item in menu_items if item.name != "help"]


@hooks.register("construct_main_menu")
def hide_images_menu_item(request: HttpRequest, menu_items: List[MenuItem]) -> None:
    menu_items[:] = [item for item in menu_items if item.name != "images"]


@hooks.register("construct_main_menu")
def hide_documents_menu_item(request: HttpRequest, menu_items: List[MenuItem]) -> None:
    menu_items[:] = [item for item in menu_items if item.name != "documents"]
