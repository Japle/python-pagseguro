#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import tempfile
import flask
from flask import json

from flask_seguro.products import Products
from flask_seguro import create_app


class FlasKSeguroTestCase(unittest.TestCase):
    def setUp(self):
        self._current_app = create_app('development')

        self.db_fd, self._current_app.config['DATABASE'] = tempfile.mkstemp()
        self._current_app.config['TESTING'] = True
        self.app = self._current_app.test_client()
        # flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self._current_app.config['DATABASE'])

    def list_products(self):
        return Products().get_all()

    def check_cart_fields(self, response):
        cart = flask.session['cart']
        self.assertNotIn('error_msg', cart)
        self.assertIn('total', cart)
        self.assertIn('subtotal', cart)
        return cart

    def test_retrieve_cart_and_add_remove_item(self):
        with self._current_app.test_client() as c:
            response = c.get('/')
            session = flask.session
            self.assertIn('cart', session)
            self.assertEquals(0, len(session['cart']['items']))

            products = self.list_products()

            response = c.get('/cart/add/%s' % (products[0]['id']))
            self.assertEquals(1, len(session['cart']['items']))
            cart = self.check_cart_fields(response)
            self.assertEquals(
                float(cart['subtotal']), float(products[0]['price']))

            response = c.get('/cart/remove/%s' % (products[0]['id']))
            self.assertEquals(0, len(session['cart']['items']))
            cart = self.check_cart_fields(response)
            self.assertEquals(0, float(cart['total']))
            self.assertEquals(float(cart['total']), float(cart['subtotal']))

    def checkout(self, data, c, decode_json=True):
        response = c.post('/checkout', data=data)
        if decode_json:
            response = json.loads(response.data)
        return response

    def test_checkout(self):
        with self._current_app.test_client() as c:
            response = c.get('/')
            session = flask.session

            self.assertEquals(0, len(session['cart']['items']))

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
            self.assertEquals(
                u'Seu carrinho está vazio.', response['error_msg'])

            response = self.checkout({}, c)
            self.assertIn('error_msg', response)
            self.assertEquals(
                u'Todos os campos são obrigatórios.', response['error_msg'])

            products = self.list_products()
            response = c.get('/cart/add/%s' % (products[0]['id']))
            self.assertEquals(1, len(session['cart']['items']))

            response = self.checkout(data, c, decode_json=False)
            self.assertEquals(302, response.status_code)
            self.assertIn('pagseguro', response.location)

    def test_cart_view(self):
        response = self.app.get('/cart')
        self.assertEquals(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
