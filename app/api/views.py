from json import loads
from logging import error
from flask import jsonify, request
from . import api
from ..core import put_message
from ..models import Message

# El módulo dummy_threading.threading provee una interfaz igual a la del módulo
# threading porque threading utilizá el módulo _thread y este no es provisto por
# todas las plataformas.
try:
    from threading import Thread
except ImportError:
    from dummy_threading.threading import Thread


@api.route('/', methods=['GET'])
def index():
    return jsonify('Bienvenido a la API de Cerebro!')


@api.route('/message', methods=['POST'])
def new_message():
    json = loads(request.json)
    module = json.get('module')
    text = json.get('text')
    tags = json.get('tags')
    # Comprobar si el json recibido es correcto
    if None in (module, text, tags):
        error('Nuevo mensaje sin "module", "text" o "tags".')
        return jsonify({'error': 'module, text and tags are required'}), 400
    message = Message(text=text, tags=tags)
    message.save()
    thread = Thread(target=put_message, args=((module, message.id, message.tags), ))
    thread.start()
    return jsonify({'id': str(message.id)}), 201
