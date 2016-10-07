import datetime
from HoverSpace.models import QUESTIONS_COLLECTION

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
                    'posetdBy': self.posetdBy, 'timestamp': self.timestamp}).inserted_id

        return quesID
