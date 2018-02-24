from sqlite3 import IntegrityError

from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from main import app, login_manager, db
from forms import LoginForm, SignupForm
from models import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

baseTemplate = 'index.html'
loginTemplate = 'login.html'
signupTemplate = 'signup.html'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/navitem1', methods=['GET'])
@login_required
def navitem1():
    return None

@app.route('/navitem2', methods=['GET'])
def navitem2():
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return render_template(baseTemplate, loggingMessage='Logged in successfully as '+current_user.username)

        return render_template(loginTemplate, form=form, error=True)

    return render_template(loginTemplate, form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return render_template(signupTemplate, form=form, success=True)
        except IntegrityError as e:
            return render_template(signupTemplate, form=form, error=e)

    return render_template(signupTemplate, form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template(baseTemplate, loggingMessage='Logged out successfully')
