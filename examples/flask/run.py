#!/usr/bin/env python
from flask_seguro import app
import os

if __name__ == "__main__":
    config_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'settings.cfg')
    app.config.from_pyfile(config_file)
    app.run()
