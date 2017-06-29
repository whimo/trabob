from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField('username', validators=[
        DataRequired(),
        Length(min=4, max=64, message='Username must contain from 4 to 64 characters'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               message='Username can contain only letters, numbers, dots and underscores')])
    password = PasswordField('password', validators=[
        DataRequired(),
        Length(min=6, max=128, message='Password must contain from 6 to 128 characters'),
        EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired()])


class AddAccountForm(Form):
    server_url = StringField('server_url', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    default = BooleanField('default')
