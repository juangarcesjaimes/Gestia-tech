from rest_framework import serializers
from .models import Cliente, Producto, Cotizacion, Venta, Factura, Categoria, Proveedor

# Serializador para el modelo Cliente
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['creado_por', 'actualizado_por', 'creado_en', 'actualizado_en']

    def create(self, validated_data):
        validated_data['creado_por'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['actualizado_por'] = self.context['request'].user
        return super().update(instance, validated_data)

# Serializador para el modelo Producto
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
        read_only_fields = ['creado_en', 'actualizado_en']

# Serializador para el modelo Cotizacion
class CotizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotizacion
        fields = '__all__'
        read_only_fields = ['creado_por', 'actualizado_por', 'creado_en', 'actualizado_en', 'total']

    def create(self, validated_data):
        validated_data['creado_por'] = self.context['request'].user
        validated_data['total'] = validated_data['cantidad'] * validated_data['precio_unitario']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['actualizado_por'] = self.context['request'].user
        if 'cantidad' in validated_data or 'precio_unitario' in validated_data:
            validated_data['total'] = validated_data.get('cantidad', instance.cantidad) * validated_data.get('precio_unitario', instance.precio_unitario)
        return super().update(instance, validated_data)

    def convertir_a_venta(self, cotizacion, vendedor):
        venta = cotizacion.convertir_a_venta(vendedor)
        return VentaSerializer(venta).data

# Serializador para el modelo Venta
class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'
        read_only_fields = ['creado_por', 'actualizado_por', 'creado_en', 'actualizado_en', 'total']

    def create(self, validated_data):
        validated_data['creado_por'] = self.context['request'].user
        validated_data['total'] = validated_data['cantidad'] * validated_data['precio_unitario']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['actualizado_por'] = self.context['request'].user
        if 'cantidad' in validated_data or 'precio_unitario' in validated_data:
            validated_data['total'] = validated_data.get('cantidad', instance.cantidad) * validated_data.get('precio_unitario', instance.precio_unitario)
        return super().update(instance, validated_data)

# Serializador para el modelo Factura
class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'
        read_only_fields = ['creado_en', 'actualizado_en']

# Serializador para el modelo Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

# Serializador para el modelo Proveedor
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'
