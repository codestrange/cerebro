from json import loads
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
    module = json['module']
    message = Message()
    message.text = json['text']
    message.tags = json['tags']
    message.save()
    thread = Thread(target=put_message, args=((module, message.id, message.tags), ))
    thread.start()
    return jsonify({'id': str(message.id)})
