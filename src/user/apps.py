from django.apps import AppConfig
from django.contrib import admin
from .admin import SuperCleanAdminSite


class UserConfig(AppConfig):
    name = "src.user"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        cleaned_site = SuperCleanAdminSite()
        admin.site = cleaned_site
        admin.sites.site = cleaned_site
