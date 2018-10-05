#!/usr/bin/env python

from app.models import User
from app.api.errors import error_response

from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):  # -> bool:

    user = User.query.filter_by(username=username).first()

    if user is None:

        return False

    g.current_user = user

    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():

    return error_response(401)


@token_auth.verify_token
def verify_api_token(api_token):  # -> Union[User, None]:

    user = User.query.filter_by(api_token=api_token).first()

    if user:

        g.current_user = user

        return g.current_user

    return None


@token_auth.error_handler
def api_token_auth_error():

    return error_response(401)
