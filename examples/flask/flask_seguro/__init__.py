from flask import Flask
from flask_bootstrap import Bootstrap
from config import config

bootstrap = Bootstrap()

def create_app(config_name):
    """ Create Flask class instance for app """
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, '{0} not exists in current context'.format(config_name)))

    # instance middleware
    bootstrap.init_app(app)
    
    # call controllers
    from .controllers.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app