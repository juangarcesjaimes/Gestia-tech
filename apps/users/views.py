# views.py - Vistas para gestionar usuarios, roles, login, logout, etc.

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Role, UserActivityLog
from .serializers import (
    UserSerializer,
    UserListSerializer,
    UpdateUserSerializer,
    CustomTokenObtainPairSerializer,
    RoleSerializer,
    UserActivityLogSerializer
)
from .permissions import IsAdminUser, IsAccountOwner

class UserViewSet(viewsets.GenericViewSet):
    """
    Vista para gestionar las operaciones relacionadas con usuarios.
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Listar todos los usuarios activos.
        """
        users = self.get_queryset()
        serializer = self.list_serializer_class(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Crear un nuevo usuario.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario creado correctamente.'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Errores en la creación del usuario.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Obtener detalles de un usuario específico.
        """
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Actualizar un usuario específico.
        """
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario actualizado correctamente.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Errores en la actualización del usuario.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Desactivar un usuario específico.
        """
        user = get_object_or_404(self.queryset, pk=pk)
        user.is_active = False
        user.save()
        return Response({'message': 'Usuario desactivado correctamente.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], permission_classes=[IsAccountOwner])
    def set_password(self, request, pk=None):
        """
        Cambiar la contraseña de un usuario específico.
        """
        user = get_object_or_404(self.queryset, pk=pk)
        password = request.data.get('password')
        if password:
            user.set_password(password)
            user.save()
            return Response({'message': 'Contraseña actualizada correctamente.'})
        return Response({'message': 'Contraseña no proporcionada.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    """
    Vista personalizada para el inicio de sesión.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Iniciar sesión y obtener tokens de acceso y renovación.
        """
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    """
    Vista para cerrar sesión.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Cerrar sesión del usuario.
        """
        request.user.auth_token.delete()  # Elimina el token de autenticación
        return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_205_RESET_CONTENT)


class RoleViewSet(viewsets.ModelViewSet):
    """
    Vista para gestionar roles de usuario.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]

    def create(self, request):
        """
        Crear un nuevo rol.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Rol creado correctamente.'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Errores en la creación del rol.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        Listar todos los roles.
        """
        roles = self.queryset
        serializer = self.serializer_class(roles, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Actualizar un rol específico.
        """
        role = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Rol actualizado correctamente.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Errores en la actualización del rol.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Eliminar un rol específico.
        """
        role = get_object_or_404(self.queryset, pk=pk)
        role.delete()
        return Response({'message': 'Rol eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)


class UserActivityLogViewSet(viewsets.ModelViewSet):
    """
    Vista para gestionar el registro de actividades de usuario.
    """
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtrar los logs de actividades por el usuario autenticado.
        """
        return self.queryset.filter(user=self.request.user)
