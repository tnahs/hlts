#!/usr/bin/env python

from app.models import User

from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import InputRequired, ValidationError


class LoginForm(FlaskForm):

    user = None

    username = StringField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'username'})
    password = PasswordField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'password'})
    remember = BooleanField('remember')

    def validate_username(self, field):

        try:
            self.user = User.check_user(field.data)

        except ValueError as error:
            flash(error, "warning")
            raise ValidationError()

    def validate_password(self, field):

        if self.user:

            try:
                self.user.check_password(field.data)

            except ValueError as error:
                flash(error, "warning")
                raise ValidationError()


class UserForm(FlaskForm):

    id = HiddenField()
    username = StringField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'username'})
    fullname = StringField(
        render_kw={'placeholder': 'full name'})
    email = StringField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'e-mail'})
    results_per_page = StringField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'results per page'})
    recent_days = StringField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'recent days'})
    api_key = StringField(render_kw={'readonly': True})
    # theme_index = SelectField('theme', choices=AppDefaults.THEME_CHOICES)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        user = kwargs.get("obj", None)

        if user is not None:
            self.user = user

    def validate_username(self, field):

        try:
            self.user.username = field.data

        except AssertionError as error:
            flash(error, "warning")
            raise ValidationError()

    def validate_fullname(self, field):

        try:
            self.user.fullname = field.data

        except AssertionError as error:
            flash(error, "warning")
            raise ValidationError()

    def validate_email(self, field):

        try:
            self.user.email = field.data

        except AssertionError as error:
            flash(error, "warning")
            raise ValidationError()

    def validate_results_per_page(self, field):

        try:
            self.user.results_per_page = field.data

        except AssertionError as error:
            flash(error, "warning")
            raise ValidationError()

    def validate_recent_days(self, field):

        try:
            self.user.recent_days = field.data

        except AssertionError as error:
            flash(error, "warning")
            raise ValidationError()
