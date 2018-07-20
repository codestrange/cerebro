from .config import config

def process(message):
    """Actualizar la base de datos de los mensajes y buscar en el
    diccionario de configuración el próximo módulo al que
    transferirle el mensaje.

    Arguments:
        message {tuple} -- Tupla de tres elementos. Conteniendo
        en este orden: etiqueta del módulo procedente, id del
        mensaje y lista de etiquetas del mensaje.
    """
    pass

def get_message():
    """Obtiene un mensaje de la cola de mensajes a procesar.

    Returns:
        tuple -- Tupla de tres elementos. Conteniendo
        en este orden: etiqueta del módulo procedente, id del
        mensaje y lista de etiquetas del mensaje.
    """
    return None

def put_message(message):
    """Inserta un mensaje en la cola de mensajes a procesar.

    Arguments:
        message {tuple} -- Tupla de tres elementos. Conteniendo
        en este orden: etiqueta del módulo procedente, id del
        mensaje y lista de etiquetas del mensaje.
    """
    pass

# Hay que hacer este metodo asincrónico
def start_core():
    """Controla el proceso de perdir los mensajes de la cola de
    mensajes a procesar y procesarlos.
    """
    pass
