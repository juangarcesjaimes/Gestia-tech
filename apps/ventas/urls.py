from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from .views import ClienteViewSet, ProductoViewSet, CotizacionViewSet, VentaViewSet, FacturaViewSet, CategoriaViewSet, ProveedorViewSet

# Crear un enrutador y registrar nuestros viewsets con él
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'cotizaciones', CotizacionViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'proveedores', ProveedorViewSet)

# Las URL de la API ahora están determinadas automáticamente por el enrutador.
urlpatterns = [
    path('api/v1/', include(router.urls) ),
    path('docs/', include_docs_urls(title='cliente API'))
]
