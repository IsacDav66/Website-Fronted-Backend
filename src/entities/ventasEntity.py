# src/entities/ventasEntity.py
class VentasEntity:
    def __init__(self, venta_id, username, producto_id, cantidad, precio_total, fecha_ventas, ):
        self.venta_id = venta_id
        self.username = username
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_total = precio_total
        self.fecha_ventas = fecha_ventas
    def to_dict(self):
        return {
            'venta_id': self.venta_id,
            'username': self.username,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'precio_total': self.precio_total,
            'fecha_ventas': self.fecha_ventas,
        }