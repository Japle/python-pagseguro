
class Config:
    EXTRA_AMOUNT = 12.12
    REDIRECT_URL = "http://meusite.com/obrigado"
    NOTIFICATION_URL = "http://meusite.com/notification"
    EMAIL = "seuemail@dominio.com"
    TOKEN = "ABCDEFGHIJKLMNO"
    SECRET_KEY = "s3cr3t"

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'

config = {
    'development': DevelopmentConfig
}