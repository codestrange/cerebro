_config = {
    'frontend': {
        'url': 'http://localhost:8080/',
        'tags': ['frontend'],
        'transitions': [
            {
                'query': lambda tags: True,
                'next_module': 'inbox'
            }
        ]
    },
    'inbox': {
        'url': 'http://localhost:3000/',
        'tags': ['inbox'],
        'transitions': []
    }
}


class Transition(object):
    """Clase para facilitar la utilizacion de un diccionario de la forma:
    {
        'query': lambda tags: True,
        'next_module': 'proxima_etiqueta_modulo'
    }

    Raises:
        Exception -- Lanza una excepción si algún argumento es nulo
    """
    def __init__(self, query, next_module):
        if query is None or next_module is None:
            raise Exception('Para Transition ningún argumento puede ser nulo.')
        self.query = query
        self.next_module = next_module


class Module(object):
    """Clase para facilitar la utilizacion de un diccionario de la forma:
    {
        'url': 'http://www.example.com',
        'tags': ['Tag1', 'Tag2'],
        'transitions': [...]
    }

    Raises:
        Exception -- Lanza una excepción si algún argumento es nulo
    """
    def __init__(self, url, tags, transitions):
        if url is None or tags is None or transitions is None:
            raise Exception('Para Module ningún argumento puede ser nulo.')
        self.url = url
        self.tags = tags
        self.transitions = transitions


def get_config():
    """Devolver un diccionario en el que los varlos son
    de tipo Module

    Returns:
        dict -- Diccionario de la forma {key: instance of Module}
    """
    new_config = {}
    for key in _config:
        _module = _config[key]
        url = _module['url']
        tags = _module['tags']
        transitions = []
        for _transitions in _module['transitions']:
            _query = _transitions['query']
            _next_module = _transitions['next_module']
            transition = Transition(_query, _next_module)
            transitions.append(transition)
        module = Module(url, tags, transitions)
        new_config[key] = module
    return new_config
