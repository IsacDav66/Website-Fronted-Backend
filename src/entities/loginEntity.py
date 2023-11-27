#--------------------------------------------------------------------------------------------------------------------------
#  *                                                      INFO
#    
#    Este archivo define la entidad LoginEntity, que representa la información asociada a un usuario que está intentando iniciar sesión. Esta entidad tiene dos atributos: username y password, que se utilizan para almacenar las credenciales del usuario. Además, la entidad tiene un método to_json para convertir la entidad a formato JSON.
#    
# 
#--------------------------------------------------------------------------------------------------------------------------


import json

class LoginEntity:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
