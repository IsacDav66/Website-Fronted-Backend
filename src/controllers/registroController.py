#--------------------------------------------------------------------------------------------------------------------------
#  *                                                      INFO
#    
#    En este archivo, se define la clase RegistroController, que hereda de BaseController. La clase tiene un método llamado registro, que maneja la lógica del registro. En este método, se obtienen las credenciales del formulario, se crea una instancia de RegistroEntity y se utiliza el método register_user de RegistroModel para realizar el registro en la base de datos.
#    
# 
#--------------------------------------------------------------------------------------------------------------------------


# src/controllers/registroController.py
import re
from flask import redirect, request, render_template
from src.controllers.baseController import BaseController
from src.models.registroModel import RegistroModel
from src.entities.registroEntity import RegistroEntity

class RegistroController(BaseController):
    def __init__(self, app):
        prefix = '/registro'
        super().__init__(app, prefix)

        self.app.route('/registro', methods=['GET', 'POST'])(self.registro)
    
    def validate_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    def registro(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            # Validar la contraseña antes de intentar el registro
            if not self.validate_password(password):
                return "La contraseña no cumple con los requisitos. Intenta de nuevo."

            registro_entity = RegistroEntity(username=username, password=password, email=email)
            if RegistroModel.register_user(registro_entity.username, registro_entity.password, registro_entity.email):
                return redirect('/login')
            else:
                return "Error al registrar. Intenta de nuevo."

        return render_template('registro.html')
