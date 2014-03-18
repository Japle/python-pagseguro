from flask_seguro import app
from flask_seguro.cart import make_cart
from flask import session, jsonify

products = [
        {"id": "0001", "description": "Produto 1", "amount": 354.20, "quantity": 2, "weight": 200},
        {"id": "0002", "description": "Produto 2", "amount": 50, "quantity": 1, "weight": 1000},
]

@app.route('/')
def index():
    return ''

@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart']=make_cart()

@app.route('/products/list')
def list_products():
    return jsonify({"product_list":products})


@app.route('/cart/add/<item_id>')
def add_to_cart(item_id):
    product=filter(lambda p:p['id']==item_id,products)
    if product!=[]:
        session['cart'].append(product[0])
        return 'success'
    else:
        return 'product not found'

@app.route('/cart/remove/<item_id>')
def remove_from_cart(item_id):
    product=filter(lambda p:p['id']==item_id,session['cart'])
    if product!=[]:
        session['cart'].remove(product[0])
        return 'success'
    else:
        return 'product not found'
