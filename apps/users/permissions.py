# (9) permissions.py - Lógica de permisos y roles personalizados

from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permiso personalizado que permite el acceso solo a usuarios administradores.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsAccountOwner(permissions.BasePermission):
    """
    Permiso personalizado que permite el acceso solo al propietario de la cuenta.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsStaffUser(permissions.BasePermission):
    """
    Permiso que permite el acceso solo a usuarios que son parte del personal.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class HasRole(permissions.BasePermission):
    """
    Permiso que permite el acceso basado en el rol del usuario.
    """
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role in self.allowed_roles
        return False

class IsActiveUser(permissions.BasePermission):
    """
    Permiso que permite el acceso solo a usuarios activos.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_active
