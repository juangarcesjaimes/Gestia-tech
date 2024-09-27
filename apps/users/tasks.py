# (14) tasks.py - Tareas automáticas o programadas (ejemplo: limpieza de tokens)

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token

@shared_task
def cleanup_expired_tokens():
    """
    Tarea programada que se encarga de eliminar los tokens expirados.
    Los tokens que no han sido utilizados en las últimas 24 horas se consideran expirados.

    Esta tarea se puede programar para ejecutarse periódicamente utilizando
    Celery Beat.
    """
    expiration_time = timezone.now() - timedelta(days=1)  # Define la duración de 24 horas
    expired_tokens = Token.objects.filter(created__lt=expiration_time)  # Filtra los tokens expirados
    count = expired_tokens.count()  # Cuenta los tokens expirados

    expired_tokens.delete()  # Elimina los tokens expirados

    return f"{count} expired tokens removed."  # Retorna un mensaje de registro
