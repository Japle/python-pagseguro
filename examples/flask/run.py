#!/usr/bin/env python
from flask_seguro import app


class Config(object):
    EXTRA_AMOUNT = 12.70
    REDIRECT_URL = "http://meusite.com/obrigado"
    NOTIFICATION_URL = "http://meusite.com/notification"
    EMAIL = "seuemail@dominio.com"
    TOKEN = "ABCDEFGHIJKLMNO"

if __name__ == "__main__":
    app.config.from_object(Config())
    app.run()
