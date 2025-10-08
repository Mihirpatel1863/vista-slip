from django.apps import AppConfig

class SocietyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'society'

    def ready(self):
        try:
            import society.signals  # noqa
        except Exception:
            pass
