from os import getenv
from app import create_app
from app.models import db, Message
from app.core import start_core

app = create_app(getenv('FLASK_CONFIG') or 'default')
start_core()

@app.cli.command()
def test():
    """Run the unit tests."""
    from unittest import TestLoader, TextTestRunner
    tests = TestLoader().discover('tests')
    TextTestRunner(verbosity=2).run(tests)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Message=Message)
