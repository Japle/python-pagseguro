# -*- coding: utf-8 -*-
import datetime

from pagseguro.utils import (is_valid_cpf, is_valid_cnpj, is_valid_email,
                             parse_date)
from pagseguro.exceptions import PagSeguroValidationError

import pytest
from dateutil.tz import tzutc


def test_is_valid_email():
    valid = 'test@email.com'
    valid2 = u'user@росси́я.ро'
    not_valid = '@asd.com'
    not_valid2 = 'bad'
    not_valid3 = u'user@росси́я'

    with pytest.raises(PagSeguroValidationError):
        is_valid_email(not_valid)

    with pytest.raises(PagSeguroValidationError):
        is_valid_email(not_valid2)

    with pytest.raises(PagSeguroValidationError):
        is_valid_email(not_valid3)

    assert is_valid_email(valid) == 'test@email.com'
    assert is_valid_email(valid2) == u'user@росси́я.ро'


def test_parse_date():
    # DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
    date_str = '2016-10-10T10:10:10'
    assert parse_date(date_str) == datetime.datetime(2016, 10, 10, 10, 10, 10,
                                                     tzinfo=tzutc())


def test_is_valid_cpf():
    valid = '041.684.826-50'
    valid2 = '04168482650'
    bad = 'bla///'
    max_digits = '1111111111111111111111111'
    invalid_cpf = '040.684.826-50'

    with pytest.raises(PagSeguroValidationError):
        is_valid_cpf(bad)

    with pytest.raises(PagSeguroValidationError):
        is_valid_cpf(max_digits)

    with pytest.raises(PagSeguroValidationError):
        is_valid_cpf(invalid_cpf)

    assert is_valid_cpf(valid) == valid
    assert is_valid_cpf(valid2) == '04168482650'


def test_is_valid_cnpj():
    valid = '31331052000174'
    valid2 = '72.168.117/0001-90'

    invalid = '///'
    digits = '1111111'
    wrong_number = '31331052000175'

    with pytest.raises(PagSeguroValidationError):
        is_valid_cnpj(invalid)

    with pytest.raises(PagSeguroValidationError):
        is_valid_cnpj(digits)

    with pytest.raises(PagSeguroValidationError):
        is_valid_cnpj(wrong_number)

    assert is_valid_cnpj(valid) == '31331052000174'
    assert is_valid_cnpj(valid2) == '72168117000190'
