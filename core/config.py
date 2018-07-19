config = {
    'etiqueta_modulo': {
        'url': 'http://www.example.com',
        'tags': ['Tag1', 'Tag2'],
        'transitions': [
            (lambda tags_list: True, 'proxima_etiqueta_modulo1'),
            (lambda tags_list: False, 'proxima_etiqueta_modulo2')
        ]
    }
}
