#--------------------------------------------------------------------------------------------------------------------------
#  *                                                      INFO
#    
#    Este archivo define la entidad RegistroEntity, que representa la información asociada a un usuario que está registrándose. La entidad tiene dos atributos: username y password, que almacenan las credenciales del usuario.
#    
# 
#--------------------------------------------------------------------------------------------------------------------------


import json

class RegistroEntity:
    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email
        
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
