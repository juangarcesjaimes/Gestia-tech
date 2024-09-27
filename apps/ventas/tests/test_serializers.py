from django.test import TestCase
from django.contrib.auth.models import User
from ventas.models import Cliente, Producto, Cotizacion, Venta, Factura
from ventas.serializers import ClienteSerializer, ProductoSerializer, CotizacionSerializer, VentaSerializer, FacturaSerializer

class ClienteSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.cliente_data = {
            'nombre': 'Cliente Test',
            'email': 'cliente@test.com',
            'telefono': '123456789',
            'tipo_cliente': 'individual'
        }

    def test_cliente_serializer(self):
        serializer = ClienteSerializer(data=self.cliente_data)
        self.assertTrue(serializer.is_valid())
        cliente = serializer.save(creado_por=self.user)
        self.assertEqual(cliente.nombre, 'Cliente Test')
        self.assertEqual(cliente.email, 'cliente@test.com')
        self.assertEqual(cliente.telefono, '123456789')
        self.assertEqual(cliente.tipo_cliente, 'individual')
        self.assertEqual(cliente.creado_por, self.user)

class ProductoSerializerTest(TestCase):
    def setUp(self):
        self.producto_data = {
            'nombre': 'Producto Test',
            'precio': 100.00,
            'stock': 10
        }

    def test_producto_serializer(self):
        serializer = ProductoSerializer(data=self.producto_data)
        self.assertTrue(serializer.is_valid())
        producto = serializer.save()
        self.assertEqual(producto.nombre, 'Producto Test')
        self.assertEqual(producto.precio, 100.00)
        self.assertEqual(producto.stock, 10)

class CotizacionSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
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

    def test_cotizacion_serializer(self):
        serializer = CotizacionSerializer(data=self.cotizacion_data)
        self.assertTrue(serializer.is_valid())
        cotizacion = serializer.save(creado_por=self.user)
        self.assertEqual(cotizacion.cliente, self.cliente)
        self.assertEqual(cotizacion.producto, self.producto)
        self.assertEqual(cotizacion.cantidad, 2)
        self.assertEqual(cotizacion.precio_unitario, 100.00)
        self.assertEqual(cotizacion.total, 200.00)
        self.assertEqual(cotizacion.creado_por, self.user)

class VentaSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
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

    def test_venta_serializer(self):
        serializer = VentaSerializer(data=self.venta_data)
        self.assertTrue(serializer.is_valid())
        venta = serializer.save(creado_por=self.user)
        self.assertEqual(venta.numero_venta, 'V001')
        self.assertEqual(venta.cliente, self.cliente)
        self.assertEqual(venta.producto, self.producto)
        self.assertEqual(venta.cantidad, 2)
        self.assertEqual(venta.precio_unitario, 100.00)
        self.assertEqual(venta.total, 200.00)
        self.assertEqual(venta.creado_por, self.user)

class FacturaSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
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

    def test_factura_serializer(self):
        serializer = FacturaSerializer(data=self.factura_data)
        self.assertTrue(serializer.is_valid())
        factura = serializer.save()
        self.assertEqual(factura.cotizacion, self.cotizacion)
        self.assertEqual(factura.numero_factura, 'F001')
        self.assertEqual(factura.total, 200.00)
