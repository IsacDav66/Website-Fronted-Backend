#--------------------------------------------------------------------------------------------------------------------------
#  *                                                      INFO
#    
#    En este archivo, se define la clase LoginModel. Esta clase tiene un método estático llamado authenticate_user que toma un username y una password como parámetros y verifica si existe un usuario con esas credenciales en la base de datos. Se utiliza la conexión a la base de datos proveniente del módulo get_database_connection (asumido).
#    
# 
#--------------------------------------------------------------------------------------------------------------------------


from src.cn.data_base_connection import get_database_connection
from flask import current_app as app

class LoginModel:
    @staticmethod
    def authenticate_user(username, password):
        try:
            # Utiliza la conexión a la base de datos desde el módulo
            conn = get_database_connection(app)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()

            return user is not None
        except Exception as e:
            print(f"Error en la conexión a la base de datos: {str(e)}")
            return False
