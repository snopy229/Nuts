from django.contrib.admin import AdminSite


class MyAdminSite(AdminSite):
    site_header = "Администрирование"

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)

        hidden_apps = {
            "cities_light",
            "wagtailmedia",
            "wagtaildocs",
            "wagtailimages",
            "taggit",
            "auth",
        }

        return [app for app in app_list if app["app_label"] not in hidden_apps]


admin_site = MyAdminSite(name="admin")
