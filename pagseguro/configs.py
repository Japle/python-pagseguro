# coding: utf-8


class Config(object):
    def get(self, key, default=None):
        return getattr(self, key, default)

    BASE_URL = "https://ws.pagseguro.uol.com.br"
    VERSION = "/v2/"
    CHECKOUT_SUFFIX = VERSION + "checkout"
    CHARSET = "UTF-8"  # ISO-8859-1
    NOTIFICATION_SUFFIX = VERSION + "transactions/notifications/%s"
    TRANSACTION_SUFFIX = VERSION + "transactions/%s"
    CHECKOUT_URL = BASE_URL + CHECKOUT_SUFFIX
    NOTIFICATION_URL = BASE_URL + NOTIFICATION_SUFFIX
    TRANSACTION_URL = BASE_URL + TRANSACTION_SUFFIX
    CURRENCY = "BRL"
    CTYPE = "application/x-www-form-urlencoded; charset={0}".format(CHARSET)
    HEADERS = {"Content-Type": CTYPE}
    REFERENCE_PREFIX = "REF%s"
    PAYMENT_HOST = "https://pagseguro.uol.com.br"
    PAYMENT_URL = PAYMENT_HOST + CHECKOUT_SUFFIX + "/payment.html?code=%s"

    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
