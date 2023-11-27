#--------------------------------------------------------------------------------------------------------------------------
#  *                                                      INFO
#    
#    Ahora, en el modelo (comentarioModel.py), definimos la clase ComentarioModel que se encargará de interactuar con la base de datos para realizar operaciones relacionadas con los comentarios.
#    
# 
#--------------------------------------------------------------------------------------------------------------------------


from src.cn.data_base_connection import get_database_connection
from src.entities.comentarioEntity import ComentarioEntity
from flask import current_app as app
from src.controllers.baseController import BaseController

class ComentarioModel(BaseController):
    def __init__(self, app):
        app.config['MOMENT_TIMEZONE'] = 'America/Lima'
        prefix = '/comentarios'
        super().__init__(app, prefix)
        self.app.route('/agregar_comentario', methods=['POST'])(self.get_comentario) 
        
    @staticmethod
    def insert_comentario(usuario, comentario):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO comentarios (usuario, comentario, fecha) VALUES (%s, %s, NOW() AT TIME ZONE 'America/Lima')", (usuario, comentario))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error al insertar comentario: {str(e)}")
            return False

    @staticmethod
    def get_comentarios(self):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM comentarios ORDER BY fecha DESC")
            comentarios = cursor.fetchall()
            cursor.close()

            comentarios_list = []
            for comentario in comentarios:
                comentario_entity = ComentarioEntity(usuario=comentario[1], comentario=comentario[2], fecha=self.formatear_fecha(comentario[3]))
                comentarios_list.append(comentario_entity)

            return comentarios_list
        except Exception as e:
            print(f"Error al obtener comentarios: {str(e)}")
            return []
