# (22) celery.py - Configuración de Celery para tareas asíncronas

import os
from celery import Celery

# Establece el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')

# Crea una instancia de Celery
app = Celery('Backend')

# Carga la configuración de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre y carga automáticamente tareas de todos los módulos
app.autodiscover_tasks()

# (Opcional) Define una tarea de prueba
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
