# -*- coding: utf-8 -*-
import pytest

from pagseguro import PagSeguro


@pytest.fixture(scope='session')
def sender():
    return {
        'name': u'Guybrush Treepwood',
        'area_code': 11,
        "phone": 5555555,
        "email": 'guybrush@monkeyisland.com',
        "cpf": "00000000000",
        "born_date": "06/08/1650",
    }


@pytest.fixture(scope='session')
def shipping():
    return {
        "type": PagSeguro.SEDEX,
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


@pytest.fixture(scope='session')
def items():
    return [
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
