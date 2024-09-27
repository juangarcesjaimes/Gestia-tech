from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Permiso personalizado para permitir solo a los administradores editar objetos.
    Los usuarios autenticados pueden leer.
    """

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff

class IsOwnerOrReadOnly(BasePermission):
    """
    Permiso personalizado para permitir solo a los propietarios de un objeto editarlo.
    Los usuarios autenticados pueden leer.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.creado_por == request.user
