from rest_framework import serializers
from .models import (
    Categoria, LineaProducto, Producto, Empresa, Sucursal,
    Pedido, DetallePedido, Promocion, CondicionPromocion,
    BeneficioPromocion, PromocionAplicada
)

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class LineaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaProducto
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'

class PromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocion
        fields = '__all__'

class CondicionPromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CondicionPromocion
        fields = '__all__'

class BeneficioPromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeneficioPromocion
        fields = '__all__'

class PromocionAplicadaSerializer(serializers.ModelSerializer):
    nombre_promocion = serializers.CharField(source='promocion.nombre', read_only=True)
    nombre_producto_bonificado = serializers.CharField(source='producto_bonificado.nombre', read_only=True)
    canal = serializers.CharField(source='promocion.canal', read_only=True)

    class Meta:
        model = PromocionAplicada
        fields = [
            'id',
            'pedido',
            'promocion',
            'nombre_promocion',
            'canal',
            'tipo_beneficio',
            'producto_bonificado',
            'nombre_producto_bonificado',
            'cantidad_bonificada',
            'porcentaje_descuento',
            'monto_descuento',
            'detalle_pedido'
        ]
    