import datetime
from HoverSpace.models import QUESTIONS_COLLECTION
from HoverSpace.user import User
from bson.objectid import ObjectId

class Question():
    #  quesID, short_description, long_description, postedBy, timestamp, ansID, upvotes, downvotes, accepted_ans, flag
    def __init__(self, postedBy, short_description, long_description=None, timestamp=None):
        self.postedBy = postedBy
        self.timestamp = datetime.datetime.utcnow()
        self.short_description = short_description
        self.long_description = long_description

    def postQuestion(self):
        quesID = QUESTIONS_COLLECTION.insert_one({
                    'postedBy': self.postedBy, 'short_description': self.short_description,
                    'long_description': self.long_description, 'timestamp': self.timestamp,
                    'ansID': [], 'commentID': [], 'votes' : 0, 'accepted_ans': None, 'flag': False
                }).inserted_id
        usr = User(self.postedBy)
        usr.update_questions(str(quesID))
        return quesID

class QuestionMethods():
    def __init__(self, quesID):
        self.quesID = quesID

    def getQuestion(self):
        ques_dict = QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)})
        return ques_dict

    def insert_answers(self, ansID):
        QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$addToSet': {'ansID': ansID}})

    def update_votes(self, username, vote=[1, -1]):
        QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$inc': {'votes': vote}})
        usr = User(username)
        usr.update_karma(vote)

    def update_comments(self, commentID):
        QUESTION_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$addToSet': {'commentID': commentID}})

    def setAcceptedAns(self, ansID, username):
        usr = (QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)}))['postedBy']
        if username == usr:
            QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$set': {'accepted_ans': ansID}})

    def getAcceptedAns(self):
        return (QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)}))['accepted_ans']

    def setFlag(self, flag=False):
        QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$set': {'flag': flag}})

    def getFlag(self):
        return (QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)}))['flag']
