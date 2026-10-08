from django.apps import AppConfig

class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LIBRARY'
    verbose_name = 'Diverse Mind Library'

    def ready(self):
        from . import signals  # noqa: F401
