from flask import Flask
from flask_login import LoginManager
from HoverSpace.searching import Searching
from HoverSpace.tags import Tag

app = Flask(__name__)
app.config.from_object('HoverSpace.config.DevelopmentConfig')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

srch = Searching(10**9 + 7, 9999991, 31, 97)
srch.add_all()

tag_choices = ['Science', 'Technology', 'Travel', 'Fiction', 'Education', 'Government', 'Weather', 'Politics', 'Current Affairs', 'History', 'Nature', 'Food', 'Outing']
for tags in tag_choices:
	t = Tag(tags)

from HoverSpace import views, questions
