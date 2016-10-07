from HoverSpace.application import app
from flask import request, redirect, session, render_template, url_for, flash
from HoverSpace.models import QUESTIONS_COLLECTION
from HoverSpace.user import User
from HoverSpace.forms import QuestionForm
from HoverSpace.QuestionClass import Question
from HoverSpace import auth

BASE_URL = 'http://127.0.0.1:5000/'

@app.route('/post-a-question/', methods=['GET', 'POST'])
def post_question():
	form = QuestionForm()
	if request.method == 'POST':
		try:
			username = session['username']
			if username:
				question = QUESTIONS_COLLECTION.find_one( {'short_description': form.short_description.data} )
				if question:
					flash("This queston has already been asked", category='error')
					return render_template('post-a-question.html', title='HoverSpace | Post a Question', form=form)
				else:
					ques_obj = Question(username, form.short_description.data, form.long_description.data)
					quesID = ques_obj.post_question()
					flash("Your question has been successfully posted.", category='success')
					return redirect(url_for('home') + 'questions/' + str(quesID))
					#return redirect(BASE_URL + 'quesID/')
			else:
				return redirect(url_for('login'))
		except KeyError:
			return redirect(url_for('login'))
	return render_template('post-a-question.html', title='HoverSpace | Post a Question', form=form)