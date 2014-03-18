from pagseguro import PagSeguro


def make_cart():
    # aqui o carrinho poderia ser criado no banco, por exemplo
    return []

def make_pg():
    pg = PagSeguro(email="seuemail@dominio.com", token="ABCDEFGHIJKLMNO")
    pg.sender = {
        "name": "Bruno Rocha",
        "area_code": 11,
        "phone": 981001213,
        "email": "rochacbruno@gmail.com",
    }
    pg.shipping = {
        "type": pg.SEDEX,
        "street": "Av Brig Faria Lima",
        "number": 1234,
        "complement": "5 andar",
        "district": "Jardim Paulistano",
        "postal_code": "06650030",
        "city": "Sao Paulo",
        "state": "SP",
        "country": "BRA"
    }
    pg.extra_amount = 12.70
    pg.redirect_url = "http://meusite.com/obrigado"
    pg.notification_url = "http://meusite.com/notification"
    return pg
