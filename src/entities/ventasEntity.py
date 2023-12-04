# src/entities/ventasEntity.py
class VentasEntity:
    def __init__(self, username, producto_id, cantidad, precio_total, en_carrito=True):
        self.username = username
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_total = precio_total
        self.en_carrito = en_carrito  # Agrega esta línea

    def to_dict(self):
        return {
            'username': self.username,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'precio_total': self.precio_total,
            'en_carrito': self.en_carrito  # Agrega esta línea
        }