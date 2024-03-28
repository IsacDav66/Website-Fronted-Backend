#--------------------------------------------------------------------------------------------------------------------------
#  *                                                      INFO
#    
#    Finalmente, en el controlador (comentariosController.py), utilizaremos la entidad y el modelo para manejar la lógica de la aplicación.
#    
# 
#--------------------------------------------------------------------------------------------------------------------------


# src/controllers/comentariosController.py
from flask import flash, redirect, request, render_template, url_for, session
from src.controllers.baseController import BaseController
from src.models.comentarioModel import ComentarioModel
from src.entities.comentarioEntity import ComentarioEntity
from datetime import datetime

import pytz

class ComentariosController(BaseController):
    def __init__(self, app):
        prefix = '/comentarios'
        super().__init__(app, prefix)

        # Registro de rutas
        self.app.route('/comentarios', methods=['GET', 'POST'])(self.comentarios)

    def comentarios(self):
        try:
            if request.method == 'POST':
                usuario = session.get('username')
                comentario = request.form['comentario']

                if usuario:
                    if ComentarioModel.insert_comentario(usuario, comentario):
                        return redirect('/comentarios')
                    else:
                        flash("Error al insertar comentario. Intenta de nuevo.", "error")
                        return redirect(url_for('comentarios.comentarios'))
                else:
                    flash('Necesitas iniciar sesión para comentar.', 'info')
                    return redirect(url_for('login'))

            elif request.method == 'GET':
                comentarios_list = ComentarioModel.get_comentarios(self)
                username = session.get('username', None)
                return render_template('comentarios.html', username=username, comentarios=comentarios_list)

        except Exception as e:
            print(f"Error en la función 'comentarios': {str(e)}")
            flash(f"Error interno del servidor: {str(e)}", "error")
            return redirect(url_for('comentarios.comentarios'))
        
        
        
        
        
