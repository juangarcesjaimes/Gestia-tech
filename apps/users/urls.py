# (8) urls.py - Rutas de la API para usuarios

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet, LoginView, LogoutView, UserActivityLogViewSet


# Crear un enrutador para manejar las rutas automáticamente
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'activity-logs', UserActivityLogViewSet, basename='activity-log')

urlpatterns = [
    # Incluir las rutas registradas en el enrutador
    path('', include(router.urls)),
    # Ruta para iniciar sesión
    path('login/', LoginView.as_view(), name='login'),
    # Ruta para cerrar sesión
    path('logout/', LogoutView.as_view(), name='logout'),
]
