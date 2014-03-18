from flask import Flask
app = Flask("PagSeguroExample")
app.secret_key = 'segredo'

import flask_seguro.views
