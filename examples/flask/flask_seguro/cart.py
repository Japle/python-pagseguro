from flask_seguro.products import Products
from flask import current_app as app


class Cart:
    def __init__(self, cart_dict=None):
        cart_dict = cart_dict or {}
        if cart_dict == {}:
            self.total = 0
            self.subtotal = 0
            self.items = []
        else:
            self.total = cart_dict["total"]
            self.subtotal = cart_dict["subtotal"]
            self.items = cart_dict["items"]
        self.extra_amount = float(app.config['EXTRA_AMOUNT'])

    def to_dict(self):
        return {
            "total": self.total,
            "subtotal": self.subtotal,
            "items": self.items,
            "extra_amount": self.extra_amount
        }

    def change_item(self, item_id, operation):
        product = Products().get_one(item_id)
        if product:
            if operation == 'add':
                self.items.append(product)
            elif operation == 'remove':
                cart_product = filter(
                    lambda x: x['id'] == product['id'], self.items)
                self.items.remove(cart_product[0])
            self.update()
            return True
        else:
            return False

    def update(self):
        subtotal = float(0)
        total = float(0)
        for product in self.items:
            subtotal += float(product["price"])
        if subtotal > 0:
            total = subtotal + self.extra_amount
        self.subtotal = subtotal
        self.total = total
