# src/models/cartDetailsModel.py
from flask import current_app as app
from src.cn.data_base_connection import get_database_connection
from src.entities.cartDetailsEntity import cartDetailsEntity  # Asegúrate de importar la clase VentasEntity

class CartDetailsModel:
    @staticmethod
    def get_cart_details_by_user(username):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            cursor.execute("""
            SELECT cart_details.*, productos.nombre, productos.precio
            FROM cart_details
            JOIN productos ON cart_details.product_id = productos.id
            WHERE cart_details.username = %s
            """, (username,))

            cart_details = cursor.fetchall()

            return cart_details

        except Exception as e:
            print(f'Error al obtener detalles del carrito: {str(e)}')
            return []

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def create_cart_for_user(username):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO carts (username) VALUES (%s)", (username,))
            conn.commit()

        except Exception as e:
            print(f'Error al crear carrito para el usuario: {str(e)}')

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def add_to_cart(cart_id, product_id, quantity, total_price, username, is_purchased_cart):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO cart_details (cart_id, product_id, quantity, total_price, username, is_purchased_cart)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (cart_id, product_id, quantity, total_price, username, is_purchased_cart))

            conn.commit()
            cursor.close()

            return True

        except Exception as e:
            print(f'Error al agregar al carrito: {str(e)}')
            return False

        finally:
            if conn is not None:
                conn.close()
                
                
                
                
    def get_productos_en_carrito(cart_id):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT cd.id, cd.cart_id, cd.product_id, cd.quantity, cd.total_price, cd.username, cd.is_purchased_cart, p.nombre, p.imagen
                FROM cart_details cd
                JOIN productos p ON cd.product_id = p.id
                WHERE cd.cart_id = %s;
            """, (cart_id,))

            productos_en_carrito = cursor.fetchall()

            # Convertir las tuplas a instancias de VentasEntity
            productos_en_carrito = [cartDetailsEntity(*cart_details) for cart_details in productos_en_carrito]

            return productos_en_carrito

        except Exception as e:
            print(f'Error al obtener productos en el carrito: {str(e)}')
            return []

        finally:
            if conn is not None:
                conn.close()
                    
                
                
        # ... (otro código en CartDetailsModel)




        # En src/models/cartDetailsModel.py
    def mark_cart_as_purchased(cart_id):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            # Actualizar is_purchased a True para todos los productos en el carrito
            cursor.execute("""
                UPDATE cart_details
                SET is_purchased = TRUE
                WHERE cart_id = %s;
            """, (cart_id,))

            conn.commit()
            cursor.close()

        except Exception as e:
            print(f'Error al marcar el carrito como comprado: {str(e)}')

        finally:
            if conn is not None:
                conn.close()
                
                
    def sum_total_price(cart_id):
        try:
            conn = get_database_connection(app)
            cursor = conn.cursor()

            # Obtener la suma de total_price para un carrito específico
            cursor.execute("""
                SELECT SUM(total_price) FROM cart_details
                WHERE cart_id = %s;
            """, (cart_id,))

            total_price_sum = cursor.fetchone()[0]

            # Actualizar total_price en la tabla carts
            cursor.execute("""
                UPDATE carts SET total_price = %s
                WHERE cart_id = %s;
            """, (total_price_sum, cart_id))

            conn.commit()
            cursor.close()

            return total_price_sum

        except Exception as e:
            print(f'Error al obtener la suma de total_price: {str(e)}')
            return None

        finally:
            if conn is not None:
                conn.close()