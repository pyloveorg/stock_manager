from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    username = StringField('Username',  [validators.Length(min=4, max=50), validators.InputRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=50), validators.InputRequired()])
    remember = BooleanField('Remember me')

class UserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=50), validators.InputRequired()])
    email = StringField('Email', [validators.Email("Incorrect email address.")])
    name = StringField('Name', [validators.Length(max=200)])
    address = StringField('Address', [validators.Length(max=200)])
    zip_code = StringField('Zip code', [validators.Length(max=10)])
    city = StringField('City', [validators.Length(max=100)])
    phone_no = StringField('Phone no', [validators.Length(max=20)])
    birth_date = DateField('Birth date')

class SignupForm(UserForm):
    password = PasswordField('Password', validators=[validators.Length(min=1, max=50), validators.InputRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password')
