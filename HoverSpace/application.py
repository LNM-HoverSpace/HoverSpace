from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('HoverSpace.config.DevelopmentConfig')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from HoverSpace import views, questions
