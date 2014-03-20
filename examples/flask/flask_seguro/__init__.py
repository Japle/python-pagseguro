from flask import Flask
app = Flask(__name__)
app.secret_key = 'segredo'

import flask_seguro.views
