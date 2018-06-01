from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from auth.forms import LoginForm, SignupForm, UserForm
from auth.models import User
from database import db
from flask import request

signupTemplate = 'signup.html'
loginModalTemplate = 'login_modal.html'
loginTemplate = 'login.html'
baseTemplate = 'index.html'
usersTemplate = 'users.html'

from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')


@auth_blueprint.route('/editprofile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    return redirect(url_for('auth.edit_user', user_id=current_user.id))


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Logged in successfully as {}'.format(current_user.username), 'success')
                return render_template(baseTemplate)

        flash('Invalid username or password', 'danger')
        # return render_template(loginTemplate, form=form, error=True)
        return render_template(loginTemplate, form=form)

    return render_template(loginTemplate, form=form)


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data,
                            email=form.email.data,
                            password=hashed_password,
                            name=form.name.data,
                            address=form.address.data,
                            zip_code=form.zip_code.data,
                            city=form.city.data,
                            phone_no=form.phone_no.data)
                            # birth_date=form.birth_date.data)

            db.session.add(new_user)
            db.session.commit()
            flash('User added successfully', 'success')
            return redirect(url_for('home.index'))
            # return render_template(signupTemplate, form=form, success=True, purpose="signup", action=url_for('auth.signup'), success_message='User added successfully')
        except IntegrityError as e:
            flash('User already exists in database', 'danger')
            return render_template(signupTemplate, form=form, purpose="signup", action=url_for('auth.signup'))
    return render_template(signupTemplate, form=form, purpose="signup", action=url_for('auth.signup'))


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return render_template(baseTemplate)


@auth_blueprint.route('/users', methods=['GET'])
@login_required
def users():
    if current_user.admin is True:
        user_list = User.query.order_by(User.username).all()
    else:
        user_list = User.query.filter_by(id=current_user.id)
    return render_template(usersTemplate, user_list=user_list)

@auth_blueprint.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.admin is False and current_user.id != user_id:
        abort(404)

    user = User.query.filter_by(id=user_id).first()
    form = UserForm()
    if request.method == 'GET':
        form.username.data = user.username
        form.name.data = user.name
        form.email.data = user.email
        form.address.data = user.address
        form.zip_code.data = user.zip_code
        form.city.data = user.city
        form.phone_no.data = user.phone_no
    elif form.validate_on_submit():
        user.username = form.username.data
        user.name = form.name.data
        user.email = form.email.data
        user.address = form.address.data
        user.zip_code = form.zip_code.data
        user.city = form.city.data
        user.phone_no = form.phone_no.data
        db.session.commit()
        flash('User successfully updated', 'success')
        return redirect(url_for('auth.users'))

    return render_template(signupTemplate,
                           form=form,
                           action=url_for('auth.edit_user', user_id=user_id))
    # return render_template(signupTemplate,
    #                        form=form,
    #                        action=url_for('auth.edit_user', user_id=user_id), success_message='User successfully updated')

    # return redirect(url_for('auth.users'))
