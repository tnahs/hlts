#!/usr/bin/env python

from functools import wraps

from app import db
from app.models import User, Annotation
from app.api.errors import ApiError

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


# NEW #########################################################################


def api_success_response():

    payload = {
        "message": "success"
    }

    response = jsonify(payload)
    response.status_code = 201
    return response


class ApiImport(object):

    max_chunk_size = 100

    def __init__(self, mode, data):

        self.mode = mode
        self.data = data

        self._validate()

    def run(self):

        if self.mode == "add":
            self._add_data()

        elif self.mode == "refresh":
            self._refresh_data()

        else:
            raise ApiError(status_code=400,
                           message="Unrecognized import mode. Valid options "
                                   "are 'add' or 'refresh'.")

    def _validate(self):

        if len(self.data) > self.max_chunk_size:
            raise ApiError(status_code=400,
                           message="Data chunk size over {0}.".format(self.max_chunk_size))

    def _add_data(self):

        for item in self.data:

            """ Set `id` to `None` if item has no `id`. """
            if not item["id"]:
                item["id"] = None

            """ Check to see if any annotation exists with this `id`.
            Annotation.query_by_id() returns `None` if no annotation is found.
            """
            existing = Annotation.query_by_id(item["id"])

            """ Skip to the next item if the annotation already exists. """
            if existing:
                continue

            self._create_commit_annotation(item)

    def _refresh_data(self):

        for item in self.data:

            """ Set `id` to `None` if item has no `id`. """
            if not item["id"]:
                item["id"] = None

            """ Check to see if any annotation exists with this `id`.
            Annotation.query_by_id() returns `None` if no annotation is found.
            """
            existing = Annotation.query_by_id(item["id"])

            if existing:

                """ Skip to the next item if the annotation is protected. """
                if existing.is_protected:
                    continue

                """ Otherwise delete the annotation. """
                db.session.delete(existing)
                db.session.commit()

            self._create_commit_annotation(item)

    def _create_commit_annotation(self, item):

        new = Annotation()
        new.deserialize(item)

        try:
            db.session.add(new)
            db.session.commit()

        except:
            db.session.rollback()