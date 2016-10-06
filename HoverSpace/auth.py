from .application import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required
from .models import USERS_COLLECTION
from .user import User
from .forms import LoginForm

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = USERS_COLLECTION.find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("empty"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/empty', methods=['GET', 'POST'])
@login_required
def empty():
    return render_template('empty.html')

@lm.user_loader
def load_user(username):
    u = USERS_COLLECTION.find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
