from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateField
import datetime

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
    admin = BooleanField('Admin')

class SignupForm(UserForm):
    password = PasswordField('Password', validators=[validators.Length(min=1, max=50), validators.InputRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password')

class EditWorkplanForm(FlaskForm):
    choices = [(-1, '')]
    for hour in range(0, 25):
        choices.append((hour, str(hour)+':00'))
    start_hour = SelectField('From', choices=choices, coerce=int)
    stop_hour = SelectField('To', choices=choices, coerce=int)
    leave = BooleanField('Leave')

class LeaveApplicationForm(FlaskForm):
    start_date = DateField('From', validators=[validators.InputRequired()])
    end_date = DateField('To', validators=[validators.InputRequired()])
    exclude_weekends = BooleanField('Exclude weekends')
