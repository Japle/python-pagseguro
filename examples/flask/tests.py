#!/usr/bin/env python
import os
import flask_seguro
import unittest
import tempfile
import flask

class FlasKSeguroTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flask_seguro.app.config['DATABASE'] = tempfile.mkstemp()
        flask_seguro.app.config['TESTING'] = True
        self.app = flask_seguro.app.test_client()
        #flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flask_seguro.app.config['DATABASE'])

    def testRetrieveCart(self):
        with flask_seguro.app.test_client() as c:
            #assert 'cart' not in flask.session
            response = c.get('/')
            assert 'cart' in flask.session


if __name__ == '__main__':
    unittest.main()
