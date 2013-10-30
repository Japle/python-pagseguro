# coding: utf-8

import arrow


def parse_date(date_str):
    return arrow.get(date_str).datetime
