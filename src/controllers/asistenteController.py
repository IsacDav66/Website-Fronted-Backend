# src/controllers/asistenteController.py
from flask import render_template
from src.controllers.baseController import BaseController

class AsistenteController(BaseController):
    def __init__(self, app):
        prefix = '/asistente'
        super().__init__(app, 'asistente')
        
        self.app.route('/asistente', methods=['GET', 'POST'])(self.asistente)

    def asistente(self):
        # tu lógica aquí
        return render_template('asistente.html')
