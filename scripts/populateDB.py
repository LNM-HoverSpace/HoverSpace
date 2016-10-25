from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import json

DATABASE_URI = os.getenv('MONGOLAB_URI')

database = MongoClient(DATABASE_URI)
database.drop_database(database.get_default_database())

db = database.get_default_database()

os.chdir('..')
basedir = os.path.abspath(os.curdir) + '/data/'

def parse_json(filename, collectionname):
    with open(filename, 'r') as f:
        parsed = json.loads(f.read())

    for record in parsed:
        try:
            x = str(record['_id']['$oid'])
            del record['_id']['$oid']
            record['_id'] = ObjectId(x)
        except TypeError:
            pass
        collectionname.insert(record, check_keys=False)

parse_json(basedir + 'answer.json', db.answers)
parse_json(basedir + 'question.json', db.questions)
parse_json(basedir + 'user.json', db.users)
