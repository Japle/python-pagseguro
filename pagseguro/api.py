# coding: utf-8
import requests
import xmltodict

from .configs import Config

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

    def get(self):
        """ do a get transaction """

    def post(self):
        """ do a post request """

    def checkout(self):
        """ create a pagseguro checkout
        and returns its code and its redirect url """

    def get_notification(self):
        """ get the notification POST from pagseguro """

    def check_notification(self):
        """ check a notification by its code """
