import datetime
from HoverSpace.models import USERS_COLLECTION
from HoverSpace import User

class Question():

    #  quesID, short_description, long_description, posetdBy, timestamp, ansID, upvotes, downvotes
    def __init__(self, short_description, long_description=None, posetdBy, db=False):
        self.short_description = short_description
        self.long_description = long_description
        self.posetdBy = posetdBy
        self.timestamp = datetime.datetime.utcnow()
        if db:
            quesID = QUESTIONS_COLLECTION.insert_one({
                        'short_description': self.short_description, 'long_description': self.long_description,
                        'posetdBy': self.posetdBy, 'timestamp': self.timestamp}).inserted_id
            
            return quesID

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    '''def set_password(self, password):
        self.password = generate_password_hash(password)
        USERS_COLLECTION.update_one({'username': self.username, {'password': self.password}})'''

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

