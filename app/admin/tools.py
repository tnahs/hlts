#!/usr/bin/env python

from flask import current_app
from flask_login import current_user

from functools import wraps


def admin_only(func):
    """ https://flask-login.readthedocs.io/en/latest/_modules/flask_login/utils.html#login_required
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):

        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_admin:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)

    return decorated_view
