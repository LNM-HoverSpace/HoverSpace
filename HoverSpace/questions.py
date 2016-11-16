import datetime
from HoverSpace.models import QUESTIONS_COLLECTION
from HoverSpace.user import User
from bson.objectid import ObjectId

class Question():
    #  quesID, short_description, long_description, postedBy, timestamp, ansID, upvotes, downvotes, accepted_ans, flag
    def __init__(self, postedBy, short_description, long_description=None, tags=None, timestamp=None):
        self.postedBy = postedBy
        self.timestamp = datetime.datetime.utcnow()
        self.short_description = short_description
        self.long_description = long_description
        self.tags = tags

    def postQuestion(self):
        quesID = QUESTIONS_COLLECTION.insert_one({
                    'postedBy': self.postedBy, 'short_description': self.short_description,
                    'long_description': self.long_description, 'timestamp': self.timestamp,
                    'ansID': [], 'commentID': [], 'votes': 0, 'tags': [], 'accepted_ans': None,
                    'flaggedBy': [], 'flag': 'False'
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

    def updateVotes(self, vote):
        QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$inc': {'votes': vote}})
        votes = (QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)}))['votes']
        return votes

    def update_comments(self, commentID):
        QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$addToSet': {'commentID': commentID}})

    def getTags(self, quesTags):
        pass

    def setAcceptedAns(self, ansID, username):
        usr = (QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)}))['postedBy']
        if username == usr:
            QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$set': {'accepted_ans': ansID}})

    def getAcceptedAns(self):
        return (QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)}))['accepted_ans']

    def setFlag(self, flag):
        QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$set': {'flag': flag}})
            
    def getFlag(self):
        return (QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)}))['flag']

    def addFlaggedBy(self, userID, postedBy):
        ques_obj = QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)})
        flags = ques_obj['flaggedBy']
        votes = ques_obj['votes']
        if userID in flags:
            return "alreadyFlagged"
        QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$addToSet': {'flaggedBy': userID}})
        if (len(flags)>=10):
            flag = "True"
            self.setFlag(postedBy, votes, flag)
            usr = User(postedBy)
            usr.update_karma(-votes)
            return "quesRemoved"
        return "flagged"

    def removeFlag(self, userID):
        QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$pull': {'flaggedBy': userID}})

    def getAcceptedAns(self):
        return (QUESTIONS_COLLECTION.find_one({'_id': ObjectId(self.quesID)}))['accepted_ans']

    def setAcceptedAns(self, ansID):
        QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$set': {'accepted_ans': ObjectId(ansID)}})

    def removeAcceptedAns(self):
        QUESTIONS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$set': {'accepted_ans': None}})        