#!/usr/bin/env python

from app.user import user

from app import db
from app.models import User
from app.tools import is_safe_url, home_url
from app.user.forms import LoginForm, UserForm

from flask import request, redirect, url_for, render_template
from flask_login import login_required, login_user, logout_user, current_user


@user.route('/login/', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():

        username = login_form.username.data
        password = login_form.password.data
        remember = login_form.remember.data

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):

            login_user(user, remember=remember)

            next = request.args.get('next', None)

            if next and is_safe_url(next):

                return redirect(next)

            else:

                return redirect(home_url())

    return render_template('user/login.html', login_form=login_form)


@user.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('user.login'))


@user.route('/settings/', methods=['POST', 'GET'])
@login_required
def settings():

    user_form = UserForm(obj=current_user)

    if user_form.validate_on_submit():

        current_user.username = user_form.username.data
        current_user.email = user_form.email.data
        current_user.fullname = user_form.fullname.data
        current_user.results_per_page = user_form.results_per_page.data
        current_user.recent_days = user_form.recent_days.data

        db.session.commit()

    return render_template('user/settings.html', user_form=user_form)