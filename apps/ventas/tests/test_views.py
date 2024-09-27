from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ventas.models import Cliente, Producto, Cotizacion, Venta, Factura

class ClienteViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.cliente_data = {
            'nombre': 'Cliente Test',
            'email': 'cliente@test.com',
            'telefono': '123456789',
            'tipo_cliente': 'individual'
        }
        self.cliente = Cliente.objects.create(**self.cliente_data, creado_por=self.user)

    def test_list_clientes(self):
        url = reverse('cliente-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_cliente(self):
        url = reverse('cliente-list')
        response = self.client.post(url, self.cliente_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 2)

class ProductoViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.producto_data = {
            'nombre': 'Producto Test',
            'precio': 100.00,
            'stock': 10
        }
        self.producto = Producto.objects.create(**self.producto_data)

    def test_list_productos(self):
        url = reverse('producto-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_producto(self):
        url = reverse('producto-list')
        response = self.client.post(url, self.producto_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 2)

class CotizacionViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.cliente = Cliente.objects.create(
            nombre='Cliente Test',
            email='cliente@test.com',
            telefono='123456789',
            tipo_cliente='individual',
            creado_por=self.user
        )
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            precio=100.00,
            stock=10
        )
        self.cotizacion_data = {
            'cliente': self.cliente.id,
            'producto': self.producto.id,
            'cantidad': 2,
            'precio_unitario': 100.00
        }
        self.cotizacion = Cotizacion.objects.create(**self.cotizacion_data, creado_por=self.user)

    def test_list_cotizaciones(self):
        url = reverse('cotizacion-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_cotizacion(self):
        url = reverse('cotizacion-list')
        response = self.client.post(url, self.cotizacion_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cotizacion.objects.count(), 2)

    def test_convertir_a_venta(self):
        url = reverse('cotizacion-convertir-a-venta', args=[self.cotizacion.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Venta.objects.count(), 1)

class VentaViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.cliente = Cliente.objects.create(
            nombre='Cliente Test',
            email='cliente@test.com',
            telefono='123456789',
            tipo_cliente='individual',
            creado_por=self.user
        )
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            precio=100.00,
            stock=10
        )
        self.venta_data = {
            'numero_venta': 'V001',
            'cliente': self.cliente.id,
            'producto': self.producto.id,
            'cantidad': 2,
            'precio_unitario': 100.00
        }
        self.venta = Venta.objects.create(**self.venta_data, creado_por=self.user)

    def test_list_ventas(self):
        url = reverse('venta-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_venta(self):
        url = reverse('venta-list')
        response = self.client.post(url, self.venta_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Venta.objects.count(), 2)

class FacturaViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.cliente = Cliente.objects.create(
            nombre='Cliente Test',
            email='cliente@test.com',
            telefono='123456789',
            tipo_cliente='individual',
            creado_por=self.user
        )
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            precio=100.00,
            stock=10
        )
        self.cotizacion = Cotizacion.objects.create(
            cliente=self.cliente,
            producto=self.producto,
            cantidad=2,
            precio_unitario=100.00,
            creado_por=self.user
        )
        self.factura_data = {
            'cotizacion': self.cotizacion.id,
            'numero_factura': 'F001',
            'total': 200.00
        }
        self.factura = Factura.objects.create(**self.factura_data)

    def test_list_facturas(self):
        url = reverse('factura-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_factura(self):
        url = reverse('factura-list')
        response = self.client.post(url, self.factura_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Factura.objects.count(), 2)
