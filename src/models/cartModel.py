# src/models/cartModel.py
from src.cn.data_base_connection import get_database_connection
from flask import current_app as app

class CartModel:
    @staticmethod
    def get_cart_id(username):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            # Buscar el cart_id para el usuario dado con is_purchased_cart en false
            cursor.execute("""
                SELECT cart_id FROM carts WHERE username = %s AND is_purchased_cart = false;
            """, (username,))

            cart_id_tuple = cursor.fetchone()

            cursor.close()

            # Si cart_id_tuple es None, significa que no se encontró un carrito no comprado para el usuario
            return cart_id_tuple[0] if cart_id_tuple else None

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

            # Insertar en la tabla carts con is_purchased en False
            cursor.execute("""
                INSERT INTO carts (username, is_purchased_cart)
                VALUES (%s, FALSE)
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


    @staticmethod
    def finalizar_compra(cart_id):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            # Actualizar is_purchased en la tabla carts
            cursor.execute("""
                UPDATE carts SET is_purchased_cart = true
                WHERE cart_id = %s;
            """, (cart_id,))

            conn.commit()
            print(f'Filas afectadas: {cursor.rowcount}')
            cursor.close()

        except Exception as e:
            print(f'Error al finalizar la compra: {str(e)}')

        finally:
            if conn is not None:
                conn.close()
                
    
    
    @staticmethod
    def is_cart_purchased(cart_id):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT is_purchased_cart
                FROM carts
                WHERE cart_id = %s AND is_purchased_cart = true;
            """, (cart_id,))

            is_purchased = cursor.fetchone()

            return is_purchased is not None and is_purchased[0]

        except Exception as e:
            print(f'Error al verificar si el carrito fue comprado: {str(e)}')
            return False

        finally:
            if conn is not None:
                conn.close()
