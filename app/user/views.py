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
        remember = login_form.remember.data

        user = User.query.filter_by(username=username).first()

        login_user(user, remember=remember)

        next_url = request.args.get('next', None)

        if next_url and is_safe_url(next_url):

            return redirect(next_url)

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

    user_form = UserForm(user=current_user, obj=current_user)

    if user_form.validate_on_submit():

        user_form.populate_obj(current_user)

        db.session.commit()

    return render_template('user/settings.html', user_form=user_form)