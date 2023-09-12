from django.apps import AppConfig


class DismsgConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "disMsg"

    def ready(self):
        from .cron import main
        main()