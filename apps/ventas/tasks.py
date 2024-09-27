from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Venta, Factura
from django.db.models import Sum
import csv
import os

# Tarea para generar un reporte de ventas diario
@shared_task
def generar_reporte_ventas_diario():
    hoy = timezone.now().date()
    ventas = Venta.objects.filter(creado_en__date=hoy)
    total_ventas = ventas.aggregate(total=Sum('monto_total'))['total'] or 0

    # Crear el archivo CSV
    reporte_path = f'reportes/ventas_diarias_{hoy}.csv'
    os.makedirs(os.path.dirname(reporte_path), exist_ok=True)
    with open(reporte_path, 'w', newline='') as csvfile:
        fieldnames = ['numero_venta', 'cliente', 'monto_total', 'fecha']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for venta in ventas:
            writer.writerow({
                'numero_venta': venta.numero_venta,
                'cliente': venta.cliente.nombre,
                'monto_total': venta.monto_total,
                'fecha': venta.creado_en
            })

    # Enviar el reporte por email
    send_mail(
        'Reporte de Ventas Diario',
        f'El reporte de ventas diario ha sido generado. Total de ventas: {total_ventas}',
        'noreply@tuempresa.com',
        ['admin@tuempresa.com'],
        fail_silently=False,
    )

# Tarea para generar un reporte de facturas mensuales
@shared_task
def generar_reporte_facturas_mensual():
    hoy = timezone.now().date()
    primer_dia_mes = hoy.replace(day=1)
    facturas = Factura.objects.filter(creado_en__date__gte=primer_dia_mes, creado_en__date__lte=hoy)
    total_facturas = facturas.aggregate(total=Sum('total'))['total'] or 0

    # Crear el archivo CSV
    reporte_path = f'reportes/facturas_mensuales_{primer_dia_mes}_{hoy}.csv'
    os.makedirs(os.path.dirname(reporte_path), exist_ok=True)
    with open(reporte_path, 'w', newline='') as csvfile:
        fieldnames = ['numero_factura', 'cliente', 'total', 'fecha_emision']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for factura in facturas:
            writer.writerow({
                'numero_factura': factura.numero_factura,
                'cliente': factura.cotizacion.cliente.nombre,
                'total': factura.total,
                'fecha_emision': factura.fecha_emision
            })

    # Enviar el reporte por email
    send_mail(
        'Reporte de Facturas Mensual',
        f'El reporte de facturas mensual ha sido generado. Total de facturas: {total_facturas}',
        'noreply@tuempresa.com',
        ['admin@tuempresa.com'],
        fail_silently=False,
    )

# Tarea para enviar recordatorios de pago
@shared_task
def enviar_recordatorios_pago():
    hoy = timezone.now().date()
    facturas_pendientes = Factura.objects.filter(estado_pago='pendiente', fecha_vencimiento__lt=hoy)

    for factura in facturas_pendientes:
        send_mail(
            'Recordatorio de Pago',
            f'Estimado {factura.cotizacion.cliente.nombre},\n\n'
            f'Le recordamos que su factura {factura.numero_factura} está pendiente de pago. '
            f'Por favor, realice el pago a la mayor brevedad posible.\n\n'
            f'Total: {factura.total}\n'
            f'Fecha de Vencimiento: {factura.fecha_vencimiento}\n\n'
            f'Gracias,\n'
            f'Tu Empresa',
            'noreply@tuempresa.com',
            [factura.cotizacion.cliente.email],
            fail_silently=False,
        )
