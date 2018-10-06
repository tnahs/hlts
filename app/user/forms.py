#!/usr/bin/env python

from app.models import User

from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, ValidationError


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

        user = User.query.filter_by(username=field.data).first()

        if not user:

            flash("user does not exist!", "warning")

            raise ValidationError()

        else:

            self.user = user

    def validate_password(self, field):

        if self.user:

            if not self.user.check_password(field.data):

                flash("invalid password!", "warning")

                raise ValidationError()


class UserForm(FlaskForm):

    username = StringField(
        validators=[InputRequired(), Length(min=5, max=16)],
        render_kw={'placeholder': 'username'})
    fullname = StringField(
        validators=[Length(min=0, max=32)],
        render_kw={'placeholder': 'full name'})
    email = StringField(
        validators=[InputRequired(), Email()],
        render_kw={'placeholder': 'e-mail'})
    results_per_page = IntegerField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'results per page'})
    recent_days = IntegerField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'recent days'})
    api_key = StringField(render_kw={'readonly': True})
    # theme_index = SelectField('theme', choices=AppDefaults.THEME_CHOICES)

    def __init__(self, user, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.user = user

    def validate_username(self, field):

        if not field.validate(field.data):

            flash("username must be between 5-16 characters!", "warning")

            raise ValidationError()

        if field.data != self.user.username:

            user = User.query.filter_by(username=field.data).first()

            if user is not None:

                flash("username already taken!", "warning")

                raise ValidationError()

    def validate_email(self, field):

        if not field.validate(field.data):

            flash("invalid e-mail address!", "warning")

        if field.data != self.user.email:

            user = User.query.filter_by(email=field.data).first()

            if user is not None:

                flash("e-mail already taken!", "warning")

                raise ValidationError()

    def validate_fullname(self, field):

        if not field.validate(field.data):

            flash("fullname too long!", "warning")

    def validate_results_per_page(self, field):

        if not field.validate(field.data):

            flash("results per page must be an integer!", "warning")

        if field.data < 16 or field.data > 128:

            flash("results per page: must be an an iteger between 16 and 128", "warning")

            raise ValidationError()

    def validate_recent_days(self, field):

        if not field.validate(field.data):

            flash("recent days must be an integer!", "warning")

        if field.data < 1 or field.data > 90:

            flash("recent days: must be an iteger between 1 and 90", "warning")

            raise ValidationError()


class PasswordChangeForm(FlaskForm):

    password = PasswordField(validators=[InputRequired()])
    password_change = PasswordField()
    password_confirm = PasswordField()
