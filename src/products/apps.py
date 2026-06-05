from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = "src.products"

    def ready(self):
        import src.products.signals  # noqa: F401
