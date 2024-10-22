from django.apps import AppConfig


class MaterialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.material'
    verbose_name = '3. Материалы'


    def ready(self):
        import apps.material.signals