_config = {
    'frontend': {
        'url': 'http://localhost:8080/',
        'tags': ['frontend'],
        'transitions': [
            {
                'query': lambda tags: True,
                'next_module': 'greaterA'
            }
        ]
    },
    'greaterA': {
        'url': 'http://localhost:3010/',
        'tags': ['greaterA', 'A'],
        'transitions': [
            {
                'query': lambda tags: 'A' in tags,
                'next_module': 'evenA'
            },
            {
                'query': lambda tags: 'A' not in tags,
                'next_module': 'evenB'
            }
        ]
    },
    'evenA': {
        'url': 'http://localhost:3030/',
        'tags': ['evenA', 'leerA'],
        'transitions': [
            {
                'query': lambda tags: 'leerA' in tags,
                'next_module': 'inbox'
            }
        ]
    },
    'evenB': {
        'url': 'http://localhost:3020/',
        'tags': ['evenB', 'leerB'],
        'transitions': [
            {
                'query': lambda tags: 'leerB' in tags,
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

from logging import error


class Transition(object):
    """Clase para facilitar la utilizacion de un diccionario de la forma:
    {
        'query': lambda tags: True,
        'next_module': 'proxima_etiqueta_modulo'
    }
    """
    def __init__(self, query, next_module):
        if None in (query, next_module):
            error('Para "Transition" ningún argumento puede ser nulo.')
        self.query = query
        self.next_module = next_module


class Module(object):
    """Clase para facilitar la utilizacion de un diccionario de la forma:
    {
        'url': 'http://www.example.com',
        'tags': ['Tag1', 'Tag2'],
        'transitions': [...]
    }
    """
    def __init__(self, url, tags, transitions):
        if None in (url, tags, transitions):
            error('Para "Module" ningún argumento puede ser nulo.')
        self.url = url
        self.tags = tags
        self.transitions = transitions


def get_config():
    """Devolver un diccionario en el que los valores son
    de tipo Module

    Returns:
        dict -- Diccionario de la forma {key: instance of Module}
    """
    new_config = {}
    for key in _config:
        _module = _config[key]
        try:
            url = _module['url']
            tags = _module['tags']
            _transitions = _module['transitions']
        except KeyError:
            error(f'El modulo {_module} no tiene "url", "tags" o \
                  "transitions".')
        transitions = []
        for _transition in _transitions:
            try:
                _query = _transition['query']
                _next_module = _transition['next_module']
            except KeyError:
                error(f'El módulo {_module} tiene una transición \
                      sin "query" o "next_module".')
            transition = Transition(_query, _next_module)
            transitions.append(transition)
        module = Module(url, tags, transitions)
        new_config[key] = module
    return new_config
