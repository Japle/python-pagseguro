# coding: utf-8
import requests
import xmltodict

from .configs import Config
from .utils import parse_date

class PagSeguroNotificationResponse(object):
    def __init__(self, xml):
        self.xml = xml
        self.parse_xml(xml)

    def parse_xml(self, xml):
        parsed = xmltodict.parse(xml)
        transaction = parsed['transaction']
        for k, v in transaction.iteritems():
            setattr(self, k, v)


class PagSeguroCheckoutResponse(object):
    def __init__(self, xml):
        self.xml = xml
        self.code = None
        self.date = None
        self.errors = None
        self.payment_url = None
        self.parse_xml(xml)

    def parse_xml(self, xml):
        """ parse returned data """
        parsed = xmltodict.parse(xml)
        if 'errors' in parsed:
            self.errors = parsed['errors']['error']
            return

        checkout = parsed['checkout']
        self.code = checkout['code']
        self.date = parse_date(checkout['date'])

        self.payment_url = self.config.PAYMENT_URL % self.code


class PagSeguro(object):
    """ Pag Seguro V2 wrapper """

    def __init__(self, email, token, data=None):
        self.config = Config()
        self.data = {}
        self.data['email'] = email
        self.data['token'] = token
        self.data['currency'] = self.config.CURRENCY
        if data and isinstance(data, dict):
            self.data.update(data)

        self.items = []
        self.sender = {}
        self.shipping = {}
        self._reference = ""
        self.extra_amount = None
        self.redirect_url = None
        self.notification_url = None


    def build_checkout_params(self):
        """ build a dict with params """
        params = {}

        self.data.update(params)

    @property
    def reference_prefix(self):
        return self.config.REFERENCE_PREFIX or "%s"

    @reference_prefix.setter
    def reference_prefix(self, value):
        self.config.REFERENCE_PREFIX = (value or "") + "%s"

    @property
    def reference(self):
        return self.reference_prefix % self._reference

    @reference.setter
    def reference(self, value):
        if not isinstance(value, (str, unicode)):
            value = str(value)
        if value.startswith(self.reference_prefix):
            value = value[len(self.reference_prefix):]
        self._reference = value

    def get(self, url):
        """ do a get transaction """
        return requests.get(url, params=self.data, headers=self.config.HEADERS)

    def post(self, url):
        """ do a post request """
        return requests.post(url, data=self.data, headers=self.config.HEADERS)

    def checkout(self):
        """ create a pagseguro checkout """
        self.build_checkout_params()
        response = self.post(url=self.config.CHECKOUT_URL)
        return PagSeguroCheckoutResponse(response.content)

    def check_notification(self, code):
        """ check a notification by its code """
        response = self.get(url=self.config.NOTIFICATION_URL % code)
        return PagSeguroNotificationResponse(response.content)
