from flask import Flask
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

app = Flask(__name__)

bootstrap.init_app(app)

import flask_seguro.views  # noqa
