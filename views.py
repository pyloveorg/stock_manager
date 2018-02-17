#!/usr/bin/env python
# encoding: utf-8
from main import app
from main import db
from main import login_manager
from models import User
from main import bcrypt
from flask import request, render_template, redirect, flash, url_for


@app.route('/', methods=['GET'])
def index():
    #import pdb; pdb.set_trace()
    return render_template('index.html')

@app.route('/info', methods=['GET'])
def info():
    return render_template('info.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = bcrypt.generate_password_hash(request.form['pwd'])
    """new_User=User(
        email=email,
        password=password,
    )

    db.session.add(new_User)
    db.session.commit()
"""
    #print password

    registered_user=User.query.filter_by(email=email).first()
    #for user in registered_user:
    #    print '{}{}'.format(user.email, user.password)

    if registered_user:
        if registered_user.password == password:

    #    print 'None'
        #flash('Username or Password is invalid', 'error')
    #    return redirect(url_for('login'))
    #print 'ABC'

    #login_user(registered_user)
            return '<h1>'+registered_user.email+' </h1>'

    print 'Non'

    #flash('Logged in successfully')
    if request.method == 'POST':
        return redirect(url_for('login'))
    """form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        return flask.redirect(url_for('index'))

    return render_template('register.html', form=form)"""

    #return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))