# src/entities/productosEntity.py
import json

class ProductoEntity:
    def __init__(self, id=None, nombre=None, descripcion=None, precio=None, imagen=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.imagen = imagen

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "descripcion": self.descripcion, "precio": self.precio, "imagen": self.imagen}

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)