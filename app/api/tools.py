#!/usr/bin/env python

from functools import wraps

from app.models import User

from flask import g, request, jsonify
from werkzeug.http import HTTP_STATUS_CODES


def api_key_required(func):
    @wraps(func)
    def check_api_key(*args, **kwargs):

        # Try to login using the api_key url arg
        api_key = request.args.get("api_key")
        if api_key:
            user = User.query.filter_by(api_key=api_key).first()

        # Next, try to login using Bearer Authorization
        api_key = request.headers.get("Authorization")
        if api_key:
            api_key = api_key = api_key.replace("Bearer ", "", 1)
            user = User.query.filter_by(api_key=api_key).first()

        if user:
            g.current_user = user
            return func(*args, **kwargs)

        return api_error_response(401, "Invalid API Key!")

    return check_api_key


def api_error_response(status_code, message=None):

    payload = {
        "error": HTTP_STATUS_CODES.get(status_code, "Unknown Error"),
        "message": message
    }

    response = jsonify(payload)
    response.status_code = status_code
    return response
