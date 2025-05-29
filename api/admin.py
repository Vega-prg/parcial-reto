from django.contrib import admin
from .models import (
    Categoria, LineaProducto, Producto,
    Empresa, Sucursal, Pedido, DetallePedido,
    Promocion, CondicionPromocion, BeneficioPromocion
)

admin.site.register(Categoria)
admin.site.register(LineaProducto)
admin.site.register(Producto)
admin.site.register(Empresa)
admin.site.register(Sucursal)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Promocion)
admin.site.register(CondicionPromocion)
admin.site.register(BeneficioPromocion)
