from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from apps.ventas import views

# version de api
routers = routers.DefaultRouter()
routers.register(r'cliente', views.clienteviews, 'cliente')

urlpatterns = [
    path('api/v1/', include(routers.urls) ),
    path('docs/', include_docs_urls(title='cliente API'))
]



