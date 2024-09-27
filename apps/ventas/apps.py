from django.apps import AppConfig


class VentasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ventas'
    verbose_name = 'Gestión de Ventas'


    def ready(self):
        import apps.ventas.signals # Importar señales para manejar eventos específicos

