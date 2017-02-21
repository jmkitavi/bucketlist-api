import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "verynotsecret"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres@localhost/bucketlist'

class StagingConfig(Config):
    DEVELOPMENT = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True


class TestingConfig(Config):
    TESTING = True
    # sqlite database for testing
    # SQLALCHEMY_DATABASE_URI = 'sqlite://'

configuration = {
    'staging': StagingConfig,
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': Config,
    'SECRET_KEY': "SECRET_KEY"
}