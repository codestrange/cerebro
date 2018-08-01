from os import getenv
from flask_script import Manager, Shell
from app import create_app
from app.models import db, Message
from app.core import start_core

app = create_app(getenv('FLASK_CONFIG') or 'default')

# El módulo dummy_threading.threading provee una interfaz igual a la del módulo
# threading porque threading utilizá el módulo _thread y este no es provisto por
# todas las plataformas.
try:
    from threading import Thread
except ImportError:
    from dummy_threading.threading import Thread

# Corriendo el módulo core en un hilo independiente al de flask
core_thread = Thread(target=start_core)
core_thread.start()


@app.cli.command()
def test():
    """Run the unit tests."""
    from unittest import TestLoader, TextTestRunner
    tests = TestLoader().discover('tests')
    TextTestRunner(verbosity=2).run(tests)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Message=Message)


# Shell de flask_script con IPython
manager = Manager(app)
manager.add_command(Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
