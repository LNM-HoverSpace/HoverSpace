import datetime
from HoverSpace.models import ANSWERS_COLLECTION, QUESTIONS_COLLECTION
from HoverSpace.user import User
from HoverSpace.questions import QuestionMethods
from bson.objectid import ObjectId

class Answers():
    #  quesID, short_description, long_description, postedBy, timestamp, ansID, upvotes, downvotes
    def __init__(self, postedBy, quesID, ansText):
        self.postedBy = postedBy
        self.timestamp = datetime.datetime.utcnow()
        self.ansText = ansText
        self.quesID = quesID


    def post_answer(self):
        ansID = ANSWERS_COLLECTION.insert_one({
                    'postedBy': self.postedBy, 'quesID': self.quesID,
                    'ansText': self.ansText, 'timestamp': self.timestamp,
                    'quesID': self.quesID, 'commentID': [], 'votes': 0,
                    'flaggedBy': [], 'flag': 'False'}).inserted_id

        usr = User(self.postedBy)
        usr.update_answers(str(ansID))
        ques = QuestionMethods(self.quesID)
        ques.insert_answers(str(ansID))
        return ansID

class AnswerMethods():
    def __init__(self, quesID):
        self.quesID = quesID

    def get_answers(self, quesID):
        answers = []
        try:
            ans_obj = (QUESTIONS_COLLECTION.find_one({'_id': ObjectId(quesID)}))['ansID']
            for answer in ans_obj:
                answers.append(ANSWERS_COLLECTION.find_one({'_id': ObjectId(answer)}))
        except TypeError:
            answers = []
        return answers


class UpdateAnswers(object):
    def __init__(self, ansID):
        self.ansID = ansID

    def getAnswer(self):
        return (ANSWERS_COLLECTION.find_one({'_id': ObjectId(self.ansID)}))

    def update_comments(self, commentID):
        ANSWERS_COLLECTION.find_one_and_update({'_id': ObjectId(self.ansID)}, {'$addToSet': {'commentID': commentID}})

    def updateVotes(self, username, vote):
        ANSWERS_COLLECTION.find_one_and_update({'_id': ObjectId(self.ansID)}, {'$inc' : {'votes': vote}})
        votes = (ANSWERS_COLLECTION.find_one({'_id': ObjectId(self.ansID)}))['votes']
        return votes

    def setFlag(self, flag):
        ANSWERS_COLLECTION.find_one_and_update({'_id': ObjectId(self.quesID)}, {'$set': {'flag': flag}})

    def getFlag(self):
        return (ANSWERS_COLLECTION.find_one({'_id': ObjectId(self.quesID)}))['flag']

    def addFlaggedBy(self, userID, postedBy):
        ans_obj = ANSWERS_COLLECTION.find_one({'_id': ObjectId(self.ansID)})
        flags = ans_obj['flaggedBy']
        votes = ans_obj['votes']
        if userID in flags:
            return "alreadyFlagged"
        ANSWERS_COLLECTION.find_one_and_update({'_id': ObjectId(self.ansID)}, {'$addToSet': {'flaggedBy': userID}})
        if (len(flags)>=10):
            flag = "True"
            self.setFlag(userID, votes, flag)
            usr = User(postedBy)
            usr.update_karma(-votes)
            return "quesRemoved"
        return "flagged"

    def removeFlag(self, userID):
        ANSWERS_COLLECTION.find_one_and_update({'_id': ObjectId(self.ansID)}, {'$pull': {'flaggedBy': userID}})
