from django.conf import settings
from django.shortcuts import render
from django.urls import include, path

from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from .api import api

urlpatterns = [
    path("crm/", admin.site.urls),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("user/", include("src.user.urls", namespace="user")),
    path("gallery/", include("src.gallery.urls", namespace="gallery")),
    path("products/", include("src.products.urls", namespace="products")),
    path("api/", api.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("checkouts/", include("src.checkouts.urls", namespace="checkouts")),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

# медиа отдаём всегда
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]


def custom_404(request, exception):
    return render(request, "404_page.html", status=404)


handler404 = custom_404
