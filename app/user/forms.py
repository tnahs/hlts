#!/usr/bin/env python

import app.defaults as AppDefaults

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import InputRequired, Email


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
    username = StringField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'username'})
    fullname = StringField(
        render_kw={'placeholder': 'full name'})
    email = StringField(
        validators=[InputRequired(), Email()],
        render_kw={'placeholder': 'e-mail'})
    results_per_page = StringField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'results per page'})
    recent_days = StringField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'recent days'})
    # theme_index = SelectField('theme', choices=AppDefaults.THEME_CHOICES)


class PasswordChangeForm(FlaskForm):
    password = PasswordField(validators=[InputRequired()])
    password_change = PasswordField()
    password_confirm = PasswordField()
