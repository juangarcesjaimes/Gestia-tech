from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


# Módulo ventas: aquí podemos crear, editar y eliminar clientes
class Cliente(models.Model):
    # Opciones para el tipo de cliente
    TIPO_CLIENTE_CHOICES = [
        ('individual', 'Individual'),
        ('business', 'Business')
    ]

    # Opciones para el método de pago preferido
    METODO_PAGO_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal')
    ]

    # Nombre del cliente
    nombre = models.CharField(max_length=255)
    # Email del cliente, debe ser único
    email = models.EmailField(unique=True)
    # Teléfono del cliente, opcional
    telefono = models.CharField(max_length=20, blank=True, null=True)
    # Dirección del cliente, opcional
    direccion = models.CharField(max_length=255, blank=True, null=True)
    # Ciudad del cliente, opcional
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    # Estado del cliente, opcional
    estado = models.CharField(max_length=100, blank=True, null=True)
    # País del cliente, opcional
    pais = models.CharField(max_length=100, blank=True, null=True)
    # Código postal del cliente, opcional
    codigo_postal = models.CharField(max_length=20, blank=True, null=True)
    # Nombre de la empresa del cliente, opcional
    nombre_empresa = models.CharField(max_length=255, blank=True, null=True)
    # Sitio web de la empresa del cliente, opcional
    sitio_web = models.URLField(blank=True, null=True)
    # Industria de la empresa del cliente, opcional
    industria = models.CharField(max_length=100, blank=True, null=True)
    # Persona de contacto en la empresa del cliente, opcional
    persona_contacto = models.CharField(max_length=255, blank=True, null=True)
    # Teléfono de la persona de contacto, opcional
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True)
    # Email de la persona de contacto, opcional
    email_contacto = models.EmailField(blank=True, null=True)
    # Notas adicionales sobre el cliente, opcional
    notas = models.TextField(blank=True, null=True)
    # Tipo de cliente: individual o empresa
    tipo_cliente = models.CharField(max_length=50, choices=TIPO_CLIENTE_CHOICES, default='individual')
    # Método de pago preferido del cliente
    metodo_pago_preferido = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES, default='credit_card')
    # Límite de crédito del cliente, opcional, no puede ser negativo
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    # Saldo pendiente del cliente, opcional, no puede ser negativo
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    # Puntos de fidelidad del cliente, no puede ser negativo
    puntos_fidelidad = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    # Usuario que creó el registro del cliente
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clientes_creados')
    # Usuario que actualizó el registro del cliente
    actualizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clientes_actualizados')
    # Fecha y hora en que se creó el registro del cliente
    creado_en = models.DateTimeField(auto_now_add=True)
    # Fecha y hora en que se actualizó el registro del cliente
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Representación en cadena del objeto Cliente
        return self.nombre

    def clean(self):
        # Validación personalizada para asegurar que el saldo pendiente no exceda el límite de crédito
        if self.limite_credito and self.saldo_pendiente and self.saldo_pendiente > self.limite_credito:
            raise ValidationError('El saldo pendiente no puede exceder el límite de crédito.')

    def save(self, *args, **kwargs):
        # Llama a la validación personalizada antes de guardar
        self.full_clean()
        super().save(*args, **kwargs)


class Producto(models.Model):
    # Nombre del producto
    nombre = models.CharField(max_length=100, help_text="Nombre del producto")
    # Descripción del producto
    descripcion = models.TextField(help_text="Descripción del producto")
    # Precio del producto, no puede ser negativo
    precio = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio del producto", validators=[MinValueValidator(0)])
    # Cantidad de stock disponible, no puede ser negativo
    stock = models.PositiveIntegerField(help_text="Cantidad de stock disponible", validators=[MinValueValidator(0)])
    # Imagen del producto, opcional
    imagen = models.ImageField(upload_to='products/', null=True, blank=True, help_text="Imagen del producto")
    # Peso del producto, opcional
    peso = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Peso del producto", validators=[MinValueValidator(0)])
    # Altura del producto, opcional
    altura = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Altura del producto", validators=[MinValueValidator(0)])
    # Anchura del producto, opcional
    anchura = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Anchura del producto", validators=[MinValueValidator(0)])
    # Profundidad del producto, opcional
    profundidad = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Profundidad del producto", validators=[MinValueValidator(0)])
    # Fecha y hora de creación del producto
    creado_en = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación del producto")
    # Fecha y hora de la última actualización del producto
    actualizado_en = models.DateTimeField(auto_now=True, help_text="Fecha y hora de la última actualización del producto")
    # Notas adicionales sobre el producto, opcional
    notas = models.TextField(null=True, blank=True, help_text="Notas adicionales sobre el producto")
    # Estado del producto (activo/inactivo)
    esta_activo = models.BooleanField(default=True, help_text="Estado del producto")
    # Fabricante del producto, opcional
    fabricante = models.CharField(max_length=100, null=True, blank=True, help_text="Fabricante del producto")
    # Número de referencia del producto (SKU), opcional
    sku = models.CharField(max_length=100, null=True, blank=True, help_text="Número de referencia del producto (SKU)")
    # Categoría del producto, opcional
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True, help_text="Categoría del producto")
    # Proveedor del producto, opcional
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True, blank=True, help_text="Proveedor del producto")
    # Código único del producto, opcional
    codigo_producto = models.CharField(max_length=100, null=True, blank=True, help_text="Código único del producto")

    def __str__(self):
        # Representación en cadena del objeto Producto
        return self.nombre

    def clean(self):
        # Validación personalizada para asegurar que el stock no sea negativo
        if self.stock < 0:
            raise ValidationError('El stock no puede ser negativo.')

    def save(self, *args, **kwargs):
        # Llama a la validación personalizada antes de guardar
        self.full_clean()
        super().save(*args, **kwargs)

# Clase categoría de producto
class Categoria(models.Model):
    # Nombre de la categoría
    nombre = models.CharField(max_length=100, help_text="Nombre de la categoría")
    # Descripción de la categoría, opcional
    descripcion = models.TextField(null=True, blank=True, help_text="Descripción de la categoría")

    def __str__(self):
        # Representación en cadena del objeto Categoria
        return self.nombre

# Clase proveedores
class Proveedor(models.Model):
    # Nombre del proveedor
    nombre = models.CharField(max_length=100, help_text="Nombre del proveedor")
    # Información de contacto del proveedor, opcional
    informacion_contacto = models.TextField(null=True, blank=True, help_text="Información de contacto del proveedor")

    def __str__(self):
        # Representación en cadena del objeto Proveedor
        return self.nombre

# Modelo de Facturación
class Factura(models.Model):
    # Relación con el modelo de cotización
    cotizacion = models.ForeignKey('Cotizacion', on_delete=models.CASCADE, help_text="Cotización asociada a la factura")
    # Número de la factura
    numero_factura = models.CharField(max_length=255, help_text="Número de la factura")
    # Fecha de emisión de la factura
    fecha_emision = models.DateTimeField(auto_now_add=True, help_text="Fecha de emisión de la factura")
    # Fecha de vencimiento de la factura
    fecha_vencimiento = models.DateTimeField(help_text="Fecha de vencimiento de la factura")
    # Estado de pago de la factura
    pagado = models.BooleanField(default=False, help_text="Estado de pago de la factura")
    # Fecha de pago de la factura, opcional
    fecha_pago = models.DateTimeField(blank=True, null=True, help_text="Fecha de pago de la factura")
    # Método de pago utilizado, opcional
    metodo_pago = models.CharField(max_length=50, choices=[
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal')
    ], blank=True, null=True, help_text="Método de pago utilizado")
    # Estado del pago
    estado_pago = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue')
    ], default='pending', help_text="Estado del pago")
    # Descuento aplicado, opcional
    descuento_aplicado = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], help_text="Descuento aplicado")
    # Impuesto aplicado, opcional
    impuesto = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], help_text="Impuesto aplicado")
    # Total de la factura
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Total de la factura")
    # Moneda utilizada
    moneda = models.CharField(max_length=10, default='USD', help_text="Moneda utilizada")
    # Notas adicionales, opcional
    notas = models.TextField(blank=True, null=True, help_text="Notas adicionales")
    # Términos y condiciones, opcional
    terminos_y_condiciones = models.TextField(blank=True, null=True, help_text="Términos y condiciones")
    # Archivos adjuntos, opcional
    adjuntos = models.FileField(upload_to='facturas/adjuntos/', blank=True, null=True, help_text="Archivos adjuntos")
    # Historial de cambios, opcional
    historial_cambios = models.JSONField(blank=True, null=True, help_text="Historial de cambios")
    # Dirección de facturación, opcional
    direccion_facturacion = models.CharField(max_length=255, blank=True, null=True, help_text="Dirección de facturación")
    # Dirección de envío, opcional
    direccion_envio = models.CharField(max_length=255, blank=True, null=True, help_text="Dirección de envío")
    # Persona de contacto, opcional
    persona_contacto = models.CharField(max_length=255, blank=True, null=True, help_text="Persona de contacto")
    # Teléfono de contacto, opcional
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True, help_text="Teléfono de contacto")
    # Email de contacto, opcional
    email_contacto = models.EmailField(blank=True, null=True, help_text="Email de contacto")
    # Número de orden de compra, opcional
    numero_orden_compra = models.CharField(max_length=255, blank=True, null=True, help_text="Número de orden de compra")
    # Número de referencia del cliente, opcional
    numero_referencia_cliente = models.CharField(max_length=255, blank=True, null=True, help_text="Número de referencia del cliente")
    # Condiciones de entrega, opcional
    condiciones_entrega = models.TextField(blank=True, null=True, help_text="Condiciones de entrega")
    # Detalles del producto o servicio, opcional
    detalles_producto_servicio = models.TextField(blank=True, null=True, help_text="Detalles del producto o servicio")
    # Fecha y hora de creación de la factura
    creado_en = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación de la factura")
    # Fecha y hora de la última actualización de la factura
    actualizado_en = models.DateTimeField(auto_now=True, help_text="Fecha y hora de la última actualización de la factura")
    # Cargo por pago tardío, opcional
    cargo_pago_tardio = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], help_text="Cargo por pago tardío")
    # Descuento por pago anticipado, opcional
    descuento_pago_anticipado = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], help_text="Descuento por pago anticipado")
    # Enlace de pago, opcional
    enlace_pago = models.URLField(blank=True, null=True, help_text="Enlace de pago")
    # Indica si la factura es recurrente
    factura_recurrente = models.BooleanField(default=False, help_text="Indica si la factura es recurrente")
    # Periodo de recurrencia, opcional
    periodo_recurrencia = models.CharField(max_length=50, choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually')
    ], blank=True, null=True, help_text="Periodo de recurrencia")
    # Indica si se ha enviado un recordatorio
    recordatorio_enviado = models.BooleanField(default=False, help_text="Indica si se ha enviado un recordatorio")
    # Fecha del recordatorio, opcional
    fecha_recordatorio = models.DateTimeField(blank=True, null=True, help_text="Fecha del recordatorio")

    def __str__(self):
        # Representación en cadena del objeto Factura
        return f"Factura {self.numero_factura} para {self.cotizacion.cliente.nombre}"

# Modelo de Cotización
class Cotizacion(models.Model):
    # Relación con el modelo de Lead
    Cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, help_text="Cliente asociado a la cotización")
    # Nombre del producto
    producto = models.CharField(max_length=255, help_text="Nombre del producto")
    # Descripción del producto, opcional
    descripcion_producto = models.TextField(blank=True, null=True, help_text="Descripción del producto")
    # Precio del producto
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Precio del producto")
    # Descuento aplicado, opcional
    descuento = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], help_text="Descuento aplicado")
    # Impuesto aplicado, opcional
    impuesto = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], help_text="Impuesto aplicado")
    # Total de la cotización
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Total de la cotización")
    # Fecha de expiración de la cotización, opcional
    fecha_expiracion = models.DateTimeField(blank=True, null=True, help_text="Fecha de expiración de la cotización")
    # Estado de la cotización
    estado = models.CharField(max_length=50, choices=[
        ('draft', 'Borrador'),
        ('sent', 'Enviada'),
        ('accepted', 'Aceptada'),
        ('rejected', 'Rechazada')
    ], default='draft', help_text="Estado de la cotización")
    # Notas adicionales, opcional
    notas = models.TextField(blank=True, null=True, help_text="Notas adicionales")
    # Método de pago preferido
    metodo_pago = models.CharField(max_length=50, choices=[
        ('credit_card', 'Tarjeta de Crédito'),
        ('bank_transfer', 'Transferencia Bancaria'),
        ('paypal', 'PayPal')
    ], default='credit_card', help_text="Método de pago preferido")
    # Moneda utilizada
    moneda = models.CharField(max_length=10, default='USD', help_text="Moneda utilizada")
    # Términos y condiciones, opcional
    terminos_y_condiciones = models.TextField(blank=True, null=True, help_text="Términos y condiciones")
    # Archivos adjuntos, opcional
    adjuntos = models.FileField(upload_to='cotizaciones/adjuntos/', blank=True, null=True, help_text="Archivos adjuntos")
    # Fecha y hora de creación de la cotización
    creado_en = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación de la cotización")
    # Fecha y hora de la última actualización de la cotización
    actualizado_en = models.DateTimeField(auto_now=True, help_text="Fecha y hora de la última actualización de la cotización")
    # Usuario que aprobó la cotización, opcional
    aprobado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='cotizaciones_aprobadas', help_text="Usuario que aprobó la cotización")
    # Fecha de aprobación de la cotización, opcional
    fecha_aprobacion = models.DateTimeField(blank=True, null=True, help_text="Fecha de aprobación de la cotización")
    # Fecha de entrega estimada, opcional
    fecha_entrega = models.DateTimeField(blank=True, null=True, help_text="Fecha de entrega estimada")
    # Dirección de envío, opcional
    direccion_envio = models.CharField(max_length=255, blank=True, null=True, help_text="Dirección de envío")
    # Dirección de facturación, opcional
    direccion_facturacion = models.CharField(max_length=255, blank=True, null=True, help_text="Dirección de facturación")
    # Persona de contacto, opcional
    persona_contacto = models.CharField(max_length=255, blank=True, null=True, help_text="Persona de contacto")
    # Teléfono de contacto, opcional
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True, help_text="Teléfono de contacto")
    # Email de contacto, opcional
    email_contacto = models.EmailField(blank=True, null=True, help_text="Email de contacto")
    # Términos de pago, opcional
    terminos_pago = models.CharField(max_length=255, blank=True, null=True, help_text="Términos de pago")
    # Condiciones de entrega, opcional
    condiciones_entrega = models.CharField(max_length=255, blank=True, null=True, help_text="Condiciones de entrega")
    # Periodo de garantía, opcional
    periodo_garantia = models.CharField(max_length=50, blank=True, null=True, help_text="Periodo de garantía")
    # Acuerdo de nivel de servicio, opcional
    acuerdo_nivel_servicio = models.TextField(blank=True, null=True, help_text="Acuerdo de nivel de servicio")
    # Servicios adicionales, opcional
    servicios_adicionales = models.TextField(blank=True, null=True, help_text="Servicios adicionales")
    # Instrucciones especiales, opcional
    instrucciones_especiales = models.TextField(blank=True, null=True, help_text="Instrucciones especiales")

    def __str__(self):
        return f"Cotización para {self.lead.nombre} - {self.producto}"

    def convertir_a_venta(self, vendedor):
        # Método para convertir una cotización en una venta
        if self.producto.stock < self.cantidad:
            raise ValidationError('Stock insuficiente para el producto seleccionado.')
        venta = Venta.objects.create(
            cliente=self.lead.cliente,
            producto=self.producto,
            cantidad=1,  # Asumiendo que la cotización es para una unidad del producto
            precio_unitario=self.precio,
            total=self.total,
            factura=None,  # La factura se puede generar después
            creado_por=vendedor,
            actualizado_por=vendedor
        )
        return venta

    def save(self, *args, **kwargs):
        # Cálculo del total
        self.total = self.precio - (self.descuento or 0) + (self.impuesto or 0)
        super().save(*args, **kwargs)

# Modelo de Venta
class Venta(models.Model):
    # Número único de la venta
    numero_venta = models.CharField(max_length=255, unique=True, help_text="Número único de la venta")
    # Relación con el modelo de Cliente
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, help_text="Cliente asociado a la venta")
    # Fecha y hora de creación de la venta
    creado_en = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación de la venta")
    # Fecha estimada de entrega, opcional
    fecha_entrega_estimada = models.DateTimeField(blank=True, null=True, help_text="Fecha estimada de entrega")
    # Estado de la venta
    estado = models.CharField(max_length=50, choices=[
        ('nuevo', 'Nuevo'),
        ('procesando', 'Procesando'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado')
    ], default='nuevo', help_text="Estado de la venta")
    # Dirección de envío
    direccion_envio = models.CharField(max_length=255, help_text="Dirección de envío")
    # Dirección de facturación
    direccion_facturacion = models.CharField(max_length=255, help_text="Dirección de facturación")
    # Método de envío
    metodo_envio = models.CharField(max_length=50, choices=[
        ('estándar', 'Estándar'),
        ('expreso', 'Expreso')
    ], default='estándar', help_text="Método de envío")
    # Método de pago
    metodo_pago = models.CharField(max_length=50, choices=[
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('transferencia_bancaria', 'Transferencia Bancaria'),
        ('paypal', 'PayPal')
    ], default='tarjeta_credito', help_text="Método de pago")
    # Monto total de la venta
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Monto total de la venta")
    # Descuento aplicado, opcional
    descuento_aplicado = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], help_text="Descuento aplicado")
    # Impuesto aplicado, opcional
    impuesto = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], help_text="Impuesto aplicado")
    # Moneda utilizada
    moneda = models.CharField(max_length=10, default='USD', help_text="Moneda utilizada")
    # Notas adicionales, opcional
    notas = models.TextField(blank=True, null=True, help_text="Notas adicionales")
    # Historial de cambios, opcional
    historial_cambios = models.JSONField(blank=True, null=True, help_text="Historial de cambios")
    # Detalles de productos y servicios
    productos_servicios = models.JSONField(help_text="Detalles de productos y servicios")
    # Cantidad de productos
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Cantidad de productos")
    # Precio unitario de los productos
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Precio unitario de los productos")
    # Subtotal de la venta
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Subtotal de la venta")
    # Archivos adjuntos, opcional
    adjuntos = models.FileField(upload_to='ventas/adjuntos/', blank=True, null=True, help_text="Archivos adjuntos")
    # Persona de contacto, opcional
    persona_contacto = models.CharField(max_length=255, blank=True, null=True, help_text="Persona de contacto")
    # Teléfono de contacto, opcional
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True, help_text="Teléfono de contacto")
    # Email de contacto, opcional
    email_contacto = models.EmailField(blank=True, null=True, help_text="Email de contacto")
    # Número de seguimiento, opcional
    numero_seguimiento = models.CharField(max_length=255, blank=True, null=True, help_text="Número de seguimiento")
    # Fecha de pago, opcional
    fecha_pago = models.DateTimeField(blank=True, null=True, help_text="Fecha de pago")
    # Estado del pago
    estado_pago = models.CharField(max_length=50, choices=[
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido')
    ], default='pendiente', help_text="Estado del pago")
    # Términos de pago, opcional
    terminos_pago = models.CharField(max_length=255, blank=True, null=True, help_text="Términos de pago")
    # Condiciones de entrega, opcional
    condiciones_entrega = models.TextField(blank=True, null=True, help_text="Condiciones de entrega")
    # Instrucciones especiales, opcional
    instrucciones_especiales = models.TextField(blank=True, null=True, help_text="Instrucciones especiales")
    # Usuario que aprobó la venta, opcional
    aprobado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas_aprobadas', help_text="Usuario que aprobó la venta")
    # Fecha de aprobación de la venta, opcional
    fecha_aprobacion = models.DateTimeField(blank=True, null=True, help_text="Fecha de aprobación de la venta")
    # Comentarios del cliente, opcional
    comentarios_cliente = models.TextField(blank=True, null=True, help_text="Comentarios del cliente")
    # Estado de la entrega
    estado_entrega = models.CharField(max_length=50, choices=[
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('devuelto', 'Devuelto')
    ], default='pendiente', help_text="Estado de la entrega")
    # Razón de la devolución, opcional
    razon_devolucion = models.TextField(blank=True, null=True, help_text="Razón de la devolución")
    # Monto del reembolso, opcional
    monto_reembolso = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], help_text="Monto del reembolso")
    # Puntos de fidelidad utilizados
    puntos_fidelidad_utilizados = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], help_text="Puntos de fidelidad utilizados")
    # Puntos de fidelidad ganados
    puntos_fidelidad_ganados = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], help_text="Puntos de fidelidad ganados")
    # Relación con el modelo de Factura, opcional
    factura = models.ForeignKey('Factura', on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas', help_text="Factura asociada a la venta")

    def __str__(self):
        return f"Venta {self.numero_venta} para {self.cliente.nombre}"

    def clean(self):
        # Validación personalizada para asegurar que el monto total no sea negativo
        if self.monto_total < 0:
            raise ValidationError('El monto total no puede ser negativo.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a la validación personalizada antes de guardar
        super().save(*args, **kwargs)

    def actualizar_estado(self, nuevo_estado):
        # Método para actualizar el estado de la venta
        self.estado = nuevo_estado
        self.save()

    def agregar_historial_cambio(self, cambio):
        # Método para agregar un cambio al historial de cambios
        if not self.historial_cambios:
            self.historial_cambios = []
        self.historial_cambios.append(cambio)
        self.save()
