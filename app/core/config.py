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


class AttributeDict(dict):

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value


def get_config():
    """Devolver un diccionario en el que las llaves son atributos.

    Returns:
        dict -- Diccionario
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
            transition = AttributeDict(query=_query, next_module=_next_module)
            transitions.append(transition)
        module = AttributeDict(url=url, tags=tags, transitions=transitions)
        new_config[key] = module
    return new_config
