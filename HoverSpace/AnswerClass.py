import datetime
from HoverSpace.models import ANSWERS_COLLECTION, QUESTIONS_COLLECTION
from HoverSpace.user import User

class Answers():
    #  quesID, short_description, long_description, posetdBy, timestamp, ansID, upvotes, downvotes
    def __init__(self, posetdBy, quesID, ansText):
        self.posetdBy = posetdBy
        self.timestamp = datetime.datetime.utcnow()
        self.ansText = ansText
        self.quesID = quesID


    def post_answer(self):
        ansID = ANSWERS_COLLECTION.insert_one({
                    'posetdBy': self.posetdBy, 'quesID': self.quesID,
                    'ansText': self.ansText, 'timestamp': self.timestamp,
                    'quesID': []}).inserted_id

        usr = User(self.posetdBy)
        usr.update_answers(str(ansID))
        ques = QuestionMethods(quesID)
        ques.update_answers(str(ansID))
        return ansID

class AnswerMethods():
    def __init__(self, quesID):
        self.quesID = quesID

    def get_answers(quesID):
        #answers = []
        answers = QUESTION_COLLECTION.find_one({'_id': quesID})['ansID']
        ans = []
        ans_obj = ANSWERS_COLLECTION.find({'_id': answers})
        return ans_obj