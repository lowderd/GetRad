from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, validators


class LoginForm(Form):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)


class RegistrationForm(Form):
    username = StringField('Username', validators=[validators.Length(min=3, max=64)])
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[validators.Length(min=3, max=120)])
    email = StringField('Email Address')
