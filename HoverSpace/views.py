from HoverSpace.application import app, lm, srch
import pymongo
import json
from flask import request, redirect, render_template, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from HoverSpace.models import USERS_COLLECTION, QUESTIONS_COLLECTION, ANSWERS_COLLECTION
from HoverSpace.questions import Question, QuestionMethods
from HoverSpace.answers import Answers, AnswerMethods, UpdateAnswers
from HoverSpace.user import User
from HoverSpace.forms import LoginForm, SignUpForm, QuestionForm, AnswerForm, SearchForm
from bson.objectid import ObjectId


@app.route('/')
@app.route('/home/', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if request.method == "POST":
        return redirect(url_for('search', s=form.srch_term.data))
    questions = QUESTIONS_COLLECTION.find({'flag': 'False'}).sort('timestamp', pymongo.DESCENDING)
    feed = list()
    for record in questions:
        try:
            story = {
                'short_description' : record['short_description'],
                'long_description': record['long_description'],
                'ques_url' : url_for('viewQuestion', quesID=str(record['_id'])),
                'postedBy': record['postedBy'],
                'ansCount': len(record['ansID']),
                'votes': record['votes'],
                'timestamp': record['timestamp']
            }
            if record['accepted_ans']:
                story['answer'] = ANSWERS_COLLECTION.find_one({'_id': ObjectId(record['accepted_ans'])})
            feed.append(story)
        except KeyError:
            pass
    return render_template('home.html', title='HoverSpace | Home', feed=feed, form=form)

@app.route('/search/<s>/', methods=['GET'])
def search(s):
    l = []
    for selected in srch.search(s):
        q = QuestionMethods(selected)
        l.append(q.getQuestion())
    return render_template('search.html', title='HoverSpace | Search', result=l)

@app.route('/profile/', methods=['GET'])
def profile():
    user = USERS_COLLECTION.find_one({'_id': current_user.get_id()})
    quesPosted = user['quesPosted']
    for i in range(len(quesPosted)):
        quesPosted[i] = ObjectId(quesPosted[i])
    ques = []
    for q in QUESTIONS_COLLECTION.find({'_id': {'$in': quesPosted}}):
        ques.append(q)
    data = {
        'userID': user['_id'],
        'fname': user['firstname'],
        'lname': user['lastname'],
        'email': user['email'],
        'karma': user['karma'],
        'quesPosted': ques
    }
    return render_template('profile.html', title='HoverSpace | Profile', data=data)

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

@app.route('/post-a-question/', methods=['GET', 'POST'])
@login_required
def postQuestion():
    form = QuestionForm()
    if request.method == 'POST':
        try:
            username = current_user.get_id()
            question = QUESTIONS_COLLECTION.find_one( {'short_description': form.short_description.data} )
            if question:
                flash("This question has already been asked", category='error')
                return render_template('post-a-question.html', title='HoverSpace | Post a Question', form=form)
            quesmet_obj = QuestionMethods('DUMMY_QUESTION')
            tags = quesmet_obj.getTags(form.tags)
            ques_obj = Question(username, form.short_description.data, form.long_description.data, tags)
            quesID = ques_obj.postQuestion()
            srch.add_string(quesID, form.short_description.data)
            flash("Your question has been successfully posted.", category='success')
            return redirect(url_for('viewQuestion', quesID=quesID))
        except KeyError:
            return redirect(url_for('login'))
    return render_template('post-a-question.html', title='HoverSpace | Post a Question', form=form)


@app.route('/question/<quesID>/', methods=['GET', 'POST'])
@login_required
def viewQuestion(quesID):
    form = AnswerForm()
    if request.method == 'POST':
        username = current_user.get_id()
        ans_obj = Answers(username, quesID, form.ans_text.data)
        ansID = ans_obj.post_answer()
        return redirect(url_for('viewQuestion', quesID=quesID))

    ques_obj = QuestionMethods(quesID)
    ques = ques_obj.getQuestion()
    ansmet_obj = AnswerMethods(quesID)
    ans = ansmet_obj.get_answers(quesID)
    return render_template('question.html', question=ques, answers=ans, form=form)

@app.route('/question/<quesID>/edit', methods=['GET', 'POST'])
def editQuestionDescription(quesID):
    form = QuestionForm()

@app.route('/question/<quesID>/vote/', methods=['POST'])
@login_required
def updateQuesVotes(quesID):
    rd = (request.data).decode('utf-8')
    data = json.loads(rd)
    voteType = data['voteType']
    print(voteType)

    ques_obj = QuestionMethods(quesID)
    postedBy = (ques_obj.getQuestion())['postedBy']

    if current_user.get_id() == postedBy:
        return json.dumps({'type': 'notAllowed'})

    usr = User(current_user.get_id())
    status = usr.voteQues(quesID, voteType)
    print(status)

    votesCount = ques_obj.updateVotes(status['votesChange'])

    usr = User(postedBy)
    usr.update_karma(status['votesChange'])
    print(status['type'], votesCount)
    return json.dumps({'type': status['type'], 'count': votesCount})


@app.route('/answer/<ansID>/vote/', methods=['POST'])
@login_required
def updateAnsVotes(ansID):
    rd = (request.data).decode('utf-8')
    data = json.loads(rd)
    voteType = data['voteType']
    print(voteType)

    ans_obj = UpdateAnswers(ansID)
    postedBy = (ans_obj.getAnswer())['postedBy']

    if current_user.get_id() == postedBy:
        return json.dumps({'type': 'notAllowed'})

    usr = User(current_user.get_id())
    status = usr.voteAns(ansID, voteType)
    print(status)

    votesCount = ans_obj.updateVotes(postedBy, status['votesChange'])

    usr = User(postedBy)
    usr.update_karma(status['votesChange'])
    print(status['type'], votesCount)
    return json.dumps({'type': status['type'], 'count': votesCount})


@app.route('/question/<quesID>/bookmark/', methods=['POST'])
@login_required
def setBookmark(quesID):
    usr = User(current_user.get_id())
    fl = usr.setBookmark(quesID)
    #print(fl)
    if fl:
        return json.dumps({'status': 'true', 'message': 'This question has been successfully bookmarked'})
    else:
        return json.dumps({'status': 'false', 'message': 'Bookmark removed'})


@app.route('/question/<quesID>/flag/', methods=['POST'])
@login_required
def setQuesFlag(quesID):
    usr = current_user.get_id()
    ques_obj = QuestionMethods(quesID)
    postedBy = (ques_obj.getQuestion())['postedBy']
    if usr == postedBy:
        return json.dumps({'flag': 'notAllowed', 'message': 'You cannot flag your own question'})
    fl = ques_obj.addFlaggedBy(usr, postedBy)
    if fl=='flagged':
        return json.dumps({'flag': 'flagged', 'message': 'You have marked this question inappropiate'})
    elif fl=='alreadyFlagged':
        ques_obj.removeFlag(usr)
        return json.dumps({'flag': 'flagRemoved', 'message': 'Flag removed'})
    else:
        return json.dumps({'flag': 'quesRemoved', 'message': 'This question has been marked inappropiate by more than 10 users, so it is removed'})


@app.route('/answer/<ansID>/flag/', methods=['POST'])
@login_required
def setAnsFlag(ansID):
    usr = current_user.get_id()
    ans_obj = UpdateAnswers(ansID)
    postedBy = (ans_obj.getAnswer())['postedBy']
    if usr == postedBy:
        return json.dumps({'flag': 'notAllowed', 'message': 'You cannot flag your own answer'})
    fl = ans_obj.addFlaggedBy(usr, postedBy)
    if fl=='flagged':
        return json.dumps({'flag': 'flagged', 'message': 'You have marked this answer inappropiate'})
    elif fl=='alreadyFlagged':
        ans_obj.removeFlag(usr)
        return json.dumps({'flag': 'flagRemoved', 'message': 'Flag removed'})
    else:
        return json.dumps({'flag': 'quesRemoved', 'message': 'This answer has been marked inappropiate by more than 10 users, so it is removed'})

@app.route('/question/<quesID>/setAccepted/<ansID>', methods=['POST'])
@login_required
def setAcceptedAns(quesID, ansID):
    usr = current_user.get_id()
    ans_obj = UpdateAnswers(ansID)
    postedBy = (ans_obj.getAnswer())['postedBy']
    if usr != postedBy:
        return json.dumps({'status': 'notAllowed', 'message': 'You are not allowed to set this answer as accepted.'})
    ques_obj = QuestionMethods(quesID)
    if str(ques_obj.getAcceptedAns()) == ansID:
        ques_obj.removeAcceptedAns()
        return json.dumps({'status': 'removed', 'message': 'Accepted answer removed'})
    else:
        ques_obj.setAcceptedAns(ansID)
        return json.dumps({'status': 'set', 'message': 'You have marked this answer as accepted'})

@lm.user_loader
def load_user(username):
    u = USERS_COLLECTION.find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
