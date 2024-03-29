#--------------------------------------------------------------------------------------------------------------------------
#  *                                                      INFO
#    
#    En este archivo, se define la clase LoginController, que hereda de BaseController. Esta clase tiene un método llamado login, que maneja la lógica del inicio de sesión. En este método, se obtienen las credenciales del formulario, se crea una instancia de LoginEntity y se utiliza el método authenticate_user de LoginModel para verificar si las credenciales son válidas.
#    
# 
#--------------------------------------------------------------------------------------------------------------------------


# src/controllers/loginController.py
from flask import redirect, request, render_template, session
from src.controllers.baseController import BaseController
from src.models.loginModel import LoginModel
from src.entities.loginEntity import LoginEntity

class LoginController(BaseController):
    def __init__(self, app):
        # Define el prefijo para este controlador, por ejemplo, '/login'
        prefix = '/login'
        super().__init__(app, prefix)
        # Configuración de la ruta
        self.app.route('/login', methods=['GET', 'POST'])(self.login)

    def login(self):
        # Lógica del login
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            login_entity = LoginEntity(username=username, password=password)
            if LoginModel.authenticate_user(login_entity.username, login_entity.password):
                session['username'] = username
                return redirect('/index')
            else:
                error_message = "Credenciales incorrectas. Intenta de nuevo."
                return render_template('login.html', error_message=error_message)

        return render_template('login.html')
