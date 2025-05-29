from rest_framework import viewsets
from .models import (
    Categoria, LineaProducto, Producto, Empresa, Sucursal,
    Pedido, DetallePedido, Promocion, CondicionPromocion,
    BeneficioPromocion, PromocionAplicada
)
from .serializers import (
    CategoriaSerializer, LineaProductoSerializer, ProductoSerializer,
    EmpresaSerializer, SucursalSerializer, PedidoSerializer,
    DetallePedidoSerializer, PromocionSerializer, CondicionPromocionSerializer,
    BeneficioPromocionSerializer, PromocionAplicadaSerializer
)
from django_filters.rest_framework import DjangoFilterBackend

# Vistas generales CRUD

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class LineaProductoViewSet(viewsets.ModelViewSet):
    queryset = LineaProducto.objects.all()
    serializer_class = LineaProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

class PromocionViewSet(viewsets.ModelViewSet):
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer

class CondicionPromocionViewSet(viewsets.ModelViewSet):
    queryset = CondicionPromocion.objects.all()
    serializer_class = CondicionPromocionSerializer

class BeneficioPromocionViewSet(viewsets.ModelViewSet):
    queryset = BeneficioPromocion.objects.all()
    serializer_class = BeneficioPromocionSerializer

class PromocionAplicadaViewSet(viewsets.ModelViewSet):
    queryset = PromocionAplicada.objects.all()
    serializer_class = PromocionAplicadaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pedido']

# Motor de promociones
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .promocion_engine import obtener_promociones_aplicables

@api_view(['GET'])
def promociones_para_pedido(request, pedido_id):
    from .models import Pedido
    try:
        pedido = Pedido.objects.get(id=pedido_id)
    except Pedido.DoesNotExist:
        return Response({"error": "Pedido no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    promociones = obtener_promociones_aplicables(pedido)
    return Response(promociones)
