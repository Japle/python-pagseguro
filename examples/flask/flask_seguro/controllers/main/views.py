# -*- coding: utf-8 -*-

from flask import session
from flask import jsonify
from flask import request
from flask import redirect
from flask import render_template
from flask import current_app as app

from . import main
from pagseguro import PagSeguro
from ...cart import Cart
from ...products import Products

@main.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = Cart().to_dict()

@main.route('/')
def index():
    return list_products()


@main.route('/cart')
def cart():
    return render_template('cart.jinja2', cart=session['cart'])


@main.route('/products/list')
def list_products():
    products = Products().get_all()
    return render_template('products.jinja2',
                           products=products,
                           cart=session['cart'])


@main.route('/cart/add/<item_id>')
def add_to_cart(item_id):
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
    if not len(cart.items):
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
    pg = checkout_pg(sender, shipping, cart)
    response = pg.checkout()
    return redirect(response.payment_url)

def checkout_pg(sender, shipping, cart):
    pg = PagSeguro(email=app.config['EMAIL'], token=app.config['TOKEN'])
    pg.sender = sender
    shipping['type'] = pg.SEDEX
    pg.shipping = shipping
    pg.extra_amount = "%.2f" % float(app.config['EXTRA_AMOUNT'])
    pg.redirect_url = app.config['REDIRECT_URL']
    pg.notification_url = app.config['NOTIFICATION_URL']
    pg.items = cart.items
    for item in cart.items:
        item['amount'] = "%.2f" % float(app.config['EXTRA_AMOUNT'])
    return pg