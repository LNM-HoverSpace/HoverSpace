from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class SignUpForm(FlaskForm):

    username = StringField('Username', [DataRequired(), Length(min=4, max=25)])
    email = StringField('Email Address', [DataRequired(), Length(min=6, max=35)])
    firstname = TextField("First name", [DataRequired()])
    lastname = TextField("Last name", [DataRequired()])
    password = PasswordField('New Password', [DataRequired()])
    #confirm = PasswordField('Repeat Password', [DataRequired()])

    '''def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        user = USERS_COLLECTION.find_one( {"email": self.email} )
        if user:
            self.email.errors.append("That email is already taken!")
            return False

        user = USERS_COLLECTION.find_one( {"username": self.username} )
        if user:
            self.username.errors.append("That username is already taken!")
            return False

        return True'''
