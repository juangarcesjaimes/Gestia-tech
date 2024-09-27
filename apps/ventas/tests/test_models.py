from django.test import TestCase
from django.contrib.auth.models import User
from ventas.models import Cliente, Producto, Cotizacion, Venta, Factura, Categoria, Proveedor

class ClienteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.cliente = Cliente.objects.create(
            nombre='Cliente Test',
            email='cliente@test.com',
            telefono='123456789',
            tipo_cliente='individual',
            creado_por=self.user
        )

    def test_cliente_creation(self):
        self.assertEqual(self.cliente.nombre, 'Cliente Test')
        self.assertEqual(self.cliente.email, 'cliente@test.com')
        self.assertEqual(self.cliente.telefono, '123456789')
        self.assertEqual(self.cliente.tipo_cliente, 'individual')
        self.assertEqual(self.cliente.creado_por, self.user)

class ProductoModelTest(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            precio=100.00,
            stock=10
        )

    def test_producto_creation(self):
        self.assertEqual(self.producto.nombre, 'Producto Test')
        self.assertEqual(self.producto.precio, 100.00)
        self.assertEqual(self.producto.stock, 10)

class CotizacionModelTest(TestCase):
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

    def test_cotizacion_creation(self):
        self.assertEqual(self.cotizacion.cliente, self.cliente)
        self.assertEqual(self.cotizacion.producto, self.producto)
        self.assertEqual(self.cotizacion.cantidad, 2)
        self.assertEqual(self.cotizacion.precio_unitario, 100.00)
        self.assertEqual(self.cotizacion.total, 200.00)
        self.assertEqual(self.cotizacion.creado_por, self.user)

class VentaModelTest(TestCase):
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
        self.venta = Venta.objects.create(
            numero_venta='V001',
            cliente=self.cliente,
            producto=self.producto,
            cantidad=2,
            precio_unitario=100.00,
            creado_por=self.user
        )

    def test_venta_creation(self):
        self.assertEqual(self.venta.numero_venta, 'V001')
        self.assertEqual(self.venta.cliente, self.cliente)
        self.assertEqual(self.venta.producto, self.producto)
        self.assertEqual(self.venta.cantidad, 2)
        self.assertEqual(self.venta.precio_unitario, 100.00)
        self.assertEqual(self.venta.total, 200.00)
        self.assertEqual(self.venta.creado_por, self.user)

class FacturaModelTest(TestCase):
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
        self.factura = Factura.objects.create(
            cotizacion=self.cotizacion,
            numero_factura='F001',
            total=200.00
        )

    def test_factura_creation(self):
        self.assertEqual(self.factura.cotizacion, self.cotizacion)
        self.assertEqual(self.factura.numero_factura, 'F001')
        self.assertEqual(self.factura.total, 200.00)
