import datetime
from HoverSpace.models import ANSWERS_COLLECTION, QUESTIONS_COLLECTION
from HoverSpace.user import User
from HoverSpace.QuestionClass import QuestionMethods
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
                    'quesID': self.quesID, 'votes': 0}).inserted_id

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

    def update_votes(self, username, vote=[1, -1]):
        ANSWERS_COLLECTION.find_one_and_update({'_id': ObjectId(self.ansID)}, {'$inc' : {'votes': vote}})
        usr = User(username)
        usr.update_karma(vote)