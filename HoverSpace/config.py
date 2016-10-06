import os
from pymongo import MongoClient

basedir = os.path.abspath(os.path.dirname(__file__))

DB_NAME = 'hoverspace'
DATABASE = MongoClient()[DB_NAME]

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
