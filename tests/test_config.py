#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pagseguro.config import Config

import pytest


@pytest.fixture
def custom_config():
    return {
        'payment_url': 'http://google.com'
    }


@pytest.fixture
def common_config():
    return { # flake8: noqa
        'CHECKOUT_URL': 'https://ws.pagseguro.uol.com.br/v2/checkout',
        'CURRENCY': 'BRL',
        'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S',
        'HEADERS': {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
        'NOTIFICATION_URL': 'https://ws.pagseguro.uol.com.br/v2/transactions/notifications/%s',
        'PAYMENT_URL': 'https://pagseguro.uol.com.br/v2/checkout/payment.html?code=%s',
        'PRE_APPROVAL_CANCEL_URL': 'https://ws.pagseguro.uol.com.br/v2/pre-approvals/cancel/%s',
        'PRE_APPROVAL_NOTIFICATION_URL': 'https://ws.pagseguro.uol.com.br/v2/pre-approvals/notifications/%s',
        'PRE_APPROVAL_PAYMENT_URL': 'https://ws.pagseguro.uol.com.br/v2/pre-approvals/payment',
        'QUERY_PRE_APPROVAL_URL': 'https://ws.pagseguro.uol.com.br/v2/pre-approvals',
        'QUERY_TRANSACTION_URL': 'https://ws.pagseguro.uol.com.br/v2/transactions',
        'SESSION_CHECKOUT_URL': 'https://ws.pagseguro.uol.com.br/v2/sessions/',
        'TRANSACTION_URL': 'https://ws.pagseguro.uol.com.br/v2/transactions/%s',
        'TRANSPARENT_CHECKOUT_URL': 'https://ws.pagseguro.uol.com.br/v2/transactions'
    }


def test_common_config(common_config):
    c = Config()
    for key, val in common_config.items():
        print key, val
        assert getattr(c, key) == common_config[key]


def test_custom_config(custom_config):
    c = Config(**custom_config)
    assert c.PAYMENT_URL == custom_config['payment_url']

def test_config_special_methods():
    c = Config()
    assert c.__getitem__('PAYMENT_URL') == c.PAYMENT_URL

    c.__setitem__('PAYMENT_URL', 'http://google.com')
    assert c.PAYMENT_URL == 'http://google.com'
    assert c['PAYMENT_URL'] == 'http://google.com'
