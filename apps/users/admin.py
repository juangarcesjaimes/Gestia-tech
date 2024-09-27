# (3) admin.py - Configuración del modelo para el panel de administración

from django.contrib import admin
from .models import User, Profile, Role, Permission, UserActivityLog, AuditLog

# Admin para el modelo User
class UserAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo User.
    Permite gestionar usuarios desde la interfaz de administración.
    """
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')  # Campos a mostrar en la lista
    search_fields = ('email', 'username', 'first_name', 'last_name')  # Campos para buscar
    list_filter = ('is_active', 'is_staff', 'roles')  # Filtros disponibles
    ordering = ('date_joined',)  # Ordenar por fecha de registro

# Admin para el modelo Profile
class ProfileAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Profile.
    Permite gestionar perfiles de usuario desde la interfaz de administración.
    """
    list_display = ('user', 'bio', 'birth_date', 'location')  # Campos a mostrar en la lista
    search_fields = ('user__email', 'user__username')  # Campos para buscar

# Admin para el modelo Role
class RoleAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Role.
    Permite gestionar roles desde la interfaz de administración.
    """
    list_display = ('name',)  # Campos a mostrar en la lista
    search_fields = ('name',)  # Campos para buscar

# Admin para el modelo Permission
class PermissionAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Permission.
    Permite gestionar permisos desde la interfaz de administración.
    """
    list_display = ('name',)  # Campos a mostrar en la lista
    search_fields = ('name',)  # Campos para buscar

# Admin para el modelo UserActivityLog
class UserActivityLogAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo UserActivityLog.
    Permite gestionar registros de actividad de usuarios desde la interfaz de administración.
    """
    list_display = ('user', 'action', 'timestamp')  # Campos a mostrar en la lista
    search_fields = ('user__email', 'action')  # Campos para buscar
    list_filter = ('action', 'timestamp')  # Filtros disponibles

# Admin para el modelo AuditLog
class AuditLogAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo AuditLog.
    Permite gestionar registros de auditoría desde la interfaz de administración.
    """
    list_display = ('user', 'change', 'timestamp')  # Campos a mostrar en la lista
    search_fields = ('user__email', 'change')  # Campos para buscar
    list_filter = ('timestamp',)  # Filtros disponibles

# Registra los modelos y sus respectivos administradores
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(UserActivityLog, UserActivityLogAdmin)
admin.site.register(AuditLog, AuditLogAdmin)
