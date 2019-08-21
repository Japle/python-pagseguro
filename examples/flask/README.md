FlaskSeguro
==========
Exemplo de integração do python-pagseguro utilizando Flask.

Instalando a virtualenv
==========

```bash
pip install -U pip
pip install virtualenv
```
Caso tenha alguma dúvida sobre a virtualenv ou ocorra algum erro no momento da instalação, verifique a documentação [clicando aqui](https://virtualenv.pypa.io/en/stable/installation/).

Download e Instalação
==========
Testado com o Python 3.6 >.

```bash
virtualenv -p python3 env
source env/bin/activate
git clone https://github.com/rochacbruno/python-pagseguro.git
cd python-pagseguro/examples/flask/
pip install -r requirements.txt
```

Execução
==========
Com o terminal aberto e setado na pasta _python-pagseguro/examples/flask_, execute o seguinte comando:

```bash
env FLASK_APP=run.py flask run
```

Configuração
==========
Altere o _settings.cfg_, ele possui as seguintes configurações por padrão:

```
EXTRA_AMOUNT = 12.12
REDIRECT_URL = "http://meusite.com/obrigado"
NOTIFICATION_URL = "http://meusite.com/notification"
EMAIL = "seuemail@dominio.com"
TOKEN = "ABCDEFGHIJKLMNO"
SECRET_KEY = "s3cr3t"
```

Caso as alterações não sejam feitas, o PagSeguro te notificará de erro retornando a seguinte mensagem _Código de checkout inválido_:

![](https://raw.githubusercontent.com/JacksonOsvaldo/python-pagseguro/master/examples/flask/screenshots/screen4.png)



Testes
==========
Para executar alguns testes e verificar se está tudo certo com a aplicação, execute:

```bash
./tests.py
```

Caso retorne algum erro, dê permissão ao arquivo e reexecute o comando acima. Assim:

```bash
chmod +x tests.py
./tests.py
```

Telas
==========
![](https://raw.githubusercontent.com/shyba/python-pagseguro/master/examples/flask/screenshots/screen1.png)
![](https://raw.githubusercontent.com/shyba/python-pagseguro/master/examples/flask/screenshots/screen2.png)
![](https://raw.githubusercontent.com/shyba/python-pagseguro/master/examples/flask/screenshots/screen3.png)
