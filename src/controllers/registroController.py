#--------------------------------------------------------------------------------------------------------------------------
#  *                                                      INFO
#    
#    En este archivo, se define la clase RegistroController, que hereda de BaseController. La clase tiene un método llamado registro, que maneja la lógica del registro. En este método, se obtienen las credenciales del formulario, se crea una instancia de RegistroEntity y se utiliza el método register_user de RegistroModel para realizar el registro en la base de datos.
#    
# 
#--------------------------------------------------------------------------------------------------------------------------


# src/controllers/registroController.py
from flask import redirect, request, render_template
from src.controllers.baseController import BaseController
from src.models.registroModel import RegistroModel
from src.entities.registroEntity import RegistroEntity

class RegistroController(BaseController):
    def __init__(self, app):
        prefix = '/registro'
        super().__init__(app, prefix)

        self.app.route('/registro', methods=['GET', 'POST'])(self.registro)
    
    def registro(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            registro_entity = RegistroEntity(username=username, password=password)
            if RegistroModel.register_user(registro_entity.username, registro_entity.password):
                return redirect('/login')
            else:
                return "Error al registrar. Intenta de nuevo."

        return render_template('registro.html')
