#!/usr/local/bin/python3

from app.models import User

from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import InputRequired, ValidationError


class LoginForm(FlaskForm):

    user = None

    username = StringField(
        validators=[InputRequired()],
        render_kw={"placeholder": "username"})
    password = PasswordField(
        validators=[InputRequired()],
        render_kw={"placeholder": "password"})
    remember = BooleanField("keep me logged in")

    def validate_username(self, field):

        try:
            self.user = User.check_user(field.data)

        except ValueError as error:
            flash(error, "flashWarning")
            raise ValidationError(error)

    def validate_password(self, field):

        if self.user:

            # FIXME Getting "Invalid Salt" Exception on Heroku. Can't login.
            password = field.data.encode('utf-8')

            try:
                self.user.check_password(password)

            except ValueError as error:
                flash(error, "flashWarning")
                raise ValidationError(error)


class UserForm(FlaskForm):

    id = HiddenField()
    username = StringField(
        validators=[InputRequired()],
        render_kw={"placeholder": "username"})
    fullname = StringField(
        render_kw={"placeholder": "full name"})
    email = StringField(
        validators=[InputRequired()],
        render_kw={"placeholder": "e-mail"})
    results_per_page = StringField(
        validators=[InputRequired()],
        render_kw={"placeholder": "results per page"})
    recent_days = StringField(
        validators=[InputRequired()],
        render_kw={"placeholder": "recent days"})
    api_key = StringField(render_kw={"readonly": True})

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        user = kwargs.get("obj", None)

        if user is not None:
            self.user = user

    def validate_username(self, field):

        try:
            self.user.username = field.data

        except AssertionError as error:
            flash(error, "flashWarning")
            raise ValidationError(error)

    def validate_fullname(self, field):

        try:
            self.user.fullname = field.data

        except AssertionError as error:
            flash(error, "flashWarning")
            raise ValidationError(error)

    def validate_email(self, field):

        try:
            self.user.email = field.data

        except AssertionError as error:
            flash(error, "flashWarning")
            raise ValidationError(error)

    def validate_results_per_page(self, field):

        try:
            self.user.results_per_page = field.data

        except AssertionError as error:
            flash(error, "flashWarning")
            raise ValidationError(error)

    def validate_recent_days(self, field):

        try:
            self.user.recent_days = field.data

        except AssertionError as error:
            flash(error, "flashWarning")
            raise ValidationError(error)


class ChangePasswordForm(FlaskForm):

    id = HiddenField()
    old_password = PasswordField(
        validators=[InputRequired()],
        render_kw={"placeholder": "old password"})
    new_password = PasswordField(
        validators=[InputRequired()],
        render_kw={"placeholder": "new password"})
    confirm_password = PasswordField(
        validators=[InputRequired()],
        render_kw={"placeholder": "confirm password"})

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        user = kwargs.get("obj", None)

        if user is not None:
            self.user = user

    def validate_old_password(self, field):

        try:
            self.user.check_password(field.data)

        except ValueError as error:
            flash(error, "flashWarning")
            raise ValidationError(error)

    def validate_new_password(self, field):

        try:
            self.user.change_password(field.data, self.confirm_password.data)

        except (ValueError, AssertionError) as error:
            flash(error, "flashWarning")
            raise ValidationError(error)

    def validate_confirm_password(self, field):

        if self.new_password.errors:
            raise ValidationError()
