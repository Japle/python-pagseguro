""" The file is responsable for cart in flask-webpage """

from flask import current_app as app
from flask_seguro.products import Products


class Cart(object):
    """ The classe is responsable for cart in webpage """

    def __init__(self, cart_dict=None):
        """ Initializing class """

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
        """ Attribute values to dict """

        return {
            "total": self.total,
            "subtotal": self.subtotal,
            "items": self.items,
            "extra_amount": self.extra_amount
        }

    def change_item(self, item_id, operation):
        """ Remove items in cart """

        product = Products().get_one(item_id)
        if product:
            if operation == 'add':
                self.items.append(product)
            elif operation == 'remove':
                cart_p = [x for x in self.items if x['id'] == product['id']]
                self.items.remove(cart_p[0])
            self.update()
            return True
        else:
            return False

    def update(self):
        """ Remove items in cart """

        subtotal = float(0)
        total = float(0)
        for product in self.items:
            subtotal += float(product["price"])
        if subtotal > 0:
            total = subtotal + self.extra_amount
        self.subtotal = subtotal
        self.total = total
