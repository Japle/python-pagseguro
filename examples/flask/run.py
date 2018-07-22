
from flask_seguro import create_app

app = create_app('development')

@app.shell_context_processor
def make_shell_context():
    return dict(app=app)