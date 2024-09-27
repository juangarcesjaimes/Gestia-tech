# (10) authentication.py - Lógica de autenticación y expiración de tokens

from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Clase de autenticación que gestiona la expiración de tokens.
    """

    def expires_in(self, token):
        """
        Calcula el tiempo restante hasta que el token expire.

        Args:
            token: El token para el que se quiere calcular el tiempo restante.

        Returns:
            timedelta: Tiempo restante hasta la expiración del token.
        """
        time_elapsed = timezone.now() - token.created  # Calcula el tiempo transcurrido desde la creación del token
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed  # Tiempo restante
        return left_time

    def is_token_expired(self, token):
        """
        Verifica si el token ha expirado.

        Args:
            token: El token que se quiere verificar.

        Returns:
            bool: True si el token ha expirado, False en caso contrario.
        """
        return self.expires_in(token) < timedelta(seconds=0)  # Devuelve True si el tiempo restante es negativo

    def token_expire_handler(self, token):
        """
        Maneja la expiración del token, creando uno nuevo si es necesario.

        Args:
            token: El token que se quiere manejar.

        Returns:
            token: El token activo, ya sea el existente o uno nuevo si el anterior ha expirado.
        """
        if self.is_token_expired(token):  # Verifica si el token ha expirado
            user = token.user  # Obtiene el usuario asociado al token
            token.delete()  # Elimina el token expirado
            token = self.get_model().objects.create(user=user)  # Crea un nuevo token para el usuario
        return token  # Retorna el token activo

    def authenticate_credentials(self, key):
        """
        Autentica las credenciales del token y maneja la expiración.

        Args:
            key: La clave del token a autenticar.

        Returns:
            tuple: Usuario y token autenticados.

        Raises:
            AuthenticationFailed: Si el token es inválido o ha expirado.
        """
        try:
            token = self.get_model().objects.select_related('user').get(key=key)  # Busca el token por su clave
            token = self.token_expire_handler(token)  # Maneja la expiración del token
            user = token.user  # Obtiene el usuario asociado al token
            if not user.is_active:  # Verifica si el usuario está activo
                raise AuthenticationFailed('Usuario inactivo o eliminado.')
            return (user, token)  # Retorna el usuario y el token

        except self.get_model().DoesNotExist:
            raise AuthenticationFailed('Token inválido o expirado.')  # Lanza error si el token no existe

    def authenticate(self, request):
        """
        Método sobreescrito para agregar lógica adicional de autenticación.

        Args:
            request: La solicitud HTTP que se está procesando.

        Returns:
            tuple: Usuario y token autenticados o None si no hay autenticación.
        """
        auth = super().authenticate(request)  # Llama al método de autenticación base
        if not auth:
            return None  # Retorna None si no hay autenticación
        user, token = auth  # Desempaqueta el usuario y el token

        # Si deseas añadir lógica adicional, como la verificación de roles o permisos, hazlo aquí.

        return user, token  # Retorna el usuario y el token
