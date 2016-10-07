from HoverSpace.application import app
from flask import request, redirect, render_template, url_for, flash
from HoverSpace.models import ANSWERS_COLLECTION
from HoverSpace.user import User
from HoverSpace.forms import AnswerForm
from HoverSpace.AnswerClass import Answer
from HoverSpace import auth

@app.route('/question/<quesID>', methods=['GET', 'POST'])
def post_answer():
	form = AnswerForm()
	ques_obj = get_question(quesID)
	if request.method == 'POST':
		try:
			username = session['username']
			if username:
				ans_obj = Answer(username, quesID, form.ans_text.data)
				ansID = ans_obj.post_answer()
				flash("Your answer has been successfully posted.", category='success')
				return render_template('question_format.html', title='HoverSpace | ' + ques_obj.short_description, form=form)
			else:
				return redirect(url_for('login'))
		except KeyError:
			return redirect(url_for('login'))
	return render_template('question_format.html', title='HoverSpace |', form=form)


#@app.route('/questions/<>')
#def view_question():
#	pass