import datetime
from HoverSpace.models import TAGS_COLLECTION
from HoverSpace.user import User
from bson.objectid import ObjectId

class Tag():
    def __init__(self, quesID, tags=[]):
        self.quesID = quesID
        self.tags = tags

    def addQuestion(self):
        for tag in self.tags:
            TAGS_COLLECTION.insert_one({'_id': tag}, {'addToSet': {'quesID': self.quesID}})
