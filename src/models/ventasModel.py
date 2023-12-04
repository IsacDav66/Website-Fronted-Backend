# src/models/ventasModel.py
from flask import current_app as app
from src.cn.data_base_connection import get_database_connection

class VentasModel:
    @staticmethod
    def insert_venta(username, producto_id, cantidad, precio_total, en_carrito=True):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO ventas (username, producto_id, cantidad, precio_total, en_carrito)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, producto_id, cantidad, precio_total, en_carrito))

            conn.commit()
            return True

        except Exception as e:
            print(f'Error al insertar venta en la base de datos: {str(e)}')
            return False

        finally:
            if conn is not None:
                conn.close()



    def get_productos_en_carrito(username):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            cursor.execute("""
            SELECT * FROM ventas WHERE username = %s AND en_carrito = true
            """, (username,))

            productos_en_carrito = cursor.fetchall()
            print("Productos en el carrito para el usuario", username, ":", productos_en_carrito)
            
            return productos_en_carrito

        except Exception as e:
            print(f'Error al obtener productos en el carrito: {str(e)}')
            return []

        finally:
            if conn is not None:
                conn.close()