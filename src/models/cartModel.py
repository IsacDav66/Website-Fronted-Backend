# src/models/cartModel.py
from src.cn.data_base_connection import get_database_connection
from flask import current_app as app

class CartModel:
    @staticmethod
    def get_cart_id(username):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            # Buscar el cart_id para el usuario dado
            cursor.execute("""
                SELECT cart_id FROM carts WHERE username = %s;
            """, (username,))

            cart_id = cursor.fetchone()

            cursor.close()
            return cart_id

        except Exception as e:
            print(f'Error al obtener el cart_id: {str(e)}')
            return None

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def create_cart(username):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            # Insertar en la tabla carts
            cursor.execute("""
                INSERT INTO carts (username)
                VALUES (%s)
                RETURNING cart_id;
            """, (username,))

            cart_id = cursor.fetchone()[0]

            conn.commit()
            cursor.close()

            return cart_id

        except Exception as e:
            print(f'Error al crear el carrito: {str(e)}')
            return None

        finally:
            if conn is not None:
                conn.close()
