#--------------------------------------------------------------------------------------------------------------------------
#  *                                                      INFO
#    
#    En este archivo definiremos la entidad ComentarioEntity que representa la información asociada a un comentario. La entidad tiene tres atributos: usuario, comentario y fecha.
#    
# 
#--------------------------------------------------------------------------------------------------------------------------


import json

class ComentarioEntity:
    def __init__(self, usuario=None, comentario=None, fecha=None):
        self.usuario = usuario
        self.comentario = comentario
        self.fecha = fecha

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
