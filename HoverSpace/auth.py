from HoverSpace.application import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required
from HoverSpace.models import USERS_COLLECTION
from HoverSpace.user import User
from HoverSpace.forms import LoginForm, SignUpForm

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = USERS_COLLECTION.find_one({ "username": form.username.data })
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['username'])
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("empty"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = USERS_COLLECTION.find_one( {'username': form.username.data} )
        if user:
            flash("That email has already been taken", category='error')
        else:
            user = USERS_COLLECTION.find_one( {'email': form.email.data} )
            if user:
                flash("That username has already been taken", category='error')
            else:
                flash("SignUp successfull!", category='success')
                user_obj = User(form.username.data, form.email.data, form.firstname.data,
                        form.lastname.data, form.password.data, db=True)
                return redirect(url_for('login'))
    return render_template('signup.html', title='signup', form=form)

@app.route('/empty', methods=['GET', 'POST'])
@login_required
def empty():
    return render_template('empty.html')

@lm.user_loader
def load_user(username):
    u = USERS_COLLECTION.find_one({"username": username})
    if not u:
        return None
    return User(u['username'])
