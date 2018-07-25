from json import dumps
from queue import Queue, Empty, Full
from time import sleep
from logging import debug, error
from requests.api import post
from requests.exceptions import ConnectionError
from .config import get_config
from ..models import Message

config = get_config()
queue = Queue()

# El módulo dummy_threading.threading provee una interfaz igual a la del módulo
# threading porque threading utilizá el módulo _thread y este no es provisto por
# todas las plataformas.
try:
    from threading import Thread
except ImportError:
    from dummy_threading.threading import Thread

def process(message):
    """Actualizar la base de datos de los mensajes y buscar en el
    diccionario de configuración el próximo módulo al que
    transferirle el mensaje.

    Arguments:
        message {tuple} -- Tupla de tres elementos. Conteniendo
        en este orden: etiqueta del módulo procedente, id del
        mensaje y lista de etiquetas del mensaje.
    """
    try:
        prev_module = message[0]
        id_message = message[1]
        tags_message = message[2]
    except IndexError:
        # Lanzar excepción si la tupla message no tiene 3 elementos
        error('La tupla "message" pasada como argumento no tiene 3 elementos.')

    try:
        # Obtener mensaje de la base de datos con el id = id_message
        message = Message.objects.get(id=id_message)
    except Exception:
        # Lanzar excepción si no se encontró el mensaje en la base de datos
        error(f'El mensaje con id={id_message} no existe en la base de datos.')

    # Guardar en la base de datos las nuevas etiquetas del mensaje
    for tag in tags_message:
        if tag not in message.tags:
            message.tags.append(tag)
    message.save()
    tags_message = message.tags
    text_message = message.text

    # Obtener el modulo en la configuración
    try:
        prev_module = config[prev_module]
    except KeyError:
        error(f'No existe el módulo {prev_module} en el archivo de configuración.')

    # Revizar que transiciones se pueden realizar y hacerlas
    for transition in prev_module.transitions:
        # url es la dirección a la que hay que hacerle POST
        # si la transición se debe realizar
        try:
            url_next_module = config[transition.next_module].url
        except KeyError:
            error('No existe el módulo {0} en el archivo de configuración.'
                  .format(transition.next_module))
        # query es una expresión lamda que resive como parámetro
        # la lista de etiquetas y retorna True si se puede hacer
        # la transición (si retorna False no se puede)
        if transition.query(tags_message):
            # Realizar POST a la url
            obj = {'id': str(id_message), 'text': text_message, 'tags': tags_message}
            try:
                post(url_next_module, json=dumps(obj))
            except ConnectionError:
                error('No se pudo establecer la conexión con el módulo "{0}" con la url: "{1}"'
                      .format(transition.next_module, url_next_module))


def get_message():
    """Obtiene un mensaje de la cola de mensajes a procesar.

    Returns:
        tuple -- Tupla de tres elementos. Conteniendo
        en este orden: etiqueta del módulo procedente, id del
        mensaje y lista de etiquetas del mensaje.
    """
    debug('Obteniendo mensaje ...')
    try:
        message = queue.get(timeout=1)
        debug('Procesando mensaje ...')
        process(message)
    except Empty:
        debug('Cola sin mensajes ...')


def put_message(message):
    """Inserta un mensaje en la cola de mensajes a procesar.

    Arguments:
        message {tuple} -- Tupla de tres elementos. Conteniendo
        en este orden: etiqueta del módulo procedente, id del
        mensaje y lista de etiquetas del mensaje.
    """
    debug('Insertando mensaje ...')
    try:
        queue.put(message)
    except Full:
        debug('Cola completamente llena ...')


# Hay que hacer este metodo asincrónico
def start_core():
    """Controla el proceso de perdir los mensajes de la cola de
    mensajes a procesar y procesarlos.
    """
    while True:
        sleep(1)
        thread_get = Thread(target=get_message)
        thread_get.start()
