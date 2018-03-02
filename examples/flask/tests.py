#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import flask_seguro
import unittest
import tempfile
import flask
from flask import json
from flask_seguro.products import Products


class FlasKSeguroTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, flask_seguro.app.config['DATABASE'] = tempfile.mkstemp()
        config_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'settings.cfg')
        flask_seguro.app.config.from_pyfile(config_file)
        flask_seguro.app.config['TESTING'] = True
        self.app = flask_seguro.app.test_client()
        # flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flask_seguro.app.config['DATABASE'])

    def list_products(self):
        return Products().get_all()

    def check_cart_fields(self, response):
        cart = flask.session['cart']
        self.assertNotIn('error_msg', cart)
        self.assertIn('total', cart)
        self.assertIn('subtotal', cart)
        return cart

    def test_retrieve_cart_and_add_remove_item(self):
        with flask_seguro.app.test_client() as c:
            response = c.get('/')
            session = flask.session
            self.assertIn('cart', session)
            self.assertEqual(0, len(session['cart']['items']))

            products = self.list_products()

            response = c.get('/cart/add/%s' % (products[0]['id']))
            self.assertEqual(1, len(session['cart']['items']))
            cart = self.check_cart_fields(response)
            self.assertEqual(
                float(cart['subtotal']), float(products[0]['price']))

            response = c.get('/cart/remove/%s' % (products[0]['id']))
            self.assertEqual(0, len(session['cart']['items']))
            cart = self.check_cart_fields(response)
            self.assertEqual(0, float(cart['total']))
            self.assertEqual(float(cart['total']), float(cart['subtotal']))

    def checkout(self, data, c, decode_json=True):
        response = c.post('/checkout', data=data)
        if decode_json:
            response = json.loads(response.data)
        return response

    def test_checkout(self):
        with flask_seguro.app.test_client() as c:
            response = c.get('/')
            session = flask.session

            self.assertEqual(0, len(session['cart']['items']))

            data = {
                "name": "Victor Shyba",
                "email": "teste@example.com",
                "street": "Av Brig Faria Lima",
                "number": 1234,
                "complement": "5 andar",
                "district": "Jardim Paulistano",
                "postal_code": "06650030",
                "city": "Sao Paulo",
                "state": "SP"
            }

            response = self.checkout(data, c)
            self.assertIn('error_msg', response)
            self.assertEqual(
                u'Seu carrinho está vazio.', response['error_msg'])

            response = self.checkout({}, c)
            self.assertIn('error_msg', response)
            self.assertEqual(
                u'Todos os campos são obrigatórios.', response['error_msg'])

            products = self.list_products()
            response = c.get('/cart/add/%s' % (products[0]['id']))
            self.assertEqual(1, len(session['cart']['items']))

            response = self.checkout(data, c, decode_json=False)
            self.assertEqual(302, response.status_code)
            self.assertIn('pagseguro', response.location)

    def test_cart_view(self):
        response = self.app.get('/cart')
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
