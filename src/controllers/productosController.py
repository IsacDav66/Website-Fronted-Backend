# src/controllers/productosController.py
from flask import render_template, jsonify, request, flash
from src.controllers.baseController import BaseController
from src.models.productosModel import ProductoModel
from src.entities.productosEntity import ProductoEntity
from flask import flash, redirect, request, render_template, url_for, session
from src.entities.ventasEntity import VentasEntity
from src.models.ventasModel import VentasModel
from src.models.cartDetailsModel import CartDetailsModel  # Agregamos el modelo para el carrito
from src.models.cartModel import CartModel

class ProductosController(BaseController):
    def __init__(self, app):
        prefix = '/productos'
        super().__init__(app, prefix)
        self.productos_model = ProductoModel(self.app, "prefix")
        self.app.route('/productos', methods=['GET', 'POST'])(self.productos)
        self.app.route('/productos/<int:producto_id>')(self.get_productos_description)
        self.app.route('/productos/add', methods=['POST'])(self.add_producto)
        self.app.route('/productos/agregar_al_carrito/<int:producto_id>', methods=['POST'])(self.agregar_al_carrito)
        self.app.route('/carrito', methods=['GET', 'POST'])(self.ver_carrito)
        self.app.route('/total_productos')(self.calcular_total)
        self.totalU = 0 
        self.app.route('/productos/carrito_calculo/<int:producto_id>', methods=['GET', 'POST'])(self.carrito_calculo)
        self.app.route('/productos/comprar', methods=['POST'])(self.comprar)
        self.app.route('/historial_compras', methods=['GET', 'POST'])(self.finalizar_compra)

    #?Se usa para mostrar los productos en la pagina e insertar en postman
    def productos(self):
        try:
            #? Creo que se usa para insertar desde un formulario por ejmp
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
                    cart_id = CartModel.get_cart_id(username)
                    return render_template('productos.html', productos=productos, username=username, cart_id= cart_id)
                else:
                    flash('Debes iniciar sesión para ver los productos.', 'error')
                    return redirect(url_for('login'))  # Reemplaza 'login' con la ruta real de inicio de sesión

        except Exception as error:
            print(f'Error: {str(error)}')
            flash(f'Error: {str(error)}', 'error')
            return render_template('productos.html'), 500

        return render_template('productos.html')


    #? Se usa para llamada con Postman
    def get_productos_description(self, producto_id):
        producto_data = self.productos_model.get_producto_by_id(producto_id)

        if producto_data:
            producto_description = f"{producto_data[1]}, Descripción: {producto_data[2]}, Precio: {producto_data[3]}, Imagen: {producto_data[4]}"
        else:
            producto_description = "No se encontró el producto."

        return producto_description

    #? Se usa para agregar con Postman con ID
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
        
        
    
    
    def carrito_calculo(self, producto_id):
        cantidad = int(request.form.get('cantidad', 1))  # Obtener la cantidad del formulario
        producto_data = self.productos_model.get_producto_by_id(producto_id)
        
        total_producto_actual = cantidad * float(producto_data[3])
        self.totalU += total_producto_actual  # Acumula el total

        print("TOTAL ES IGUAL =", cantidad, producto_data, total_producto_actual)
        return redirect(url_for('productos'))  # Redirigir a la lista de productos
    
    def calcular_total(self):
        print(self.totalU)
        return jsonify({'Total': self.totalU}), 201
        
        
        
    ####--------------------------------------------------
    #? Usa CartModel (create_car)  - ProductoModel (get_producto_by_id)
    def agregar_al_carrito(self, producto_id):
        try:
            if 'username' not in session:
                flash('Debes iniciar sesión para agregar productos al carrito.', 'error')
                return redirect(url_for('login'))

            username = session['username']
            cantidad = int(request.form.get('cantidad', 1))

            # Verificar si el usuario ya tiene un carrito
            cart_id = CartModel.get_cart_id(username)

            # Si no tiene carrito o el carrito ya fue comprado, créalo
            if not cart_id or CartModel.is_cart_purchased(cart_id):
                cart_id = CartModel.create_cart(username)

            if cart_id:
                producto_data = self.productos_model.get_producto_by_id(producto_id)

                if producto_data:
                    precio_total = cantidad * producto_data[3]
                    CartDetailsModel.add_to_cart(cart_id, producto_id, cantidad, precio_total, username=username, is_purchased_cart=False)
                    flash('Producto agregado al carrito correctamente.', 'success')
                else:
                    flash('Error al obtener información del producto.', 'error')
            else:
                flash('Error al crear el carrito.', 'error')

        except Exception as error:
            print(f'Error: {str(error)}')
            flash(f'Error: {str(error)}', 'error')

        return redirect(url_for('productos'))

    
    
    def comprar(self):
        try:
            if 'username' not in session:
                flash('Debes iniciar sesión para realizar una compra.', 'error')
                return redirect(url_for('login'))  # Reemplaza 'login' con la ruta real de inicio de sesión

            username = session['username']

            # Obtener el cart_id del usuario
            cart_id = CartModel.get_cart_id(username)

            if cart_id:
                # Marcar el carrito como comprado
                CartDetailsModel.mark_cart_as_purchased(cart_id)

                flash('Compra realizada con éxito. ¡Gracias por tu compra!', 'success')
                return render_template('confirmacion_compra.html')

            else:
                flash('No hay productos en tu carrito para comprar.', 'error')

        except Exception as error:
            print(f'Error al realizar la compra: {str(error)}')
            flash(f'Error al realizar la compra: {str(error)}', 'error')

        return redirect(url_for('productos'))  # Redirigir a la lista de productos



    def ver_carrito(self):
        try:
            if 'username' not in session:
                flash('Debes iniciar sesión para ver tu carrito.', 'error')
                return redirect(url_for('login'))  # Reemplaza 'login' con la ruta real de inicio de sesión

            username = session['username']

            # Obtener el cart_id del usuario
            cart_id = CartModel.get_cart_id(username)

            if cart_id:
                # Obtener la suma de total_price para el carrito actual
                total_price_sum = CartDetailsModel.sum_total_price(cart_id)
                print("Total de la compra ->:", total_price_sum)

                # Obtener los productos en el carrito del usuario desde la base de datos
                productos_en_carrito = CartDetailsModel.get_productos_en_carrito(cart_id)

                return render_template('carrito.html', productos_en_carrito=productos_en_carrito, total_price_sum=total_price_sum, username=username, cart_id=cart_id)

            else:
                print("No hay productos")
                flash('No hay productos en tu carrito.', 'error')

        except Exception as error:
            print(f'Error: {str(error)}')
            flash(f'Error: {str(error)}', 'error')
            return redirect(url_for('carrito')), 500
        
        
        
    def finalizar_compra(self):
        try:
            username = session['username']

            # Obtener el cart_id del usuario
            cart_id = CartModel.get_cart_id(username)

            if cart_id:
                # Finalizar la compra actualizando is_purchased en la tabla carts
                CartModel.finalizar_compra(cart_id)

                flash('Compra finalizada correctamente.', 'success')

            else:
                flash('No hay productos en tu carrito.', 'error')

        except Exception as error:
            print(f'Error: {str(error)}')
            flash(f'Error: {str(error)}', 'error')

        return render_template('historial_compras.html',username=username)