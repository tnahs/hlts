#!/usr/local/bin/python3

from . import user

from app import db
from app.models import User
from app.tools import is_safe_url, home_url
from app.user.forms import LoginForm, UserForm, ChangePasswordForm

from flask import request, redirect, url_for, render_template, flash
from flask_login import login_required, login_user, logout_user, current_user


@user.route("/login/", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        remember = form.remember.data

        user = User.query.filter_by(username=username).first()

        login_user(user, remember=remember)

        next_url = request.args.get("next", None)

        if next_url and is_safe_url(next_url):

            return redirect(next_url)

        else:

            return redirect(home_url())

    return render_template("user/login.html", form=form)


@user.route("/logout/")
@login_required
def logout():

    logout_user()

    return redirect(url_for("user.login"))


@user.route("/settings/", methods=["POST", "GET"])
@login_required
def settings():

    form = UserForm(obj=current_user)

    if form.validate_on_submit():

        user = User.query.get(form.id.data)

        user.edit(form.data)

        db.session.commit()

        flash("user settings updated", "flashSuccess")

    return render_template("user/settings.html", form=form)


@user.route("/change_password/", methods=["POST", "GET"])
@login_required
def change_password():

    form = ChangePasswordForm(obj=current_user)

    if form.validate_on_submit():

        user = User.query.get(form.id.data)

        user.set_password(form.new_password.data)

        db.session.commit()

        flash("password updated", "flashSuccess")

    return render_template("user/change_password.html", form=form)
