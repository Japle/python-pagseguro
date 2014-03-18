from flask_seguro import app
from flask_seguro.cart import make_cart
from flask import session

@app.route('/')
def index():
    return ''

@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart']='carrinho'
