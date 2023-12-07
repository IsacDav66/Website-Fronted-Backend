# src/controllers/carritoController.py
from flask import render_template, flash, redirect, url_for, session
from src.controllers.baseController import BaseController
from src.models.ventasModel import VentasModel
from src.models.comprasModel import ComprasModel

class CarritoController(BaseController):
    def __init__(self, app):
        prefix = '/carrito'
        super().__init__(app, prefix)
        self.ventas_model = VentasModel(self.app, "prefix")
        self.compras_model = ComprasModel(self.app, "prefix")
        self.app.route('/carrito', methods=['GET'])(self.ver_carrito)
        self.app.route('/carrito/comprar', methods=['POST'])(self.comprar)

    def ver_carrito(self):
        try:
            if 'username' not in session:
                flash('Debes iniciar sesión para ver tu carrito.', 'error')
                return redirect(url_for('login'))  # Reemplaza 'login' con la ruta real de inicio de sesión

            username = session['username']

            # Obtener los productos en el carrito del usuario desde la base de datos
            productos_carrito = self.ventas_model.get_productos_en_carrito(username)

            return render_template('carrito.html', productos_carrito=productos_carrito)

        except Exception as error:
            print(f'Error: {str(error)}')
            flash(f'Error: {str(error)}', 'error')
            return redirect(url_for('carrito')), 500

    def comprar(self):
        try:
            if 'username' not in session:
                flash('Debes iniciar sesión para comprar.', 'error')
                return redirect(url_for('login'))  # Reemplaza 'login' con la ruta real de inicio de sesión

            username = session['username']

            # Obtener los productos en el carrito del usuario desde la base de datos
            productos_carrito = self.ventas_model.get_productos_en_carrito(username)

            if productos_carrito:
                # Registrar la compra en la tabla de compras
                compra_id = self.compras_model.registrar_compra(username)

                # Mover los productos comprados de la tabla de ventas a la tabla de compras
                for producto in productos_carrito:
                    self.compras_model.registrar_producto_comprado(compra_id, producto)

                # Eliminar los productos comprados del carrito del usuario
                self.ventas_model.eliminar_productos_comprados(username)

                flash('Compra realizada correctamente.', 'success')
            else:
                flash('El carrito está vacío. Agrega productos antes de comprar.', 'warning')

        except Exception as error:
            print(f'Error: {str(error)}')
            flash(f'Error: {str(error)}', 'error')

        return redirect(url_for('carrito'))
