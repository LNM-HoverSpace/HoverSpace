from flask import Flask
#from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def hello_world():
    return 'Hello, World!'
#lm = LoginManager()
#lm.init_app(app)
#lm.login_view = 'login'
