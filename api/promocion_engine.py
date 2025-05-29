# api/promocion_engine.py
from datetime import date
from django.db.models import Q
from .models import (
    Pedido, DetallePedido, Promocion, CondicionPromocion,
    BeneficioPromocion, PromocionAplicada
)

def obtener_promociones_aplicables(pedido):
    fecha_referencia = pedido.fecha
    promociones_aplicadas = []

    PromocionAplicada.objects.filter(pedido=pedido).delete()

    promociones = Promocion.objects.filter(
        Q(empresa=pedido.empresa) | Q(empresa__isnull=True),
        Q(sucursal=pedido.sucursal) | Q(sucursal__isnull=True),
        Q(canal=pedido.canal) | Q(canal__isnull=True),
        fecha_inicio__lte=fecha_referencia,
        fecha_fin__gte=fecha_referencia,
        estado='ACTIVA'
    )

    detalles = DetallePedido.objects.filter(pedido=pedido)

    for promo in promociones:
        condiciones = CondicionPromocion.objects.filter(promocion=promo)

        mejor_descuento = None
        mejor_bonificacion = None
        max_descuento = 0
        max_bonificacion = 0
        cantidad_total = 0
        monto_total = 0

        for item in detalles:
            producto = item.producto
            if promo.producto and producto == promo.producto:
                cantidad_total += item.cantidad
                monto_total += item.subtotal
            elif promo.categoria and producto.categoria == promo.categoria:
                cantidad_total += item.cantidad
                monto_total += item.subtotal
            elif promo.linea_producto and producto.linea_producto == promo.linea_producto:
                cantidad_total += item.cantidad
                monto_total += item.subtotal
            elif not promo.producto and not promo.categoria and not promo.linea_producto:
                cantidad_total += item.cantidad
                monto_total += item.subtotal

        productos_en_pedido = set(item.producto.id for item in detalles)

        for condicion in condiciones:
            cumple = False
            es_combinada = condicion.tipo == 'DOBLE'

            if es_combinada:
                if condicion.producto_1 and condicion.producto_2:
                    if condicion.producto_1.id in productos_en_pedido and condicion.producto_2.id in productos_en_pedido:
                        cumple = True
            else:
                if condicion.monto_min and monto_total >= condicion.monto_min:
                    cumple = True
                if condicion.cantidad_min and cantidad_total >= condicion.cantidad_min:
                    cumple = True

            if cumple:
                beneficios = list(BeneficioPromocion.objects.filter(condicion=condicion))

                for beneficio in beneficios:
                    if beneficio.tipo == 'DESCUENTO' and beneficio.porcentaje:
                        if beneficio.porcentaje > max_descuento:
                            mejor_descuento = beneficio
                            max_descuento = beneficio.porcentaje
                    elif beneficio.tipo == 'BONIFICACION' and beneficio.cantidad:
                        if beneficio.cantidad > max_bonificacion:
                            mejor_bonificacion = beneficio
                            max_bonificacion = beneficio.cantidad
                            mejor_condicion_bonificacion = condicion

        if mejor_descuento:
            PromocionAplicada.objects.create(
                pedido=pedido,
                promocion=mejor_descuento.condicion.promocion,
                detalle_pedido=None,
                tipo_beneficio=mejor_descuento.tipo,
                producto_bonificado=None,
                cantidad_bonificada=None,
                porcentaje_descuento=mejor_descuento.porcentaje,
                monto_descuento=None
            )

            promociones_aplicadas.append({
                "promocion_id": mejor_descuento.condicion.promocion.id,
                "nombre": mejor_descuento.condicion.promocion.nombre,
                "tipo": mejor_descuento.tipo,
                "producto_bonificado": None,
                "cantidad_bonificada": None,
                "porcentaje_descuento": mejor_descuento.porcentaje
            })

        if mejor_bonificacion:
            veces = 1
            if mejor_condicion_bonificacion.cantidad_min and mejor_condicion_bonificacion.cantidad_min > 0:
                veces = cantidad_total // mejor_condicion_bonificacion.cantidad_min
            if mejor_condicion_bonificacion.monto_min and mejor_condicion_bonificacion.monto_min > 0:
                veces = monto_total // mejor_condicion_bonificacion.monto_min

            for _ in range(int(veces)):
                PromocionAplicada.objects.create(
                    pedido=pedido,
                    promocion=mejor_bonificacion.condicion.promocion,
                    detalle_pedido=None,
                    tipo_beneficio=mejor_bonificacion.tipo,
                    producto_bonificado=mejor_bonificacion.producto,
                    cantidad_bonificada=mejor_bonificacion.cantidad,
                    porcentaje_descuento=None,
                    monto_descuento=None
                )

                promociones_aplicadas.append({
                    "promocion_id": mejor_bonificacion.condicion.promocion.id,
                    "nombre": mejor_bonificacion.condicion.promocion.nombre,
                    "tipo": mejor_bonificacion.tipo,
                    "producto_bonificado": mejor_bonificacion.producto.nombre if mejor_bonificacion.producto else None,
                    "cantidad_bonificada": mejor_bonificacion.cantidad,
                    "porcentaje_descuento": None
                })

    return promociones_aplicadas
