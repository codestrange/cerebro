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


def send_to_core(module, message_id, message_tags):
    thread = Thread(target=put_message, args=((module, message_id, message_tags), ))
    thread.start()


@api.route('/', methods=['GET'])
def index():
    return jsonify('Bienvenido a la API de Cerebro!')


@api.route('/new_message', methods=['POST'])
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
    send_to_core(module, message.id, message.tags)
    return jsonify({'id': str(message.id)}), 201


@api.route('/message', methods=['POST'])
def incoming_message():
    json = loads(request.json)
    module = json.get('module')
    tags = json.get('tags')
    message_id = json.get('id')
    # Comprobar si el json recibido es correcto
    if None in (module, tags, message_id):
        error('Mensaje sin "id", module" o "tags".')
        return jsonify({'error': 'id, module and tags are required'}), 400
    send_to_core(module, message_id, tags)
    return jsonify({'id': str(message_id)}), 201
