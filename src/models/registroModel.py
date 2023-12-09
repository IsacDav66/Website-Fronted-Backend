#---------------------------------------------------------------------------------------------------
#  *                                            INFO
#    
#    En este archivo, se define la clase RegistroModel. Esta clase tiene un método estático llamado register_user que toma un username y una password como parámetros y realiza la inserción en la base de datos.
#    
# 
#---------------------------------------------------------------------------------------------------


from src.cn.data_base_connection import get_database_connection
from flask import current_app as app


class RegistroModel:
    @staticmethod
    def register_user(username, password, email):
        try:
            connection = get_database_connection(app)
            cursor = connection.cursor()

            cursor.execute("INSERT INTO usuarios (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            connection.commit()
            print("Se registró correctamente")
            return True
        except Exception as e:
            print(f"Error al registrar en la base de datos: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
