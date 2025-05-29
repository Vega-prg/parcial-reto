from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoriaViewSet, LineaProductoViewSet, ProductoViewSet,
    EmpresaViewSet, SucursalViewSet, PedidoViewSet, DetallePedidoViewSet,
    PromocionViewSet, CondicionPromocionViewSet, BeneficioPromocionViewSet,
    PromocionAplicadaViewSet, promociones_para_pedido
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'lineas', LineaProductoViewSet)
router.register(r'productos', ProductoViewSet)  
router.register(r'empresas', EmpresaViewSet)
router.register(r'sucursales', SucursalViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles', DetallePedidoViewSet)
router.register(r'promociones', PromocionViewSet)
router.register(r'condiciones', CondicionPromocionViewSet)
router.register(r'beneficios', BeneficioPromocionViewSet)
router.register(r'aplicadas', PromocionAplicadaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/evaluar_promociones/<int:pedido_id>/', promociones_para_pedido),
]
