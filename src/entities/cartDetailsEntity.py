# src/entities/cartDetailsEntity.py
class cartDetailsEntity:
    def __init__(self, id, cart_id, product_id, quantity, total_price, username, is_pucharsed ):
        self.id = id
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price
        self.username = username
        self.is_pucharsed =is_pucharsed
    def to_dict(self):
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'total_price': self.total_price,
            'username': self.username,
            'is_pucharsed': self.is_pucharsed
        }