from werkzeug.security import check_password_hash, generate_password_hash
from HoverSpace.models import USERS_COLLECTION
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, username, email=None, firstname=None, lastname=None, password=None, db=False):
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        if db:
            USERS_COLLECTION.insert_one({
                '_id': self.username, 'email': self.email,
                'firstname': self.firstname, 'lastname': self.lastname,
                'password': generate_password_hash(self.password),
                'quesPosted': [], 'ansPosted': [], 'bookmarks': [],
                'karma': 0, 'voted_ques': [], 'voted_ans': [] })

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def update_questions(self, quesID):
        USERS_COLLECTION.find_one_and_update({'_id': self.username}, {'$addToSet': {'quesPosted': quesID}})

    def update_answers(self, ansID):
        USERS_COLLECTION.find_one_and_update({'_id': self.username}, {'$addToSet': {'ansPosted': ansID}})

    def update_karma(self, karma=[1, -1]):
        USERS_COLLECTION.find_one_and_update({'_id': self.username}, {'$inc': {'karma': karma}})

    def set_bookmarks(self, quesID):
        USERS_COLLECTION.find_one_and_update({'_id': self.username}, {'$addToSet': {'bookmarks': quesID}})

    def vote_ques(self, quesID, vote):
        USERS_COLLECTION.find_one_and_update({'_id': self.username}, {'$addToSet': {'voted_ques': {'quesID': quesID, 'vote': vote}}})

    def vote_ans(self, ansID, vote):
        USERS_COLLECTION.find_one_and_update({'_id': self.username}, {'$addToSet': {'voted_ans': {'ansID': ansID, 'vote': vote}}})

    def alreadyVotedQues(self, quesID):
        try:
            voted_ques = list()
            voted_ques = (USERS_COLLECTION.find_one({'_id': self.username}))['voted_ques']
            for ques in voted_ques:
                if ques['quesID'] == quesID:
                    return True
            return False
        except:
            return False

    def alreadyVotedAns(self, ansID):
        try:
            voted_ans = list()
            voted_ans = (USERS_COLLECTION.find_one({'_id': self.username}))['voted_ans']
            for ans in voted_ans:
                if ans['ansID'] == ansID:
                    return True
            return False
        except:
            return False

    '''def set_password(self, password):
        self.password = generate_password_hash(password)
        USERS_COLLECTION.update_one({'username': self.username, {'password': self.password}})'''

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

