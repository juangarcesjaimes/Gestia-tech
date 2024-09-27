# serializers.py - Serializadores para usuarios, perfiles y roles

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Profile, Role, Permission, UserActivityLog, AuditLog

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializador personalizado para obtener el par de tokens JWT.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'user': self.user.username})
        return data

class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo User. Usado para crear y actualizar usuarios.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'roles', 'profile_image']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'profile_image': {'required': False}
        }

class UserListSerializer(serializers.ModelSerializer):
    """
    Serializador para listar usuarios. Incluye campos relevantes para la vista de lista.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'date_joined']

class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Serializador para actualizar detalles del usuario.
    """
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'roles', 'profile_image']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'roles': {'required': False},
            'profile_image': {'required': False}
        }

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Profile. Usado para crear y actualizar perfiles de usuario.
    """
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'birth_date', 'location']
        read_only_fields = ['user']

class RoleSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Role. Usado para crear y actualizar roles.
    """
    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions']

class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Permission. Usado para crear y actualizar permisos.
    """
    class Meta:
        model = Permission
        fields = ['id', 'name']

class UserActivityLogSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo UserActivityLog. Usado para listar actividades de usuario.
    """
    class Meta:
        model = UserActivityLog
        fields = ['id', 'user', 'action', 'timestamp']
        read_only_fields = ['timestamp']

class AuditLogSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo AuditLog. Usado para listar registros de auditoría.
    """
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'change', 'timestamp']
        read_only_fields = ['timestamp']
