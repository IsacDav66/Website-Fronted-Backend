# src/controllers/productosController.py
from flask import render_template, jsonify, request, flash
from src.controllers.baseController import BaseController
from src.models.productosModel import ProductoModel
from src.entities.productosEntity import ProductoEntity
from flask import flash, redirect, request, render_template, url_for, session
from src.entities.ventasEntity import VentasEntity
from src.models.ventasModel import VentasModel

class ProductosController(BaseController):
    def __init__(self, app):
        prefix = '/productos'
        super().__init__(app, prefix)
        self.productos_model = ProductoModel(self.app, "prefix")
        self.app.route('/productos', methods=['GET', 'POST'])(self.productos)
        self.app.route('/productos/<int:producto_id>')(self.get_productos_description)
        self.app.route('/productos/add', methods=['POST'])(self.add_producto)
        self.app.route('/productos/agregar_al_carrito/<int:producto_id>', methods=['POST'])(self.agregar_al_carrito)  # Agrega esta línea
        self.app.route('/carrito')(self.ver_carrito)
    def productos(self):
        try:
            if request.method == 'POST':
                nombre = request.form['nombre']
                descripcion = request.form['descripcion']
                precio = request.form['precio']
                imagen = request.form['imagen']
                # Crear una instancia de ProductoEntity
                producto_entity = ProductoEntity(nombre=nombre, descripcion=descripcion, precio=precio, imagen=imagen)

                # Usar ProductoModel para insertar en la base de datos
                if ProductoModel.insert_producto(producto_entity):
                    return 'Producto insertado correctamente'

            elif request.method == 'GET':
                # Obtener la lista de productos desde la base de datos
                productos_data = ProductoModel.get_productos()

                # Convertir cada diccionario a una instancia de ProductoEntity
                productos = [ProductoEntity(**producto) for producto in productos_data]

                username = session.get('username', None)
                if username is not None:
                    return render_template('productos.html', productos=productos, username=username)
                else:
                    flash('Debes iniciar sesión para ver los productos.', 'error')
                    return redirect(url_for('login'))  # Reemplaza 'login' con la ruta real de inicio de sesión

        except Exception as error:
            print(f'Error: {str(error)}')
            flash(f'Error: {str(error)}', 'error')
            return render_template('productos.html'), 500

        return render_template('productos.html')

    def get_productos_description(self, producto_id):
        producto_data = self.productos_model.get_producto_by_id(producto_id)

        if producto_data:
            producto_description = f"{producto_data[1]}, Descripción: {producto_data[2]}, Precio: {producto_data[3]}, Imagen: {producto_data[4]}"
        else:
            producto_description = "No se encontró el producto."

        return producto_description

    def add_producto(self):
        try:
            if request.method == 'POST':
                data = request.get_json()

                nombre = data.get('nombre')
                descripcion = data.get('descripcion')
                precio = data.get('precio')
                imagen = data.get('imagen')
                if nombre and descripcion and precio and imagen:
                    producto_id = self.productos_model.add_producto(nombre, descripcion, precio, imagen)
                    return jsonify({'id': producto_id, 'message': 'Producto agregado correctamente.'}), 201
                else:
                    return jsonify({'error': 'Se requieren el nombre y la descripción del Producto.'}), 400
        except Exception as error:
            print(f'Error: {str(error)}')
            flash(f'Error: {str(error)}', 'error')
            return jsonify({'error': str(error)}), 500
        
    def agregar_al_carrito(self, producto_id):
        try:
            if 'username' not in session:
                flash('Debes iniciar sesión para agregar productos al carrito.', 'error')
                return redirect(url_for('login'))

            username = session['username']
            producto_data = self.productos_model.get_producto_by_id(producto_id)
            producto_id = producto_data[0]

            if producto_data:
                cantidad = 1
                precio_total = cantidad * producto_data[3]

                venta_entity = VentasEntity(username=username, producto_id=producto_id,
                                            cantidad=cantidad, precio_total=precio_total, en_carrito=True)

                if VentasModel.insert_venta(**venta_entity.to_dict()):
                    flash('Producto agregado al carrito correctamente.', 'success')
                else:
                    flash('Error al agregar producto al carrito.', 'error')

        except Exception as error:
            print(f'Error: {str(error)}')
            flash(f'Error: {str(error)}', 'error')

        return redirect(url_for('ver_carrito'))
    
    def ver_carrito(self):
        try:
            if 'username' not in session:
                flash('Debes iniciar sesión para ver tu carrito.', 'error')
                return redirect(url_for('login'))  # Reemplaza 'login' con la ruta real de inicio de sesión

            username = session['username']

            # Obtener los productos en el carrito del usuario desde la base de datos
            productos_carrito = VentasModel.get_productos_en_carrito(username)

            return render_template('carrito.html', productos_carrito=productos_carrito)

        except Exception as error:
            print(f'Error: {str(error)}')
            flash(f'Error: {str(error)}', 'error')
            return redirect(url_for('carrito')), 500