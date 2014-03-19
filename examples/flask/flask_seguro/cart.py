from flask_seguro.products import Products
from flask import current_app as app


class Cart:

    def __init__(self, cart_dict={}):
        if cart_dict == {}:
            self.total = 0
            self.subtotal = 0
            self.items = []
        else:
            self.total = cart_dict["total"]
            self.subtotal = cart_dict["subtotal"]
            self.items = cart_dict["items"]

    def to_dict(self):
        return {"total": self.total,
                "subtotal": self.subtotal,
                "items": self.items}

    def change_item(self, item_id, operation):
        product = Products().get_one(item_id)
        if product:
            if operation == 'add':
                self.items.append(product)
            elif operation == 'remove':
                self.items.remove(product)
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
            total = subtotal + float(app.config['EXTRA_AMOUNT'])
        self.subtotal = subtotal
        self.total = total
