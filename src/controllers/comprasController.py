from flask import render_template
from src.controllers.baseController import BaseController

class ComprasController(BaseController):
    def __init__(self, app):
        prefix = '/compras'
        super().__init__(app, 'compras')
        
        self.app.route('/compras', methods=['GET', 'POST'])(self.compras)

    def compras(self):
        # tu lógica aquí
        return render_template('compras.html', datos='AlgunosDatos')
