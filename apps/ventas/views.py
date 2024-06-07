from rest_framework import viewsets
from .serializers import ClienteSerializer
from .models import Cliente

# Vistas de Django REST Framework
class clienteviews(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()
