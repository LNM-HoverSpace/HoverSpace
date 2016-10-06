from pymongo import MongoClient

DB_NAME = 'hoverspace'
DATABASE = MongoClient()[DB_NAME]

USERS_COLLECTION = DATABASE.users
