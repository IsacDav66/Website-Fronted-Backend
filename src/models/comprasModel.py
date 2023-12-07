# src/models/comprasModel.py
from src.cn.data_base_connection import get_database_connection
from flask import current_app as app

class ComprasModel:
    @staticmethod
    def registrar_compra(username):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            # Realiza la lógica para registrar una compra en la base de datos
            cursor.execute("""
                INSERT INTO compras (username, fecha_compra) VALUES (%s, NOW())
                RETURNING id;
            """, (username,))

            compra_id = cursor.fetchone()[0]

            conn.commit()
            cursor.close()

            return compra_id

        except Exception as e:
            print(f'Error al registrar compra: {str(e)}')
            return None

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def registrar_producto_comprado(compra_id, producto_id, cantidad):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            # Realiza la lógica para registrar un producto comprado en la base de datos
            cursor.execute("""
                INSERT INTO productos_comprados (compra_id, producto_id, cantidad)
                VALUES (%s, %s, %s);
            """, (compra_id, producto_id, cantidad))

            conn.commit()
            cursor.close()

        except Exception as e:
            print(f'Error al registrar producto comprado: {str(e)}')

        finally:
            if conn is not None:
                conn.close()
