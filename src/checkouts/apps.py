from django.apps import AppConfig


class CheckoutsConfig(AppConfig):
    name = "src.checkouts"

    def ready(self):
        import src.checkouts.signals  # noqa: F401
