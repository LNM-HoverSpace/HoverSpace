from HoverSpace.application import app
from flask import request, redirect, render_template, url_for, flash
from flask_login import current_user
from HoverSpace.models import ANSWERS_COLLECTION
from HoverSpace.user import User
from HoverSpace.forms import AnswerForm
#from HoverSpace.AnswerClass import Answer

'''@app.route('/question/<quesID>', methods=['GET', 'POST'])
def post_answer():
	form = AnswerForm()
    ques_obj = QuestionMethods(quesID)
    ques = ques_obj.get_question()
	if request.method == 'POST':
		try:
			username = current_user.get_id()
			if username:
				ans_obj = Answer(username, quesID, form.ans_text.data)
				ansID = ans_obj.post_answer()
				flash("Your answer has been successfully posted.", category='success')
				return redirect(url_for('post_answer') + quesID + '/')
			else:
				return redirect(url_for('login'))
		except KeyError:
			return redirect(url_for('login'))
	return redirect(url_for('post_answer') + quesID + '/')


#@app.route('/questions/<>')
#def viewQuestion():
#	pass
'''