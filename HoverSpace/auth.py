from HoverSpace.application import app, lm
import pymongo
from flask import request, redirect, render_template, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from HoverSpace.models import USERS_COLLECTION, QUESTIONS_COLLECTION, ANSWERS_COLLECTION
from HoverSpace.user import User
from HoverSpace.forms import LoginForm, SignUpForm
from bson.objectid import ObjectId
from HoverSpace.question import view_question

@app.route('/')
@app.route('/home/', methods=['GET', 'POST'])
def home():
    questions = QUESTIONS_COLLECTION.find().sort('timestamp', pymongo.ASCENDING)
    feed = list()
    for record in questions:
        try:
            story = {
                'short_description' : record['short_description'],
                'long_description': record['long_description'],
                'ques_url' : url_for('view_question', quesID=str(record['_id']))
            }
            if record['accepted_ans']:
                story['answer'] = ANSWERS_COLLECTION.find_one({'_id': ObjectId(accepted_ans)})
            feed.append(story)
        except KeyError:
            pass
    return render_template('home.html', title='HoverSpace | Home', feed=feed)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = USERS_COLLECTION.find_one({ "_id": form.username.data })
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj, remember=True)
            flash("Logged in successfully!", category='success')
            return redirect(url_for('home'))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='HoverSpace | Login', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = USERS_COLLECTION.find_one( {'email': form.email.data} )
        if user:
            flash("You have already signed up from this email id", category='error')
        else:
            user = USERS_COLLECTION.find_one( {'_id': form.username.data} )
            if user:
                flash("That username has already been taken", category='error')
            else:
                user_obj = User(form.username.data, form.email.data, form.firstname.data,
                        form.lastname.data, form.password.data, db=True)
                flash("SignUp successfull!", category='success')
                return redirect(url_for('login'))
    return render_template('signup.html', title='HoverSpace | Signup', form=form)

@lm.user_loader
def load_user(username):
    u = USERS_COLLECTION.find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
