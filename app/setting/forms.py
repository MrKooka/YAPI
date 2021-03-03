from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField,SubmitField
from wtforms.validators import InputRequired,Email,Length,DataRequired
## login and registration


class RgisterForm(FlaskForm):
    username = TextField('Username',validators=[Email('Некорректный email')])
    email = TextField('Email',validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()])
    submit = SubmitField("Register")
class ChangePasswordForm(FlaskForm):
    origin_password = PasswordField('Type Origin Password', id='origin_assword')
    new_password = PasswordField('Type New Password', id='new_assword')
    new_password2 = PasswordField('Type New Password Again', id='new_assword2')