#!/usr/bin/env python
import os
import flask_seguro
import unittest
import tempfile
import flask
from flask import json

class FlasKSeguroTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flask_seguro.app.config['DATABASE'] = tempfile.mkstemp()
        flask_seguro.app.config['TESTING'] = True
        self.app = flask_seguro.app.test_client()
        #flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flask_seguro.app.config['DATABASE'])


    def testRetrieveCartAndAddRemoveItem(self):
        with flask_seguro.app.test_client() as c:
            response = c.get('/')
            session = flask.session
            assert 'cart' in session
            assert len(session['cart'])==0

            response = c.get('/products/list')
            products = json.loads(response.data)
            assert 'product_list' in products
            assert len(products['product_list']) > 0
            products = products['product_list']

            response = c.get('/cart/add/%s'%(products[0]['id']))
            assert len(session['cart'])==1

            response = c.get('/cart/remove/%s'%(products[0]['id']))
            assert len(session['cart'])==0


if __name__ == '__main__':
    unittest.main()
