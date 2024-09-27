# (16) utils.py - Utilidades auxiliares como helpers o funciones comunes

import re
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta

def is_valid_email(email):
    """
    Valida si el email proporcionado tiene un formato correcto.
    
    :param email: El email a validar.
    :return: True si el email es válido, False en caso contrario.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def cache_results(key, function, *args, timeout=300):
    """
    Almacena los resultados de una función en la caché para mejorar el rendimiento.
    
    :param key: Clave única para almacenar los resultados en la caché.
    :param function: La función a ejecutar y almacenar en caché.
    :param args: Argumentos para la función.
    :param timeout: Tiempo de expiración para la caché en segundos (por defecto 300s).
    :return: El resultado de la función.
    """
    results = cache.get(key)
    if results is None:
        results = function(*args)
        cache.set(key, results, timeout)
    return results

def get_time_difference(start_time, end_time):
    """
    Calcula la diferencia de tiempo entre dos objetos datetime.
    
    :param start_time: El tiempo de inicio.
    :param end_time: El tiempo de finalización.
    :return: La diferencia de tiempo en un formato legible.
    """
    diff = end_time - start_time
    return {
        'days': diff.days,
        'seconds': diff.seconds,
        'total_seconds': diff.total_seconds()
    }

def is_token_expired(token_creation_time, expiry_duration=60):
    """
    Verifica si un token ha expirado basado en su tiempo de creación y duración de expiración.
    
    :param token_creation_time: Tiempo de creación del token.
    :param expiry_duration: Duración de expiración en minutos (por defecto 60 minutos).
    :return: True si el token ha expirado, False en caso contrario.
    """
    expiration_time = token_creation_time + timedelta(minutes=expiry_duration)
    return timezone.now() > expiration_time

def generate_random_string(length=8):
    """
    Genera una cadena aleatoria de un tamaño específico.
    
    :param length: Longitud de la cadena generada.
    :return: Cadena aleatoria.
    """
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
