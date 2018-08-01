from unittest import TestCase
from app.core.config import _config, get_config


class ConfigTestCase(TestCase):
    def setUp(self):
        self.config = get_config()

    def test_get_config(self):
        # Comprobar si las llaves son iguales
        for key1, key2 in zip(_config, self.config):
            self.assertEqual(key1, key2)
        for key in _config:
            module1 = _config[key]
            module2 = self.config[key]
            # Comprobar si las urls son iguales
            self.assertEqual(module1['url'], module2.url)
            # Comprobar si los etiquetas son iguales
            for tag1, tag2 in zip(module1['tags'], module2.tags):
                self.assertEqual(tag1, tag2)
            # Comprobar si las transiciones son iguales
            for trans1, trans2 in zip(module1['transitions'], module2.transitions):
                self.assertEqual(trans1['query'], trans2.query)
                self.assertEqual(trans1['next_module'], trans2.next_module)
