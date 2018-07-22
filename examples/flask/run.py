#!/usr/bin/env python
from flask_seguro import create_app
import os

app = create_app(os.environ.get('CONFIG_APP_DEFAULT') or 'development')

@app.shell_context_processor
def make_shell_context():
    return dict(app=app)