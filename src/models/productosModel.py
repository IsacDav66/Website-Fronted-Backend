# src/models/productosModel.py
from flask import Blueprint, redirect, render_template, session

from src.cn.data_base_connection import get_database_connection
from flask import current_app as app
from src.entities.cartDetailsEntity import cartDetailsEntity
class ProductoModel:
    def __init__(self, app, prefix):
        self.app = app
        self.prefix = prefix
        self.blueprint = Blueprint(self.prefix, __name__)
        
    
    #?Se usa para insertar en postman

    def insert_producto(entity):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO productos (nombre, descripcion, precio, imagen) VALUES (%s, %s, %s, %s)",
                           (entity.nombre, entity.descripcion, entity.precio, entity.imagen))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f'Error al insertar en la base de datos: {str(e)}')
            return False
        finally:
            if conn is not None:
                conn.close()
            pass

     #?Se usa para mostrar los productos en la pagina

    def get_productos():
        try:
            # Utiliza la conexión a la base de datos desde el módulo
            conn = get_database_connection(app)
            cursor = conn.cursor()

            cursor.execute("SELECT id, nombre, descripcion, precio, imagen FROM productos")
            productos = cursor.fetchall()

            return [{"id": id, "nombre": nombre, "descripcion": descripcion, "precio": precio, "imagen": imagen} for id, nombre, descripcion, precio, imagen in productos]

        except Exception as e:
            print(f'Error al obtener productos de la base de datos: {str(e)}')
            return []

        finally:
            if conn is not None:
                conn.close()
                
                
    #? Se usa para llamada con Postman
    def get_producto_by_id(self, producto_id):
        # Conéctate a la base de datos y realiza una consulta SQL
        connection = get_database_connection(self.app)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM productos WHERE id = %s;", (producto_id,))
        producto_data = cursor.fetchone()

        cursor.close()
        connection.close()

        print(f'Producto Data: {producto_data}')  # Agrega esta línea para verificar la salida
        return producto_data
    
    
    
    
    
    def add_producto(self, nombre, descripcion, precio, imagen):
        try:
            connection = get_database_connection(self.app)
            cursor = connection.cursor()

            # Insertar el nuevo Pokémon en la base de datos
            cursor.execute("INSERT INTO productos (nombre, descripcion, precio, imagen) VALUES (%s, %s, %s, %s) RETURNING id", (nombre, descripcion, precio, imagen))
            new_producto_id = cursor.fetchone()[0]

            connection.commit()
            return new_producto_id
        except Exception as e:
            print(f"Error al agregar el Producto a la base de datos: {e}")
            raise
        finally:
            cursor.close()
            connection.close()    