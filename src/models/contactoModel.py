#--------------------------------------------------------------------------------------------------------------------------
#  *                                                      INFO
#    
#    Este archivo define el modelo asociado a la funcionalidad de contacto
#    
# 
#--------------------------------------------------------------------------------------------------------------------------


# src/models/contactoModel.py
from src.cn.data_base_connection import get_database_connection
from flask import current_app as app

class ContactoModel:
    @staticmethod
    def insert_contacto(entity):
        try:
            # Utiliza la conexión a la base de datos desde el módulo
            conn = get_database_connection(app)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO contacto (nombre, email, mensaje) VALUES (%s, %s, %s)",
                           (entity.nombre, entity.email, entity.mensaje))

            conn.commit()
            cursor.close()

            return True

        except Exception as e:
            print(f'Error al insertar en la base de datos: {str(e)}')
            return False

        finally:
            if conn is not None:
                conn.close()

    # Otros métodos del modelo si es necesario
