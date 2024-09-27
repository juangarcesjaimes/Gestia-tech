# (13) signals.py - Señales para automatizar la creación de perfiles u otras acciones

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Señal que se activa después de que se crea un nuevo usuario.
    Crea un perfil asociado al nuevo usuario.

    Args:
        sender: El modelo que envía la señal.
        instance: La instancia del modelo que se acaba de guardar.
        created: Booleano que indica si se creó una nueva instancia.
        **kwargs: Argumentos adicionales.
    """
    if created:
        # Crea un perfil vacío asociado al nuevo usuario
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Señal que se activa después de que se guarda un usuario.
    Guarda el perfil asociado al usuario.

    Args:
        sender: El modelo que envía la señal.
        instance: La instancia del modelo que se acaba de guardar.
        **kwargs: Argumentos adicionales.
    """
    instance.profile.save()  # Guarda el perfil asociado al usuario
