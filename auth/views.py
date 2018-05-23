from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from auth.forms import LoginForm, SignupForm
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
    # setattr(User.query.filter_by(id=current_user.id).one(), 'address', 'Kutnp')
    #  setattr(User.query.filter_by(id=current_user.id).one(), {'address': 'NewHampshire', 'phone_no': '777333222'})
    # User.query.filter_by(id=current_user.id).one().address = 'Kutno'
    # db.session.commit()
    # session = Session()
    # User.query(id=current_user.id).update(address='jakistamadres')
    #  # current_user.update(username='admin2')
    return redirect(url_for('auth.edit_user', user_id=current_user.id))
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
                            phone_no=form.phone_no.data)
                            # birth_date=form.birth_date.data)

            db.session.add(new_user)
            db.session.commit()
            return render_template(signupTemplate, form=form, success=True, action="/signup", success_message='User added successfully')
        except IntegrityError as e:
            return render_template(signupTemplate, form=form, error=e, action="/signup")
    return render_template(signupTemplate, form=form, action="/signup")



@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template(baseTemplate, loggingMessage='Logged out successfully')


@auth_blueprint.route('/users', methods=['GET'])
@login_required
def users():
    user_list = User.query.order_by(User.username).all()

    # user_list = User.query.all()
    return render_template(usersTemplate, user_list=user_list)

@auth_blueprint.route('/user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = SignupForm()
    if request.method == 'GET':
        form.username.data = user.username
        form.name.data = user.name
        form.email.data = user.email
        form.address.data = user.address
        form.zip_code.data = user.zip_code
        form.city.data = user.city
        form.phone_no.data = user.phone_no
        # return render_template(signupTemplate, form=form)
    else:
        if form.validate_on_submit():
            user.username = form.username.data
            user.name = form.name.data
            user.email = form.email.data
            user.address = form.address.data
            user.zip_code = form.zip_code.data
            user.city = form.city.data
            user.phone_no = form.phone_no.data
            db.session.commit()
        # else:
        #     print('pretty')

    return render_template(signupTemplate, form=form, action="/user/{}".format(str(user_id)), success_message='User successfully updated')

    # print(request.method)
    # else:
    #     print('MÓJ')
    # print(str(user_id))
    # stmt = User.update(). \
    #     values(address=('Yokohama')). \
    #     where(User.id == current_user.id)
    # db.engine.execute(stmt)


    # user = User.query.filter_by(id==)
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
    #                         phone_no=form.phone_no.data)
    #                         # birth_date=form.birth_date.data)
    #
    #         db.session.add(new_user)
    #         db.session.commit()
    #         return render_template(signupTemplate, form=form, success=True)
    #     except IntegrityError as e:
    #         return render_template(signupTemplate, form=form, error=e)
    # return render_template(signupTemplate, form=form)
    #



    return redirect(url_for('auth.users'))
