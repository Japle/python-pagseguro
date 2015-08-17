class Products:
    def __init__(self):
        self.products = [
            {
                "id": "0001",
                "description": "Produto 1",
                "amount": 1.00,
                "quantity": 1,
                "weight": 200,
                "price": 10.10
            },
            {
                "id": "0002",
                "description": "Produto 2",
                "amount": 50,
                "quantity": 1,
                "weight": 1000,
                "price": 10.50
            },
        ]

    def get_all(self):
        return self.products

    def get_one(self, item_id):
        p = filter(lambda p: p['id'] == item_id, self.products)
        if len(p) > 0:
            return p[0]
        else:
            return False
