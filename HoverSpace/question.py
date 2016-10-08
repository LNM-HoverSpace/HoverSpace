from HoverSpace.application import app
from flask import request, redirect, session, render_template, url_for, flash
from flask_login import login_required, current_user
from HoverSpace.models import QUESTIONS_COLLECTION
from HoverSpace.forms import QuestionForm, AnswerForm
from HoverSpace.QuestionClass import Question, QuestionMethods
from HoverSpace.AnswerClass import Answers, AnswerMethods
from HoverSpace.user import User            #check

@app.route('/post-a-question/', methods=['GET', 'POST'])
@login_required
def post_question():
    form = QuestionForm()
    if request.method == 'POST':
        try:
            username = current_user.get_id()
            question = QUESTIONS_COLLECTION.find_one( {'short_description': form.short_description.data} )
            if question:
                flash("This queston has already been asked", category='error')
                return render_template('post-a-question.html', title='HoverSpace | Post a Question', form=form)
            ques_obj = Question(username, form.short_description.data, form.long_description.data)
            quesID = ques_obj.post_question()
            flash("Your question has been successfully posted.", category='success')
            #print(quesID)
            return redirect(url_for('view_question', quesID=quesID))
        except KeyError:
            return redirect(url_for('login'))
    return render_template('post-a-question.html', title='HoverSpace | Post a Question', form=form)


@app.route('/questions/<quesID>', methods=['GET', 'POST'])
@login_required
def view_question(quesID):
    form = AnswerForm()
    ques_obj = QuestionMethods(quesID)
    ques = ques_obj.get_question()
    ans_obj = AnswerMethods(quesID)
    ans = ans_obj.get_answers(quesID)
    print(ans)
    if request.method == 'POST':
        username = current_user.get_id()
        ans_obj = Answers(username, quesID, form.ans_text.data)
        ansID = ans_obj.post_answer()
    return render_template('question.html', question=ques, answers=ans, form=form)