# -*- coding: utf-8 -*-
class Config(dict):
    def __init__(self, **kwargs):
        sandbox = kwargs.pop('sandbox', False)

        base_url = 'https://ws.pagseguro.uol.com.br'
        payment_host = 'https://pagseguro.uol.com.br'
        if sandbox:
            base_url = 'https://ws.sandbox.pagseguro.uol.com.br'
            payment_host = 'https://sandbox.pagseguro.uol.com.br'

        # prefixes/suffixes
        version = '/v2/'
        checkout_suffix = '{}checkout'.format(version)
        session_checkout_suffix = '{}sessions/'.format(version)
        notification_suffix = '{}transactions/notifications/%s'.format(version)
        pre_approval_notification_suffix = ('{}pre-approvals/'
                                            'notifications/%s'.format(version))
        transaction_suffix = '{}transactions/%s'.format(version)
        query_transaction_suffix = '{}transactions'.format(version)
        ctype = 'application/x-www-form-urlencoded; charset=UTF-8'

        # default config settings
        defaults = dict(
            PRE_APPROVAL_PAYMENT_URL='{}{}pre-approvals/payment'.format(
                base_url, version),
            PRE_APPROVAL_CANCEL_URL='{}{}pre-approvals/cancel/%s'.format(
                base_url, version),
            SESSION_CHECKOUT_URL='{}{}'.format(
                base_url, session_checkout_suffix),
            TRANSPARENT_CHECKOUT_URL='{}{}'.format(
                base_url, query_transaction_suffix),
            CHECKOUT_URL='{}{}'.format(base_url, checkout_suffix),
            NOTIFICATION_URL='{}{}'.format(base_url, notification_suffix),
            PRE_APPROVAL_NOTIFICATION_URL='{}{}'.format(
                base_url, pre_approval_notification_suffix),
            TRANSACTION_URL='{}{}'.format(base_url, transaction_suffix),
            QUERY_TRANSACTION_URL='{}{}'.format(
                base_url, query_transaction_suffix),
            QUERY_PRE_APPROVAL_URL='{}{}pre-approvals'.format(
                base_url, version),
            CURRENCY='BRL',
            HEADERS={'Content-Type': ctype},
            PAYMENT_URL='{}{}/payment.html?code=%s'.format(
                payment_host, checkout_suffix),
            DATETIME_FORMAT='%Y-%m-%dT%H:%M:%S',
            REFERENCE_PREFIX='REF%s',
            USE_SHIPPING=True,
        )

        kwargs = {key.upper(): val for key, val in kwargs.items()}
        keys = defaults.keys()
        for key in keys:
            # only add override keys to properties
            value = kwargs.pop(key, defaults[key])
            setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)
