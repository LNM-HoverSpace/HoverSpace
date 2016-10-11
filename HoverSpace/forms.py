from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class SignUpForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(min=4, max=25)])
    email = StringField('Email Address', [DataRequired(), Email(), Length(min=6, max=35)])
    firstname = TextField("First name", [DataRequired()])
    lastname = TextField("Last name", [DataRequired()])
    password = PasswordField('Password', [DataRequired(), Length(min=6)])


class QuestionForm(FlaskForm):
	short_description = TextAreaField('Short Desciption', validators=[DataRequired(), Length(max=100)])
	long_description = TextAreaField('Long Desciption', validators=[Length(max=500)])


class AnswerForm(FlaskForm):
	ans_text = TextAreaField('Write your answer here: ', description='Write your answer here', validators=[DataRequired(), Length(max=1000)])
