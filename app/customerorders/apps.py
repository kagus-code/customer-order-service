from django.apps import AppConfig


class CustomerordersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.customerorders"

    def ready(self):
        import app.customerorders.signals  # noqa
