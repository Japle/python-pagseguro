# coding: utf-8
import re

import arrow

from .exceptions import PagSeguroValidationError

def parse_date(date_str):
    return arrow.get(date_str).datetime

# Validators
def is_valid_email(value):
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*$"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"$)', # quoted-string
        re.IGNORECASE)
    domain_regex = re.compile(
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,})$'  # domain
        # literal form, ipv4 address (SMTP 4.1.3)
        r'|^\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$',
        re.IGNORECASE)
    domain_whitelist = ['localhost']

    if not value or '@' not in value:
        raise PagSeguroValidationError(u'Email inválido')

    user_part, domain_part = value.rsplit('@', 1)

    if not user_regex.match(user_part):
        raise PagSeguroValidationError(u'Email inválido')

    if (not domain_part in domain_whitelist and
            not domain_regex.match(domain_part)):
        # Try for possible IDN domain-part
        try:
            domain_part = domain_part.encode('idna').decode('ascii')
            if not domain_regex.match(domain_part):
                raise PagSeguroValidationError(u'Email inválido')
            else:
                return value
        except UnicodeError:
            pass
        raise PagSeguroValidationError(u'Email inválido')
    return value
