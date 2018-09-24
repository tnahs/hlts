#!/usr/bin/env python

import app.defaults as AppDefaults

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    """ login form
    """
    username = StringField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'username'})
    password = PasswordField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'password'})
    remember = BooleanField('remember')


class UserForm(FlaskForm):
    """ user form
    """
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    password_change = PasswordField()
    password_confirm = PasswordField()


class SettingsForm(FlaskForm):
    """ settings form
    """
    theme_index = SelectField('theme', choices=AppDefaults.THEME_CHOICES)
    results_per_page = StringField(validators=[InputRequired()])
    recent_days = StringField(validators=[InputRequired()])
