from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField



class LoginForm(FlaskForm):
    username = TextField('Username')
    password = PasswordField('Password', id='pwd_login')


class CreateAccountForm(FlaskForm):
    username = TextField('Username', id='username_create')
    email = TextField('Email')
    password = PasswordField('Password', id='pwd_create')
