import datetime
from HoverSpace.models import QUESTIONS_COLLECTION
from HoverSpace.user import User
from bson.objectid import ObjectId

class Question():
    #  quesID, short_description, long_description, posetdBy, timestamp, ansID, upvotes, downvotes
    def __init__(self, posetdBy, short_description, long_description=None, timestamp=None):
        self.posetdBy = posetdBy
        self.timestamp = datetime.datetime.utcnow()
        self.short_description = short_description
        self.long_description = long_description

    def post_question(self):
        quesID = QUESTIONS_COLLECTION.insert_one({
                    'short_description': self.short_description, 'long_description': self.long_description,
                    'posetdBy': self.posetdBy, 'timestamp': self.timestamp, 'ansID': []}).inserted_id
        usr = User(self.posetdBy)
        usr.update_questions(str(quesID))
        return quesID

class QuestionMethods():
    def __init__(self, quesID):
        self.quesID = quesID

    def get_question(self):
        ques_dict = QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)})
        return ques_dict

    def update_answers(self, ansID):
        print("updating")
        QUESTIONS_COLLECTION.update({'_id': self.quesID}, {'$addToSet': {'ansPosted': ansID}})
        QUESTIONS_COLLECTION.find_one_and_update({'_id': self.quesID}, {'$addToSet': {'ansPosted': ansID}})