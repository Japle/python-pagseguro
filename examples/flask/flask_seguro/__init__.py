""" Application Skeleton """
from flask import Flask
from flask_bootstrap import Bootstrap
from config import config

BOOTSTRAP = Bootstrap()


def create_app(config_name):
    """ Factory Function """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    BOOTSTRAP.init_app(app)

    # call controllers
    from flask_seguro.controllers.main import main as main_blueprint

    app.register_blueprint(main_blueprint)
    return app
