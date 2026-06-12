from django.urls import reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem


@hooks.register("register_admin_menu_item")
def register_user_account_menu_item() -> MenuItem:
    return MenuItem(
        "Настроки аккаунтов",
        reverse("wagtailsettings:edit", args=("user", "useraccountsettings")),
        icon_name="mail",
        order=600,
    )


@hooks.register("register_admin_menu_item")
def register_page_404() -> MenuItem:
    return MenuItem(
        "Страница не найдена",
        reverse("wagtailsettings:edit", args=("core", "page404settings")),
        icon_name="mail",
        order=600,
    )
