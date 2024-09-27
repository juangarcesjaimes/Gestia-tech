from django.contrib import admin
from .models import Cliente, Producto, Cotizacion, Venta, Factura, Categoria, Proveedor

admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Cotizacion)
admin.site.register(Venta)
admin.site.register(Factura)
admin.site.register(Categoria)
admin.site.register(Proveedor)




'''
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'tipo_cliente', 'creado_en', 'actualizado_en')
    search_fields = ('nombre', 'email', 'telefono')
    list_filter = ('tipo_cliente', 'creado_en', 'actualizado_en')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'esta_activo', 'creado_en', 'actualizado_en')
    search_fields = ('nombre', 'sku')
    list_filter = ('esta_activo', 'creado_en', 'actualizado_en')

@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'get_cliente', 'precio', 'get_cantidad', 'total', 'estado', 'creado_en', 'actualizado_en')
    search_fields = ('producto', 'cliente__nombre')
    list_filter = ('estado', 'creado_en', 'actualizado_en')

    def get_cliente(self, obj):
        return obj.cliente.nombre
    get_cliente.short_description = 'Cliente'

    def get_cantidad(self, obj):
        return obj.cantidad
    get_cantidad.short_description = 'Cantidad'

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('numero_venta', 'cliente', 'monto_total', 'estado', 'creado_en', 'get_actualizado_en')
    search_fields = ('numero_venta', 'cliente__nombre')
    list_filter = ('estado', 'creado_en', 'get_actualizado_en')

    def get_actualizado_en(self, obj):
        return obj.actualizado_en
    get_actualizado_en.short_description = 'Actualizado en'

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'get_cliente', 'total', 'estado_pago', 'fecha_emision', 'fecha_vencimiento')
    search_fields = ('numero_factura', 'cliente__nombre')
    list_filter = ('estado_pago', 'fecha_emision', 'fecha_vencimiento')

    def get_cliente(self, obj):
        return obj.cotizacion.cliente.nombre
    get_cliente.short_description = 'Cliente'

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'informacion_contacto')
    search_fields = ('nombre',)
'''