from flask import Blueprint, render_template, session, redirect, url_for

class LogOutController:
    def __init__(self, app):
        self.blueprint = Blueprint('logout', __name__, url_prefix='/logout')

        @self.blueprint.route('/cerrar_sesion')
        def cerrar_sesion():
            session.clear()
            return redirect('/')  # Redirige a la página de inicio u otra página

    def get_blueprint(self):
        return self.blueprint
