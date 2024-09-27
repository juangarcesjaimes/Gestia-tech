# (11) throttling.py - Configuración de throttling para usuarios

from rest_framework.throttling import UserRateThrottle

class CustomUserThrottle(UserRateThrottle):
    """
    Clase de throttling personalizada para usuarios.
    
    Permite limitar la cantidad de solicitudes que un usuario puede hacer en un 
    período de tiempo definido para evitar abusos.
    """
    scope = 'user'

    def get_cache_key(self, request, view):
        """
        Obtiene la clave de caché para el throttling.
        
        Args:
            request: La solicitud HTTP que se está procesando.
            view: La vista a la que se está accediendo.

        Returns:
            str: La clave de caché para el usuario, o None si no se puede determinar.
        """
        if request.user.is_authenticated:
            return request.user.pk  # Usa el ID del usuario autenticado como clave de caché
        return None  # No se aplica throttling a usuarios no autenticados
