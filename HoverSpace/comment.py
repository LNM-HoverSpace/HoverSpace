from Hoverspace.models import COMMENT_COLLECTION
from HoverSpace.answers import UpdateAnswers
from HoverSpace.questions import QuestionMethod
from HoverSpace.users import User
from flask_login import current_user
import datetime

class Comment(object):

    def __init__(self, text, ID, postedBy=None, typee='q', timestamp=None):
        if not postedBy:
            postedBy = current_user.get_id()
        self.timestamp = datetime.datetime.utcnow()
        self.text = text
        self.type = typee
        self.postedBy = postedBy
        self.parentID = ID

    def postComment(self):
        commentID = COMMENT_COLLECTION.insert_one({
            'postedBy': self.postedBy,
            'text': self.text,
            'timestamp': self.timestamp,
            'type': self.type,
            'parentID': self.parentID
        })
        usr = User(self.postedBy)
        usr.update_comment(str(commentID))
        if self.type == 'q':
            q = QuestionMethod(self.parentID)
            q.update_comment(commentID)
        else:
            a = UpdateAnswers(self.parentID)
            a.update_comment(commentID)
        return commentID

