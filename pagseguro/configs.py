# coding: utf-8
import abc


class AbstractConfig(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, sandbox=False):
        self.sandbox = sandbox

    @classmethod
    def get(self, key, default=None):
        return getattr(self, key, default)

    @abc.abstractproperty
    def BASE_URL(self):
        return self._BASE_URL

    @BASE_URL.setter
    def BASE_URL(self, value):
        self._BASE_URL = value

    @abc.abstractproperty
    def VERSION(self):
        return self._VERSION

    @VERSION.setter
    def VERSION(self, value):
        self._VERSION = value

    @abc.abstractproperty
    def CHECKOUT_SUFFIX(self):
        return self._CHECKOUT_SUFFIX

    @CHECKOUT_SUFFIX.setter
    def CHECKOUT_SUFFIX(self, value):
        self._CHECKOUT_SUFFIX = value

    @abc.abstractproperty
    def CHARSET(self):
        return self._CHARSET

    @CHARSET.setter
    def CHARSET(self, value):
        self._CHARSET = value

    @abc.abstractproperty
    def NOTIFICATION_SUFFIX(self):
        return self._NOTIFICATION_SUFFIX

    @NOTIFICATION_SUFFIX.setter
    def NOTIFICATION_SUFFIX(self, value):
        self._NOTIFICATION_SUFFIX = value

    @abc.abstractproperty
    def TRANSACTION_SUFFIX(self):
        return self._TRANSACTION_SUFFIX

    @TRANSACTION_SUFFIX.setter
    def TRANSACTION_SUFFIX(self, value):
        self._TRANSACTION_SUFFIX = value

    @abc.abstractproperty
    def QUERY_TRANSACTION_SUFFIX(self):
        return self._QUERY_TRANSACTION_SUFFIX

    @QUERY_TRANSACTION_SUFFIX.setter
    def QUERY_TRANSACTION_SUFFIX(self, value):
        self._QUERY_TRANSACTION_SUFFIX = value

    @abc.abstractproperty
    def CHECKOUT_URL(self):
        return self._CHECKOUT_URL

    @CHECKOUT_URL.setter
    def CHECKOUT_URL(self, value):
        self._CHECKOUT_URL = value

    @abc.abstractproperty
    def NOTIFICATION_URL(self):
        return self._NOTIFICATION_URL

    @NOTIFICATION_URL.setter
    def NOTIFICATION_URL(self, value):
        self._NOTIFICATION_URL = value

    @abc.abstractproperty
    def TRANSACTION_URL(self):
        return self._TRANSACTION_URL

    @TRANSACTION_URL.setter
    def TRANSACTION_URL(self, value):
        self._TRANSACTION_URL = value

    @abc.abstractproperty
    def QUERY_TRANSACTION_URL(self):
        return self._QUERY_TRANSACTION_URL

    @QUERY_TRANSACTION_URL.setter
    def QUERY_TRANSACTION_URL(self, value):
        self._QUERY_TRANSACTION_URL = value

    @abc.abstractproperty
    def CURRENCY(self):
        return self._CURRENCY

    @CURRENCY.setter
    def CURRENCY(self, value):
        self._CURRENCY = value

    @abc.abstractproperty
    def CTYPE(self):
        return self._CTYPE

    @CTYPE.setter
    def CTYPE(self, value):
        self._CTYPE = value

    @abc.abstractproperty
    def HEADERS(self):
        return self._HEADERS

    @HEADERS.setter
    def HEADERS(self, value):
        self._HEADERS = value

    @abc.abstractproperty
    def REFERENCE_PREFIX(self):
        return self._REFERENCE_PREFIX

    @REFERENCE_PREFIX.setter
    def REFERENCE_PREFIX(self, value):
        self._REFERENCE_PREFIX = value

    @abc.abstractproperty
    def PAYMENT_HOST(self):
        return self._PAYMENT_HOST

    @PAYMENT_HOST.setter
    def PAYMENT_HOST(self, value):
        self._PAYMENT_HOST = value

    @abc.abstractproperty
    def PAYMENT_URL(self):
        return self._PAYMENT_URL

    @PAYMENT_URL.setter
    def PAYMENT_URL(self, value):
        self._PAYMENT_URL = value

    @abc.abstractproperty
    def DATETIME_FORMAT(self):
        return self._DATETIME_FORMAT

    @DATETIME_FORMAT.setter
    def DATETIME_FORMAT(self, value):
        self._DATETIME_FORMAT = value


class Config(AbstractConfig):

    BASE_URL = "https://ws.pagseguro.uol.com.br"
    VERSION = "/v2/"
    CHECKOUT_SUFFIX = VERSION + "checkout"
    CHARSET = "UTF-8"  # ISO-8859-1
    NOTIFICATION_SUFFIX = VERSION + "transactions/notifications/%s"
    PRE_APPROVAL_NOTIFICATION_SUFFIX = (
        VERSION + "pre-approvals/notifications/%s"
    )
    PRE_APPROVAL_PAYMENT_URL = BASE_URL + VERSION + "pre-approvals/payment"
    PRE_APPROVAL_CANCEL_URL = BASE_URL + VERSION + "pre-approvals/cancel/%s"
    TRANSACTION_SUFFIX = VERSION + "transactions/%s"
    QUERY_TRANSACTION_SUFFIX = VERSION + "transactions"
    SESSION_CHECKOUT_SUFFIX = VERSION + "sessions/"
    SESSION_CHECKOUT_URL = BASE_URL + SESSION_CHECKOUT_SUFFIX
    TRANSPARENT_CHECKOUT_URL = BASE_URL + QUERY_TRANSACTION_SUFFIX + '/'
    CHECKOUT_URL = BASE_URL + CHECKOUT_SUFFIX
    NOTIFICATION_URL = BASE_URL + NOTIFICATION_SUFFIX
    PRE_APPROVAL_NOTIFICATION_URL = BASE_URL + PRE_APPROVAL_NOTIFICATION_SUFFIX
    TRANSACTION_URL = BASE_URL + TRANSACTION_SUFFIX
    QUERY_TRANSACTION_URL = BASE_URL + QUERY_TRANSACTION_SUFFIX
    QUERY_PRE_APPROVAL_URL = BASE_URL + VERSION + "pre-approvals"
    CURRENCY = "BRL"
    CTYPE = "application/x-www-form-urlencoded; charset={0}".format(CHARSET)
    HEADERS = {"Content-Type": CTYPE}
    REFERENCE_PREFIX = "REF%s"
    PAYMENT_HOST = "https://pagseguro.uol.com.br"
    PAYMENT_URL = PAYMENT_HOST + CHECKOUT_SUFFIX + "/payment.html?code=%s"
    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


class ConfigSandbox(AbstractConfig):
    BASE_URL = "https://ws.sandbox.pagseguro.uol.com.br"
    VERSION = "/v2/"
    CHECKOUT_SUFFIX = VERSION + "checkout"
    CHARSET = "UTF-8"  # ISO-8859-1
    NOTIFICATION_SUFFIX = VERSION + "transactions/notifications/%s"
    TRANSACTION_SUFFIX = VERSION + "transactions/%s"
    QUERY_TRANSACTION_SUFFIX = VERSION + "transactions"
    CHECKOUT_URL = BASE_URL + CHECKOUT_SUFFIX
    NOTIFICATION_URL = BASE_URL + NOTIFICATION_SUFFIX
    TRANSACTION_URL = BASE_URL + TRANSACTION_SUFFIX
    QUERY_TRANSACTION_URL = BASE_URL + QUERY_TRANSACTION_SUFFIX
    CURRENCY = "BRL"
    CTYPE = "application/x-www-form-urlencoded; charset={0}".format(CHARSET)
    HEADERS = {"Content-Type": CTYPE}
    REFERENCE_PREFIX = "REF%s"
    PAYMENT_HOST = "https://sandbox.pagseguro.uol.com.br"
    PAYMENT_URL = PAYMENT_HOST + CHECKOUT_SUFFIX + "/payment.html?code=%s"

    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
