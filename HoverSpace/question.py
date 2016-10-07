from HoverSpace.application import app
from flask import request, redirect, session, render_template, url_for, flash
from flask_login import login_required, current_user
from HoverSpace.models import QUESTIONS_COLLECTION
from HoverSpace.forms import QuestionForm, AnswerForm
from HoverSpace.QuestionClass import Question, QuestionMethods
from HoverSpace.AnswerClass import AnswerMethods

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
            return redirect(url_for('empty'))
            #return redirect(url_for('home') + 'questions/' + str(quesID))
        except KeyError:
            return redirect(url_for('login'))
    return render_template('post-a-question.html', title='HoverSpace | Post a Question', form=form)


@app.route('/questions/<quesID>/', methods=['GET', 'POST'])
@login_required
def view_question():
    form = AnswerForm()
    ques_obj = QuestionMethods(quesID)
    ques_obj.get_question()
    ans_obj = AnswerMethods(quesID)
    ans_obj.get_answers(quesID)
    render_template('question.html', ques=ques_obj, ans=ans_obj, form=form)