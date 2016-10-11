import datetime
from HoverSpace.models import QUESTIONS_COLLECTION
from HoverSpace.user import User
from bson.objectid import ObjectId

class Question():
    #  quesID, short_description, long_description, posetdBy, timestamp, ansID, upvotes, downvotes, accepted_ans, flag
    def __init__(self, posetdBy, short_description, long_description=None, timestamp=None):
        self.posetdBy = posetdBy
        self.timestamp = datetime.datetime.utcnow()
        self.short_description = short_description
        self.long_description = long_description

    def post_question(self):
        quesID = QUESTIONS_COLLECTION.insert_one({
                    'posetdBy': self.posetdBy, 'short_description': self.short_description,
                    'long_description': self.long_description, 'timestamp': self.timestamp,
                    'ansID': [], 'votes' : 0, 'accepted_ans': None, 'flag': False}).inserted_id
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
        QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$addToSet': {'ansID': ansID}})

    def update_votes(self, username, vote=[1, -1]):
        QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$inc': {'votes': vote}})
        usr = User(username)
        usr.update_votes(vote)

    def set_accepted_ans(self, ansID, username):
        usr = (QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)}))['posetdBy']
        if username == usr:
            QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$set': {'accepted_ans': ansID}})

    def get_accepted_ans(self):
        return (QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)}))['accepted_ans']

    def set_flag(self, flag=False):
        QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$set': {'flag': flag}})

    def get_flag(self):
        return (QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)}))['flag']
