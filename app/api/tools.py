#!/usr/bin/env python

from functools import wraps

from app import db
from app.models import User, Annotation

from flask import g, request, jsonify, current_app


"""
TODO: Document the API!
"""


def api_key_required(func):
    @wraps(func)
    def check_api_key(*args, **kwargs):

        """ Try to login using the api_key url arg. """
        api_key = request.args.get("api_key")
        if api_key:
            user = User.query.filter_by(api_key=api_key).first()

        """ Next, try to login using Bearer Authorization. """
        api_key = request.headers.get("Authorization")
        if api_key:
            api_key = api_key = api_key.replace("Bearer ", "", 1)
            user = User.query.filter_by(api_key=api_key).first()

        if user:
            g.current_user = user
            return func(*args, **kwargs)

        return api_response_error(401, "Invalid API Key!")

    return check_api_key


class ApiError(Exception):
    pass


class ImportApiError(ApiError):

    def __init__(self, status_code, message):

        message = "{0} Error: {1}".format(status_code, message)

        super(ImportApiError, self).__init__(message)

        current_app.logger.error(message)



class ImportApi(object):

    _max_chunk_size = 100

    def __init__(self, mode, data):

        self._mode = mode
        self._annotations = data
        self._chunk_size = len(self._annotations)

        self._count_added = 0
        self._count_refreshed = 0
        self._errors = []

        self._validate()

    def _validate(self):

        """ Annotations should be sent in chunks to help prevent Timeouts. """
        if self._chunk_size > self._max_chunk_size:
            raise ApiError(status_code=400,
                           message="Data chunk size over {0}.".format(self.max_chunk_size))

        if self._chunk_size == 0:
            raise ApiError(status_code=400, message="No data received.")

    def run(self):

        if self._mode == "add":
            self._add_annotations()

        elif self._mode == "refresh":
            self._refresh_annotations()

        else:
            raise ApiError(status_code=400,
                           message="Unrecognized import mode. Valid options "
                                   "are 'add' or 'refresh'.")

    def _add_annotations(self):

        for annotation in self._annotations:

            """ Set `id` to `None` if annotation has no `id`. """
            if not annotation["id"]:
                annotation["id"] = None

            """ Check to see if any annotation exists with this `id`.
            Annotation.query_by_id() returns `None` if no annotation is found.
            """
            existing = Annotation.query_by_id(annotation["id"])

            """ Skip to the next annotation if the annotation exists. """
            if existing:
                continue

            new = Annotation()
            new.deserialize(annotation)

            try:
                db.session.add(new)
                db.session.commit()
                self._log_added()

            except Exception as error:
                db.session.rollback()
                self._log_error(error, annotation)

    def _refresh_annotations(self):

        for annotation in self._annotations:

            """ Set `id` to `None` if annotation has no `id`. """
            if not annotation["id"]:
                annotation["id"] = None

            """ Check to see if any annotation exists with this `id`.
            Annotation.query_by_id() returns `None` if no annotation is found.
            """
            existing = Annotation.query_by_id(annotation["id"])

            if existing:

                """ Skip to the next annotation if the annotation is protected. """
                if existing.is_protected:
                    continue

                """ Otherwise delete the annotation. """
                try:
                    db.session.delete(existing)
                    db.session.commit()

                except Exception as error:
                    db.session.rollback()
                    self._log_error(error, annotation)

                    """ Skip to the next annotation if error occurs. """
                    continue

            new = Annotation()
            new.deserialize(annotation)

            try:
                db.session.add(new)
                db.session.commit()
                self._log_refreshed()

            except Exception as error:
                db.session.rollback()
                self._log_error(error, annotation)

    def _log_added(self):
        self._count_added += 1

    def _log_refreshed(self):
        self._count_refreshed += 1

    def _log_error(self, error, annotation):

        current_app.logger.error("{0} @ {1}".format(error, annotation))

        self._errors.append({
                "error": error,
                "annotation": annotation
            }
        )

    @property
    def message(self):

        data = {
            "mode": self._mode,
            "chunk_size": self._chunk_size,
            "count_added": self._count_added,
            "count_refreshed": self._count_refreshed,
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
