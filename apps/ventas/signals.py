from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Venta, Factura, Producto, Cotizacion

@receiver(pre_save, sender=Venta)
def actualizar_stock_producto(sender, instance, **kwargs):
    """
    Señal para actualizar el stock del producto antes de guardar una venta.
    """
    if instance.pk:
        # Si la venta ya existe, obtener la venta anterior
        venta_anterior = Venta.objects.get(pk=instance.pk)
        # Revertir el stock del producto
        instance.producto.stock += venta_anterior.cantidad
    # Reducir el stock del producto
    instance.producto.stock -= instance.cantidad
    instance.producto.save()

@receiver(post_save, sender=Factura)
def notificar_cliente_factura(sender, instance, created, **kwargs):
    """
    Señal para notificar al cliente cuando se crea una factura.
    """
    if created:
        cliente = instance.cotizacion.cliente
        send_mail(
            'Factura Generada',
            f'Estimado {cliente.nombre},\n\n'
            f'Se ha generado una nueva factura con el número {instance.numero_factura}.\n'
            f'Total: {instance.total}\n\n'
            f'Gracias por su compra.\n'
            f'Tu Empresa',
            'noreply@tuempresa.com',
            [cliente.email],
            fail_silently=False,
        )

@receiver(post_save, sender=Cotizacion)
def actualizar_total_cotizacion(sender, instance, created, **kwargs):
    """
    Señal para actualizar el total de la cotización después de guardarla.
    """
    if created:
        instance.total = instance.cantidad * instance.precio_unitario
        instance.save()

@receiver(post_save, sender=Venta)
def actualizar_total_venta(sender, instance, created, **kwargs):
    """
    Señal para actualizar el total de la venta después de guardarla.
    """
    if created:
        instance.total = instance.cantidad * instance.precio_unitario
        instance.save()
