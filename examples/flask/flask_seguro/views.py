# -*- coding: utf-8 -*-
from flask_seguro import app
from flask_seguro.cart import Cart
from flask_seguro.products import Products
from flask import session
from flask import jsonify
from flask import request
from flask import redirect
from flask import render_template
from pagseguro import PagSeguro


@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = Cart().to_dict()


@app.route('/')
def index():
    return render_template('base.jinja2')


@app.route('/products/list')
def list_products():
    return jsonify({"product_list": Products().get_all()})


@app.route('/cart/add/<item_id>')
def add_to_cart(item_id):
    cart = Cart(session['cart'])
    if cart.change_item(item_id, 'add'):
        session['cart'] = cart.to_dict()
        return jsonify(cart.to_dict())
    else:
        return jsonify({'error_msg': 'Failure.'})


@app.route('/cart/remove/<item_id>')
def remove_from_cart(item_id):
    cart = Cart(session['cart'])
    if cart.change_item(item_id, 'remove'):
        session['cart'] = cart.to_dict()
        return jsonify(cart.to_dict())
    else:
        return jsonify({'error_msg': 'Failure.'})


@app.route('/checkout', methods=['POST'])
def checkout_view():
    email = request.form.get("email")
    if not email or not email.strip():
        return jsonify({'error_msg': 'Email inválido.'})
    cart = Cart(session['cart'])
    if not len(cart.items):
        return jsonify({'error_msg': 'Seu carrinho está vazio.'})
    sender = {
        #"name": "Bruno Rocha",
        #"area_code": 11,
        #"phone": 981001213,
        "email": email,
    }
    shipping = {
        #"type": pg.SEDEX,
        "street": "Av Brig Faria Lima",
        "number": 1234,
        "complement": "5 andar",
        "district": "Jardim Paulistano",
        "postal_code": "06650030",
        "city": "Sao Paulo",
        "state": "SP",
        "country": "BRA"
    }
    pg = checkout_pg(sender, shipping)
    response = pg.checkout()
    return redirect(response.payment_url)


@app.route('/notification')
def notification_view(request):
    notification_code = request.POST['notificationCode']
    pg = PagSeguro(email=app.config['EMAIL'], token=app.config['TOKEN'])
    notification_data = pg.check_notification(notification_code)
    #save notification_data


def checkout_pg(sender, shipping):
    pg = PagSeguro(email=app.config['EMAIL'], token=app.config['TOKEN'])
    pg.sender = sender
    pg.shipping = shipping
    pg.extra_amount = app.config['EXTRA_AMOUNT']
    pg.redirect_url = app.config['REDIRECT_URL']
    pg.notification_url = app.config['NOTIFICATION_URL']
    return pg
