# src/controllers/baseController.py
from flask import Blueprint, redirect, render_template, session
from datetime import datetime, timedelta

class BaseController:
    def __init__(self, app, prefix):
        self.app = app
        self.prefix = prefix
        self.blueprint = Blueprint(self.prefix, __name__)

        # Añadir funciones comunes
        self.blueprint.before_request(self.before_request)

    def route(self, rule, **options):
        def decorator(f):
            self.blueprint.route(rule, **options)(f)
            return f
        return decorator

    def get_blueprint(self):
        return self.blueprint

    def before_request(self):
        # Función que se ejecuta antes de cada solicitud
        # Puedes poner aquí lógica común para todos los controladores, por ejemplo, verificar la sesión del usuario
        pass

    def formatear_fecha(self, fecha):
        fecha_actual = datetime.now()

        if fecha_actual.date() == fecha.date():
            return f'Hoy a las {fecha.strftime("%H:%M")}'
        elif fecha_actual.date() - timedelta(days=1) == fecha.date():
            return f'Ayer a las {fecha.strftime("%H:%M")}'
        else:
            return fecha.strftime("%d/%m/%Y %H:%M")
        
   
    
    def get_app(self):
        return self.app

