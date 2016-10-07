from HoverSpace.app import app
from flask import request, redirect, session, render_template, url_for, flash
from HoverSpace.models import QUESTIONS_COLLECTION
from HoverSpace.user import User
from HoverSpace.forms import QuestionForm
from HoverSpace import QuestionClass

BASE_URL = 'http://127.0.0.1:5000/'

@app.route('post-a-question/', methods=['GET', 'POST'])
def post_question():
	form = QuestionForm()
	username = session['username']
	if username:
		question = QUESTIONS_COLLECTION.find_one( {'short_description': form.username.data} )
		if question:
			flash("This queston has already been asked", category='error')
		else:
			quesID = QuestionClass.Question(form.short_description.data, form.long_description.data, username, True)
			flash("Your question has been posted at " + BASE_URL + '/quesID', category='success')
	else:
		return redirect(url_for('login'))