import os
from pymongo import MongoClient

DATABASE_URI = os.getenv('MONGOLAB_URI') or 'hoverspace'

DATABASE = MongoClient(DATABASE_URI)
db = DATABASE.get_default_database()

USERS_COLLECTION = db.users
QUESTIONS_COLLECTION = db.questions
ANSWERS_COLLECTION = db.answers
