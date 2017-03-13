""" config/config"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY =os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres@localhost/bucketlist'

class Staging(Config):
    DEVELOPMENT = True


class Development(Config):
    DEVELOPMENT = True


class Testing(Config):
    TESTING = True
    # sqlite database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

configuration = {
    'staging': Staging,
    'testing': Testing,
    'development': Development,
    'default': Config,
    'SECRET_KEY': "SECRET_KEY"
}