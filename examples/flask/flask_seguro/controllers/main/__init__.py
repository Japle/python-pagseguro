# -*- coding: utf-8 -*-
""" Main Controllers """
from flask import session
from flask import jsonify
from flask import request
from flask import redirect
from flask import render_template
from flask import current_app as app

from pagseguro import PagSeguro
from flask_seguro.products import Products
from flask_seguro.cart import Cart
from .views import main


@main.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = Cart().to_dict()


@main.route('/')
def index():
    """ Index Route """
    return list_products()


@main.route('/cart')
def cart():
    """ Cart Route """
    return render_template('cart.jinja2', cart=session['cart'])


@main.route('/products/list')
def list_products():
    """ Product list """
    products = Products().get_all()
    return render_template('products.jinja2',
                           products=products,
                           cart=session['cart'])


@main.route('/cart/add/<item_id>')
def add_to_cart(item_id):
    """ Cart with Product """
    cart = Cart(session['cart'])
    if cart.change_item(item_id, 'add'):
        session['cart'] = cart.to_dict()
    return list_products()


@main.route('/cart/remove/<item_id>')
def remove_from_cart(item_id):
    cart = Cart(session['cart'])
    if cart.change_item(item_id, 'remove'):
        session['cart'] = cart.to_dict()
    return list_products()


@main.route('/notification')
def notification_view(request):
    notification_code = request.POST['notificationCode']
    pg = PagSeguro(email=app.config['EMAIL'], token=app.config['TOKEN'])
    pg.check_notification(notification_code)
    # use the return of the function above to update the order


@main.route('/checkout', methods=['GET'])
def checkout_get():
    return render_template('checkout.jinja2')


@main.route('/checkout', methods=['POST'])
def checkout_post():
    for field in ['name', 'email', 'street', 'number', 'complement',
                  'district', 'postal_code', 'city', 'state']:
        if not request.form.get(field, False):
            return jsonify({'error_msg': 'Todos os campos são obrigatórios.'})
    cart = Cart(session['cart'])
    if len(cart.items) == 0:
        return jsonify({'error_msg': 'Seu carrinho está vazio.'})
    sender = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
    }
    shipping = {
        "street": request.form.get("street"),
        "number": request.form.get("number"),
        "complement": request.form.get("complement"),
        "district": request.form.get("district"),
        "postal_code": request.form.get("postal_code"),
        "city": request.form.get("city"),
        "state": request.form.get("state"),
        "country": 'BRA'
    }
    pagseguro = checkout_pg(sender, shipping, cart)
    response = pagseguro.checkout()
    return redirect(response.payment_url)


def checkout_pg(sender, shipping, cart):
    pagseguro = PagSeguro(email=app.config['EMAIL'], token=app.config['TOKEN'])
    pagseguro.sender = sender
    shipping['type'] = pagseguro.SEDEX
    pagseguro.shipping = shipping
    pagseguro.extra_amount = "%.2f" % float(app.config['EXTRA_AMOUNT'])
    pagseguro.redirect_url = app.config['REDIRECT_URL']
    pagseguro.notification_url = app.config['NOTIFICATION_URL']
    pagseguro.items = cart.items
    for item in cart.items:
        item['amount'] = "%.2f" % float(app.config['EXTRA_AMOUNT'])
    return pagseguro
