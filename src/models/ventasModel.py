# src/models/ventasModel.py
from flask import current_app as app
from src.cn.data_base_connection import get_database_connection
from src.entities.ventasEntity import VentasEntity  # Asegúrate de importar la clase VentasEntity

# ventasModel.py

class VentasModel:
    @staticmethod
    def insert_venta(username, producto_id, cantidad, precio_total):
        try:
            # Utiliza la conexión a la base de datos desde el módulo
            conn = get_database_connection(app)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO ventas (username, producto_id, cantidad, precio_total, fecha_ventas)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            """, (username, producto_id, cantidad, precio_total))

            conn.commit()
            cursor.close()

            return True

        except Exception as e:
            print(f'Error al insertar en la base de datos: {str(e)}')
            return False

        finally:
            if conn is not None:
                conn.close()




    def get_productos_en_carrito(username):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM ventas WHERE username = %s
            """, (username,))

            productos_en_carrito = cursor.fetchall()

            # Convertir las tuplas a instancias de VentasEntity
            productos_en_carrito = [VentasEntity(*producto) for producto in productos_en_carrito]

            return productos_en_carrito

        except Exception as e:
            print(f'Error al obtener productos en el carrito: {str(e)}')
            return []

        finally:
            if conn is not None:
                conn.close()