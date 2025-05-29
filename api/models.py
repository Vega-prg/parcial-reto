from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class LineaProducto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    linea_producto = models.ForeignKey(LineaProducto, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    CANAL_CHOICES = [
        ('Mayorista', 'Mayorista'),
        ('Cobertura', 'Cobertura'),
        ('Mercado', 'Mercado'),
        ('Institucionales', 'Institucionales'),
    ]

    fecha = models.DateField()
    hora = models.TimeField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True, blank=True)
    canal = models.CharField(max_length=20, choices=CANAL_CHOICES)
    total_bruto = models.DecimalField(max_digits=10, decimal_places=2)
    total_descuento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_final = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto}"


class Promocion(models.Model):
    TIPO_CHOICES = [
        ('Volumen_bonificacion', 'Volumen bonificación'),
        ('Volumen_descuento', 'Volumen descuento'),
        ('Monto_bonificacion', 'Monto bonificación'),
        ('Monto_descuento', 'Monto descuento'),
        ('Volumen_combinada', 'Volumen combinada'),
        ('Monto_Combinada', 'Monto combinada'),
        ('Combo', 'Combo'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('INACTIVA', 'Inactiva'),
    ]

    CANAL_CHOICES = Pedido.CANAL_CHOICES

    tipo = models.CharField(max_length=25, choices=TIPO_CHOICES)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    canal = models.CharField(max_length=20, choices=CANAL_CHOICES, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)

    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    linea_producto = models.ForeignKey(LineaProducto, on_delete=models.SET_NULL, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre or f"Promoción #{self.id}"


class CondicionPromocion(models.Model):
    TIPO_CHOICES = [
        ('NORMAL', 'Normal'),
        ('DOBLE', 'Doble'),
    ]

    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    monto_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cantidad_min = models.PositiveIntegerField(null=True, blank=True)

    producto_1 = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True, related_name='condicion_producto_1')
    producto_2 = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True, related_name='condicion_producto_2')

    def __str__(self):
        return f"Condición {self.tipo} - Promoción {self.promocion_id}"


class BeneficioPromocion(models.Model):
    TIPO_CHOICES = [
        ('DESCUENTO', 'Descuento'),
        ('BONIFICACION', 'Bonificación'),
    ]

    condicion = models.ForeignKey(CondicionPromocion, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField(null=True, blank=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Beneficio {self.tipo} - Condición {self.condicion_id}"


class PromocionAplicada(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    promocion = models.ForeignKey(Promocion, on_delete=models.SET_NULL, null=True, blank=True)
    detalle_pedido = models.ForeignKey(DetallePedido, on_delete=models.SET_NULL, null=True, blank=True)

    tipo_beneficio = models.CharField(
        max_length=15,
        choices=BeneficioPromocion.TIPO_CHOICES
    )

    producto_bonificado = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='producto_bonificado'
    )
    cantidad_bonificada = models.PositiveIntegerField(null=True, blank=True)
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    monto_descuento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Promoción '{self.promocion}' aplicada al Pedido #{self.pedido_id}"
