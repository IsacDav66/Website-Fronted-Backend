#--------------------------------------------------------------------------------------------------------------------------
#  *                                                      INFO
#    
#    Este archivo define la entidad asociada a la funcionalidad de contacto
#    
# 
#--------------------------------------------------------------------------------------------------------------------------


# src/entities/contactoEntity.py
import json

class ContactoEntity:
    def __init__(self, nombre=None, email=None, mensaje=None):
        self.nombre = nombre
        self.email = email
        self.mensaje = mensaje

    def to_dict(self):
        return {"nombre": self.nombre, "email": self.email, "mensaje": self.mensaje}

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
