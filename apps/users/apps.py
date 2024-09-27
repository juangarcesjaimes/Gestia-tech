from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Define el tipo de campo automático por defecto
    name = 'apps.users'  # Nombre de la aplicación
    verbose_name = 'Gestión de Usuarios'  # Nombre legible para la aplicación en el panel de administración

    def ready(self):
        # Aquí se pueden registrar señales u otras inicializaciones necesarias
        import apps.users.signals  # Importa el módulo de señales para que se registren


