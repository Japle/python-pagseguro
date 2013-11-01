# coding: utf-8
import unittest

from pagseguro import PagSeguro
from pagseguro.configs import Config
from pagseguro.exceptions import PagSeguroValidationError
from pagseguro.utils import is_valid_email, is_valid_cpf


class PagseguroTest(unittest.TestCase):

    def setUp(self):
        self.token = '123456'
        self.email = 'seu@email.com'
        self.pagseguro = PagSeguro(token=self.token, email=self.email)
        self.sender = {
            'name': u'Guybrush Treepwood',
            'area_code': 11,
            "phone": 5555555,
            "email": 'guybrush@monkeyisland.com',
            "cpf": "00000000000",
            "born_date": "06/08/1650",
        }
        self.shipping = {
            "type": self.pagseguro.SEDEX,
            "street": "Av Brig Faria Lima",
            "number": 1234,
            "complement": "5 andar",
            "district": "Jardim Paulistano",
            "postal_code": "06650030",
            "city": "Sao Paulo",
            "state": "SP",
            "country": "BRA",
            "cost": "1234.56"
        }
        self.items = [
            {"id": "0001", "description": "Produto 1", "amount": 354.20, "quantity": 2, "weight": 200},
            {"id": "0002", "description": "Produto 2", "amount": 355.20, "quantity": 1, "weight": 200},
        ]

    def test_pagseguro_class(self):
        self.assertIsInstance(self.pagseguro, PagSeguro)

    def test_pagseguro_initial_attrs(self):
        self.assertIsInstance(self.pagseguro.config, Config)
        self.assertIsInstance(self.pagseguro.data, dict)
        self.assertTrue('email' in self.pagseguro.data)
        self.assertTrue('token' in self.pagseguro.data)
        self.assertTrue('currency' in self.pagseguro.data)
        self.assertEqual(self.pagseguro.data['email'], self.email)
        self.assertEqual(self.pagseguro.data['token'], self.token)
        self.assertEqual(self.pagseguro.data['currency'], self.pagseguro.config.CURRENCY)
        self.assertIsInstance(self.pagseguro.items, list)
        self.assertIsInstance(self.pagseguro.sender, dict)
        self.assertIsInstance(self.pagseguro.shipping, dict)
        self.assertEqual(self.pagseguro._reference, "")
        self.assertIsNone(self.pagseguro.extra_amount)
        self.assertIsNone(self.pagseguro.redirect_url)
        self.assertIsNone(self.pagseguro.notification_url)
        self.assertIsNone(self.pagseguro.abandon_url)

    def test_build_checkout_params_with_all_params(self):
        self.pagseguro.sender = self.sender
        self.pagseguro.shipping = self.shipping
        self.pagseguro.extra_amount = 12.50
        self.pagseguro.redirect_url = '/redirecionando/'
        self.pagseguro.abandon_url = '/abandonando/'
        self.pagseguro.items = self.items
        self.pagseguro.build_checkout_params()
        # check all data fields
        self.assertIsInstance(self.pagseguro.data, dict)
        keys = ['email', 'token', 'currency', 'senderName', 'senderAreaCode', 'senderPhone',
                'senderEmail', 'senderCPF', 'senderBornDate', 'shippingType',
                'shippingAddressStreet', 'shippingAddressNumber', 'shippingAddressComplement',
                'shippingAddressDistrict', 'shippingAddressPostalCode', 'shippingAddressCity',
                'shippingAddressState', 'shippingAddressCountry', 'shippingCost', 'extraAmount',
                'redirectURL', 'abandonURL']
        # items
        item_keys = ['itemId%s', 'itemDescription%s', 'itemAmount%s', 'itemQuantity%s',
                     'itemWeight%s', 'itemShippingCost%s']

        for key in keys:
            self.assertTrue(key in self.pagseguro.data)

        for i, key in enumerate(item_keys, 1):
            self.assertTrue(key % i, self.pagseguro.data)

    def test_add_items_util(self):
        pagseguro = PagSeguro(email=self.email, token=self.token)
        pagseguro.add_item(**self.items[0])
        pagseguro.add_item(**self.items[1])
        self.assertEqual(len(pagseguro.items), 2)

    def test_reference(self):
        self.pagseguro.reference = '12345'
        self.assertEqual(unicode(self.pagseguro.reference), u'REF12345')

    def test_clean_none_params(self):
        pagseguro = PagSeguro(email=self.email, token=self.token)
        sender = self.sender
        sender['cpf'] = None
        sender['born_date'] = None
        pagseguro.sender = self.sender
        pagseguro.build_checkout_params()

        self.assertTrue('senderCPF' not in pagseguro.data)
        self.assertTrue('senderBornData' not in pagseguro.data)

    def test_is_valid_email(self):
        bad_email = 'john.com'
        pagseguro = PagSeguro(email=bad_email, token=self.token)
        pagseguro.sender = {
            'email': bad_email
        }
        with self.assertRaises(PagSeguroValidationError):
            pagseguro.build_checkout_params()

        # Now testing with a valid email
        pagseguro.sender['email'] = self.sender.get('email')
        self.assertEqual(is_valid_email(pagseguro.sender['email']), self.sender.get('email'))

    def test_is_valid_cpf(self):
        bad_cpf = '123.456.267-45'
        pagseguro = PagSeguro(email=self.email, token=self.token)
        pagseguro.sender = {
            'cpf': bad_cpf
        }
        with self.assertRaises(PagSeguroValidationError):
            pagseguro.build_checkout_params()

        # Now testing with a valid email
        pagseguro.sender['cpf'] = '482.268.465-28'
        self.assertEqual(is_valid_cpf(pagseguro.sender['cpf']), pagseguro.sender['cpf'])

        pagseguro.sender['cpf'] = '48226846528'
        self.assertEqual(is_valid_cpf(pagseguro.sender['cpf']), pagseguro.sender['cpf'])


if __name__ == '__main__':
    unittest.main()
