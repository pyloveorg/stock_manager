from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from auth.forms import LoginForm, SignupForm
from auth.models import User
from database import db

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
    # db.session.query(User).filter(id=current_user.id).update(address='jakistamadres')
    # user = User.query.filter_by(id=current_user.id)
    # user.address = 'newaddresshhhhhh'
    # db.session.commit()

    # db.session.query().\
    #     filter(User.id == 1). \
    #     update({"address": 'New Hampshire'})
    # db.session.commit()

    # User.query.filter(User.id == 1). \
    #     update({"address": (1)})
    # db.session.commit()
    # print(str(getattr(User.query.filter(User.id == 1).data.id)))
    # user = User.query.filter_by(id=1).first()
    # print(str(user.id))
    # setattr(User.query.filter_by(id=current_user.id).one(), 'address', 'NewHampshire')


    # db.session.commit()
    # session = Session()
    # User.query(id=current_user.id).update(address='jakistamadres')
    #  # current_user.update(username='admin2')
    return redirect(url_for('home.index'))
    # form = SignupForm()
    # if form.validate_on_submit():
    #     try:
    #         hashed_password = generate_password_hash(form.password.data, method='sha256')
    #         # print(form.phone_no.data)
    #         new_user = User(username=form.username.data,
    #                         email=form.email.data,
    #                         password=hashed_password,
    #                         name=form.name.data,
    #                         address=form.address.data,
    #                         zip_code=form.zip_code.data,
    #                         city=form.city.data,
    #                         phone_no=form.phone_no.data,
    #                         birth_date=form.birth_date.data)
    #
    #         db.session.add(new_user)
    #         db.session.commit()
    #         return render_template(signupTemplate, form=form, success=True)
    #     except IntegrityError as e:
    #         return render_template(signupTemplate, form=form, error=e)
    # return render_template(signupTemplate, form=form)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
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


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            # print(form.phone_no.data)
            new_user = User(username=form.username.data,
                            email=form.email.data,
                            password=hashed_password,
                            name=form.name.data,
                            address=form.address.data,
                            zip_code=form.zip_code.data,
                            city=form.city.data,
                            phone_no=form.phone_no.data,
                            birth_date=form.birth_date.data)

            db.session.add(new_user)
            db.session.commit()
            return render_template(signupTemplate, form=form, success=True)
        except IntegrityError as e:
            return render_template(signupTemplate, form=form, error=e)
    return render_template(signupTemplate, form=form)



@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template(baseTemplate, loggingMessage='Logged out successfully')


@auth_blueprint.route('/users', methods=['GET'])
@login_required
def users():
    user_list = User.query.filter(User.id == 1)

    # user_list = User.query.all()
    return render_template(usersTemplate, user_list=user_list)

