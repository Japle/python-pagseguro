# coding: utf-8
import unittest

from pagseguro import PagSeguro, PagSeguroTransactionSearchResult
from pagseguro.configs import Config, ConfigSandbox
from pagseguro.exceptions import PagSeguroValidationError
from pagseguro.utils import is_valid_email, is_valid_cpf


class PagseguroTest(unittest.TestCase):
    def setUp(self):
        self.token = 'sandbox_token'
        self.email = 'pagseguro_email'
        self.pagseguro = PagSeguro(
            token=self.token,
            email=self.email,
            config=ConfigSandbox())
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
            {
                "id": "0001",
                "description": "Produto 1",
                "amount": 354.20,
                "quantity": 2,
                "weight": 200
            },
            {
                "id": "0002",
                "description": "Produto 2",
                "amount": 355.20,
                "quantity": 1,
                "weight": 200
            },
        ]

    def test_pagseguro_class(self):
        self.assertIsInstance(self.pagseguro, PagSeguro)

    def test_pagseguro_initial_attrs(self):
        self.assertIsInstance(self.pagseguro.config, ConfigSandbox)
        self.assertIsInstance(self.pagseguro.data, dict)
        self.assertIn('email', self.pagseguro.data)
        self.assertIn('token', self.pagseguro.data)
        self.assertEqual(self.pagseguro.data['email'], self.email)
        self.assertEqual(self.pagseguro.data['token'], self.token)
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
        keys = ['email', 'token', 'senderName', 'senderAreaCode',
                'senderPhone', 'senderEmail', 'senderCPF', 'senderBornDate',
                'shippingType', 'shippingAddressStreet',
                'shippingAddressNumber', 'shippingAddressComplement',
                'shippingAddressDistrict', 'shippingAddressPostalCode',
                'shippingAddressCity', 'shippingAddressState',
                'shippingAddressCountry', 'shippingCost', 'extraAmount',
                'redirectURL', 'abandonURL']
        # items
        item_keys = ['itemId%s', 'itemDescription%s', 'itemAmount%s',
                     'itemQuantity%s', 'itemWeight%s', 'itemShippingCost%s']

        for key in keys:
            self.assertIn(key, self.pagseguro.data)

        for i, key in enumerate(item_keys, 1):
            self.assertTrue(key % i, self.pagseguro.data)

    def test_add_items_util(self):
        pagseguro = PagSeguro(email=self.email, token=self.token)
        pagseguro.add_item(**self.items[0])
        pagseguro.add_item(**self.items[1])
        self.assertEqual(len(pagseguro.items), 2)

    def test_reference(self):
        self.pagseguro.reference = '12345'
        self.assertEqual(str(self.pagseguro.reference), u'REF12345')

    def test_clean_none_params(self):
        pagseguro = PagSeguro(email=self.email, token=self.token)
        sender = self.sender
        sender['cpf'] = None
        sender['born_date'] = None
        pagseguro.sender = self.sender
        pagseguro.build_checkout_params()

        self.assertNotIn('senderCPF', pagseguro.data)
        self.assertNotIn('senderBornData', pagseguro.data)

    def test_is_valid_email(self):
        bad_email = 'john.com'
        pagseguro = PagSeguro(email=bad_email, token=self.token)
        pagseguro.sender = {'email': bad_email}
        with self.assertRaises(PagSeguroValidationError):
            pagseguro.build_checkout_params()

        # Now testing with a valid email
        pagseguro.sender['email'] = self.sender.get('email')
        self.assertEqual(is_valid_email(pagseguro.sender['email']),
                         self.sender.get('email'))

    def test_is_valid_cpf(self):
        bad_cpf = '123.456.267-45'
        pagseguro = PagSeguro(email=self.email, token=self.token)
        pagseguro.sender = {'cpf': bad_cpf}
        with self.assertRaises(PagSeguroValidationError):
            pagseguro.build_checkout_params()

        # Now testing with a valid email
        pagseguro.sender['cpf'] = '482.268.465-28'
        self.assertEqual(is_valid_cpf(pagseguro.sender['cpf']),
                         pagseguro.sender['cpf'])

        pagseguro.sender['cpf'] = '48226846528'
        self.assertEqual(is_valid_cpf(pagseguro.sender['cpf']),
                         pagseguro.sender['cpf'])


class PagSeguroTransactionSearchResultTest(unittest.TestCase):
    def setUp(self):
        self.email = 'seu@email.com'
        self.token = '123456'
        self.xml = """
        <transactionSearchResult>
            <date>2011-02-16T20:14:35.000-02:00</date>
            <currentPage>1</currentPage>
            <resultsInThisPage>2</resultsInThisPage>
            <totalPages>1</totalPages>
            <transactions>
                <transaction>
                    <date>2011-02-05T15:46:12.000-02:00</date>
                    <lastEventDate>2011-02-15T17:39:14.000-03:00</lastEventDate>
                    <code>9E884542-81B3-4419-9A75-BCC6FB495EF1</code>
                    <reference>REF1234</reference>
                    <type>1</type>
                    <status>3</status>
                    <paymentMethod>
                        <type>1</type>
                    </paymentMethod>
                    <grossAmount>49900.00</grossAmount>
                    <discountAmount>0.00</discountAmount>
                    <feeAmount>0.00</feeAmount>
                    <netAmount>49900.00</netAmount>
                    <extraAmount>0.00</extraAmount>
                </transaction>
                <transaction>
                    <date>2011-02-07T18:57:52.000-02:00</date>
                    <lastEventDate>2011-02-14T21:37:24.000-03:00</lastEventDate>
                    <code>2FB07A22-68FF-4F83-A356-24153A0C05E1</code>
                    <reference>REF5678</reference>
                    <type>3</type>
                    <status>4</status>
                    <paymentMethod>
                        <type>3</type>
                    </paymentMethod>
                    <grossAmount>26900.00</grossAmount>
                    <discountAmount>0.00</discountAmount>
                    <feeAmount>0.00</feeAmount>
                    <netAmount>26900.00</netAmount>
                    <extraAmount>0.00</extraAmount>
                </transaction>
            </transactions>
        </transactionSearchResult>"""

    def test_parse_xml(self):
        pg = PagSeguro(email=self.email, token=self.token)
        result = PagSeguroTransactionSearchResult(self.xml, pg.config)
        self.assertEqual(result.current_page, 1)
        self.assertEqual(result.results_in_page, 2)
        self.assertEqual(result.total_pages, 1)
        self.assertEqual(len(result.transactions), 2)
