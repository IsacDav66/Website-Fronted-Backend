# src/controllers/nosotrosController.py
from flask import render_template
from src.controllers.baseController import BaseController

class NosotrosController(BaseController):
    def __init__(self, app):
        prefix = '/nosotros'
        super().__init__(app, 'nosotros')
        
        self.app.route('/nosotros', methods=['GET', 'POST'])(self.nosotros)

    def nosotros(self):
        # tu lógica aquí
        return render_template('nosotros.html', datos='AlgunosDatos')
