# Register your models here.
from unfold.sites import UnfoldAdminSite


class SuperCleanAdminSite(UnfoldAdminSite):
    def has_module_permission(self, request, app_label):
        BANNED_APPS = [
            "cities_light",
            "wagtailmedia",
            "wagtaildocs",
            "wagtailimages",
            "wagtailcore",
            "taggit",
        ]

        if app_label in BANNED_APPS:
            return False

        return super().has_module_permission(request, app_label)
