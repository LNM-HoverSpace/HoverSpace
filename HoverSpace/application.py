from flask import Flask
from flask_login import LoginManager
from HoverSpace.searching import Searching

app = Flask(__name__)
app.config.from_object('HoverSpace.config.DevelopmentConfig')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

srch = Searching(10**9 + 7, 9999991, 31, 97)

from HoverSpace import views, questions
