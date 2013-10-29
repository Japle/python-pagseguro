# coding: utf-8


class Config(object):
    BASE_URL = "https://ws.pagseguro.uol.com.br"
    VERSION = "/v2/"
    CHECKOUT_SUFFIX = VERSION + "checkout"
    NOTIFICATION_SUFFIX = VERSION + "transactions/notifications/%s"
    TRANSACTION_SUFFIX = VERSION + "transactions/"
    CHEKOUT_URL = BASE_URL + CHECKOUT_SUFFIX
    NOTIFICATION_URL = BASE_URL + NOTIFICATION_SUFFIX
    TRANSACTION_URL = BASE_URL + TRANSACTION_SUFFIX
    CURRENCY = "BRL"
    HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded; charset=ISO-8859-1"
    }
    REFERENCE_PREFIX = "REF%s"
    PAYMENT_HOST = "https://pagseguro.uol.com.br"
    PAYMENT_REDIRECT_URL = PAYMENT_HOST + CHECKOUT_SUFFIX + "/payment.html?%s"
    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
