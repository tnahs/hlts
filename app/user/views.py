#!/usr/bin/env python

from app.user import user

from app import db
from app.models import User
from app.tools import is_safe_url, home_url
from app.user.forms import LoginForm, UserForm, SettingsForm

from flask import request, redirect, url_for, flash, render_template
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
@user.route('/settings/<mode>', methods=['POST', 'GET'])
@login_required
def settings(mode=None):

    # TODO Can we clean up logic here?

    default_mode = 'main'

    user_form = UserForm(obj=current_user)
    settings_form = SettingsForm(obj=current_user)

    if mode == 'default' or mode == default_mode:

        request.view_args['mode'] = default_mode

        if request.method == 'POST':

            if 'general' in request.form:

                if settings_form.validate_on_submit():

                    current_user.theme_index = settings_form.theme_index.data
                    current_user.results_per_page = settings_form.results_per_page.data
                    current_user.recent_days = settings_form.recent_days.data

                    db.session.commit()

            return redirect(url_for('user.settings', mode='main'))

    elif mode == 'login':

        if request.method == 'POST':

            if 'login' in request.form:

                if user_form.validate_on_submit():

                    form_username = user_form.username.data
                    form_password = user_form.password.data
                    form_password_change = user_form.password_change.data
                    form_password_confirm = user_form.password_confirm.data

                    if current_user.check_password(form_password):

                        """ NOTE ValidationError() does not get passed into the
                        form with the setup we have here. so were doing this
                        all manually in the User class.
                        """

                        # TODO figure a way to combine the flashes so we dont get doubles.

                        if form_password_change:

                            if current_user.change_password(form_password_change, form_password_confirm):
                                flash('password changed!', 'success')

                            else:
                                flash('password invalid!', 'warning')

                        if current_user.username != form_username:

                            if current_user.change_username(form_username):
                                flash('username changed!', 'success')

                            else:
                                flash('username invalid!', 'warning')

                        db.session.commit()

                    else:

                        flash('incorrect password!', 'warning')

                    return redirect(url_for('user.settings', mode='login'))

    elif mode == 'tools':

        pass

    else:

        return redirect(url_for('user.settings', mode='default'))

    return render_template('user/settings.html', user_form=user_form, settings_form=settings_form)


@user.route('/delete_color/<string:name>', methods=['POST', 'GET'])
@login_required
def delete_color(name):

    current_user.delete_color(name)

    db.session.commit()

    return redirect(url_for('user.settings'))