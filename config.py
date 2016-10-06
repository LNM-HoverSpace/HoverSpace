from os import urandom
from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = urandom(24)

DB_NAME = 'hoverspace'
DATABASE = MongoClient()[DB_NAME]

DEBUG = True
