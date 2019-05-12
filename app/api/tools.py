#!/usr/bin/env python

from functools import wraps

from app import db
from app.models import User, Annotation

from flask import g, request, jsonify, current_app


def api_key_required(func):
    @wraps(func)
    def check_api_key(*args, **kwargs):

        # Try to login using the api_key url arg.
        api_key = request.args.get("api_key")
        if api_key:
            user = User.query.filter_by(api_key=api_key).first()

        # Next, try to login using Bearer Authorization.
        api_key = request.headers.get("Authorization")
        if api_key:
            api_key = api_key = api_key.replace("Bearer ", "", 1)
            user = User.query.filter_by(api_key=api_key).first()

        if user:
            g.current_user = user
            return func(*args, **kwargs)

        return api_response_error(401, "Invalid API Key!")

    return check_api_key


class Error(Exception):
    pass


class ImportApiError(Error):

    def __init__(self, status_code, message):

        self.status_code = status_code
        self.message = message

        current_app.logger.error("{0} Error: {1}".format(self.status_code, self.message))


class ImportApi(object):

    _max_chunk_size = 100

    def __init__(self, mode, data):

        self._mode = mode
        self._data = data
        self._chunk_size = len(self._data)

        self._count_added = 0
        self._count_refreshed = 0
        self._errors = []

        self._validate()

    def _validate(self):

        if self._chunk_size > self._max_chunk_size:
            raise ApiError(status_code=400,
                           message="Data chunk size over {0}.".format(self.max_chunk_size))

        if self._chunk_size == 0:
            raise ApiError(status_code=400, message="No data received.")

    def run(self):

        if self._mode == "add":
            self._add_data()

        elif self._mode == "refresh":
            self._refresh_data()

        else:
            raise ApiError(status_code=400,
                           message="Unrecognized import mode. Valid options "
                                   "are 'add' or 'refresh'.")

    def _add_data(self):

        for item in self._data:

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

            """ Create, add and commit annotation. """
            self._create_annotation(item)

            """ """
            self._log_added()

    def _refresh_data(self):

        for item in self._data:

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
                try:
                    db.session.delete(existing)
                    db.session.commit()

                except Exception as error:
                    db.session.rollback()
                    self._log_error(error, item)

            """ Create, add and commit annotation. """
            self._create_annotation(item)

            """ """
            self._log_refreshed()

    def _create_annotation(self, item):

        """ Create and populate new Annotation object. """
        new = Annotation()
        new.deserialize(item)

        try:
            db.session.add(new)
            db.session.commit()

        except Exception as error:
            db.session.rollback()
            self._log_error(error, item)

    def _log_added(self):
        self._count_added += 1

    def _log_refreshed(self):
        self._count_refreshed += 1

    def _log_error(self, error, item):

        current_app.logger.error("{0} @ {1}".format(error, item))

        self._errors.append({
                "error": error,
                "annotation": item
            }
        )

    @property
    def message(self):

        data = {
            "mode": self._mode,
            "chunk_size": self._chunk_size,
            "imported": self._count_added,
            "imported": self._imported,
            "errors": {
                "count": len(self._errors),
                "details": self._errors
            },
        }

        return data


def api_response_error(status_code, message):

    data = {
        "status": "ERROR",
        "message": message
    }

    response = jsonify(data)
    response.status_code = status_code

    return response


def api_response_success(message=None):

    data = {
        "status": "SUCCESS",
        "message": message
    }

    response = jsonify(data)
    response.status_code = 201

    return response
