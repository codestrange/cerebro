from os import getenv
from os.path import abspath, dirname

basedir = abspath(dirname(__file__))

class Config(object):
    SECRET_KEY = getenv('SECRET_KEY') or 'secret_key'

    MONGODB_DB = getenv('MONGODB_DB') or 'Cerebro'
    MONGODB_HOST = getenv('MONGODB_HOST') or 'localhost'
    MONGODB_PORT = getenv('MONGODB_PORT') or 27017

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
