from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators

class LoginForm(FlaskForm):
    username = StringField('Username',  [validators.Length(min=4, max=50), validators.InputRequired()])
    password = PasswordField('Password', [validators.Length(min=4, max=50), validators.InputRequired()])
    remember = BooleanField('Remember me')

class SignupForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=50), validators.InputRequired()])
    email = StringField('Email', [validators.Length(max=50)])
    password = PasswordField('Password', [validators.Length(min=4, max=50), validators.InputRequired()])

