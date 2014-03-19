#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import flask_seguro
import unittest
import tempfile
import flask
from flask import json
from flask_seguro.cart import Cart


class TestConfig(object):
    EXTRA_AMOUNT = 12.70
    REDIRECT_URL = "http://meusite.com/obrigado"
    NOTIFICATION_URL = "http://meusite.com/notification"
    EMAIL = "seuemail@dominio.com"
    TOKEN = "ABCDEFGHIJKLMNO"


class FlasKSeguroTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flask_seguro.app.config['DATABASE'] = tempfile.mkstemp()
        flask_seguro.app.config.from_object(TestConfig())
        flask_seguro.app.config['TESTING'] = True
        self.app = flask_seguro.app.test_client()
        # flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flask_seguro.app.config['DATABASE'])

    def list_products(self):
        response = self.app.get('/products/list')
        products = json.loads(response.data)
        assert 'product_list' in products
        assert len(products['product_list']) > 0
        products = products['product_list']
        return products

    def check_cart_fields(self, response):
        cart = json.loads(response.data)
        assert 'error_msg' not in cart
        assert 'total' in cart
        assert 'subtotal' in cart
        return cart

    def testRetrieveCartAndAddRemoveItem(self):
        with flask_seguro.app.test_client() as c:
            response = c.get('/')
            session = flask.session
            assert 'cart' in session
            assert len(session['cart']['items']) == 0

            products = self.list_products()

            response = c.get('/cart/add/%s' % (products[0]['id']))
            assert len(session['cart']['items']) == 1
            cart = self.check_cart_fields(response)
            assert float(cart['subtotal']) == float(products[0]['price'])

            response = c.get('/cart/remove/%s' % (products[0]['id']))
            assert len(session['cart']['items']) == 0
            cart = self.check_cart_fields(response)
            assert float(cart['total']) == float(cart['subtotal']) == float(0)

    def checkout(self, email, c, decode_json=True):
        response = c.post('/checkout', data={"email": email})
        if decode_json:
            response = json.loads(response.data)
        return response

    def test_checkout(self):
        with flask_seguro.app.test_client() as c:
            response = c.get('/')
            session = flask.session

            assert len(session['cart']['items']) == 0

            response = self.checkout("valid@email.com", c)
            assert 'error_msg' in response
            assert u'Seu carrinho está vazio.' == response['error_msg']

            response = self.checkout("", c)
            assert 'error_msg' in response
            assert u'Email inválido.' == response['error_msg']

            response = c.get('/products/list')
            products = json.loads(response.data)
            products = products['product_list']
            response = c.get('/cart/add/%s' % (products[0]['id']))
            assert len(session['cart']['items']) == 1

            response = self.checkout("valid@email.com", c, decode_json=False)
            assert response.status_code == 302
            print response.location


if __name__ == '__main__':
    unittest.main()
