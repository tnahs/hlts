#!/usr/local/bin/python3

from functools import wraps

from app import db
from app.models import User, Annotation

from flask import g, request, jsonify, current_app


"""
API Error Response
------------------

API Errors are sent the the user via raising an ApiError and passing the
required arguments of status code and message.

An ApiError is raised for invalid API keys and when there's a fatal error that
can cause unexpected results. The import process is aborted before it's begun
and the error response is sent to the user. However, errors on a per-annotation
basis do not abort the import process. They are logged and sent back to the
user after the import is finished.

An Error Response looks like this:

{
    "success": false,
    "error": "Error message"
}

"""

class ApiError(Exception):

    def __init__(self, status_code, message):
        super(ApiError, self).__init__(message)

        self.status_code = status_code
        self.message = message

        current_app.logger.error("{0} Error: {1}".format(self.status_code, message))

    def send_response(self):

        data = {
            "success": False,
            "error": self.message,
        }

        response = jsonify(data)
        response.status_code = self.status_code

        return response


"""
API Import Response: 201 Created
--------------------------------

The ApiImport class has it's own response structure. This is sent back to the
user after every POST to `api/import/add` or `api/import/refresh`. The importer
documents every single success and failure during the import process. Lists of
IDs are sent back to the user for verification, handling and re-importing of
failed imports.

An Import Response looks like this:

{
    "success": true,
    "data": {
        "metadata": {
            "mode": "Import mode ('add' or 'refresh')",
            "chunk_size": "Data chunk size",
        },
        "import_succeeded": {
            "added": ["List of added annotation IDs", ],
            "refreshed": ["List of refreshed annotation IDs", ],
            "skipped_existing": ["List of skipped (existing) annotation IDs", ],
            "skipped_protected": ["List of skipped (protected) annotation IDs", ],
        },
        "import_failed": [
            {
                "exception": "Raised exception",
                "annotation_id": "Respective annotation ID",
            },
            {
                "exception": "Raised exception",
                "annotation_id": "Respective annotation ID",
            },
            ...
            ...
            ...
        ]
    }
}

"""


class ApiImport:

    _max_chunk_size = 100

    def __init__(self, mode, data):

        self._mode = mode
        self._annotations = data
        self._chunk_size = len(self._annotations)

        self._added = []
        self._refreshed = []
        self._skipped_existing = []
        self._skipped_protected = []
        self._failed = []

        self._validate()

    def _validate(self):

        """ Post requests to the API are sent as lists of annotations. If the
        length of this list is greater than ApiImport._max_chunk_size it could
        cause a Gateway Timeout (504) error. Any request over this limit is
        refused to prevent unexpected results. """
        if self._chunk_size > self._max_chunk_size:
            raise ApiError(status_code=400,
                           message="Data chunk size over {0}.".format(self._max_chunk_size))

        if self._chunk_size <= 0:
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

            # Annotation.query_by_id() returns `None` if no annotation found.
            existing = Annotation.query_by_id(annotation["id"])

            # Skip to the next annotation if the annotation exists.
            if existing:
                self._log_skipped_existing(annotation["id"])
                continue

            # Create a new annotation.
            try:
                new = Annotation()
                new.deserialize(annotation)
            except Exception as exception:
                self._log_failed(exception, annotation["id"])
                continue

            # And add it.
            try:
                db.session.add(new)
                db.session.commit()
                self._log_added(new.id)
            except Exception as exception:
                db.session.rollback()
                self._log_failed(exception, new.id)

    def _refresh_annotations(self):

        for annotation in self._annotations:

            # Annotation.query_by_id() returns `None` if no annotation found.
            existing = Annotation.query_by_id(annotation["id"])

            if existing:

                # Skip to the next annotation if the annotation is protected.
                if existing.is_protected:
                    self._log_skipped_protected(annotation["id"])
                    continue

                # Otherwise delete the annotation.
                try:
                    db.session.delete(existing)
                    db.session.commit()
                except Exception as exception:
                    db.session.rollback()
                    self._log_failed(exception, existing.id)
                    continue

            # Create a new annotation.
            try:
                new = Annotation()
                new.deserialize(annotation)
            except Exception as exception:
                self._log_failed(exception, annotation["id"])
                continue

            # And re-add it.
            try:
                db.session.add(new)
                db.session.commit()
                self._log_refreshed(new.id)
            except Exception as exception:
                db.session.rollback()
                self._log_failed(exception, new.id)

    def _log_skipped_existing(self, annotation_id):
        current_app.logger.info(
            "Skipped existing annotation: {0}".format(annotation_id))
        self._skipped_existing.append(annotation_id)

    def _log_skipped_protected(self, annotation_id):
        current_app.logger.info(
            "Skipped protected annotation: {0}".format(annotation_id))
        self._skipped_protected.append(annotation_id)

    def _log_added(self, annotation_id):
        current_app.logger.info(
            "Added annotation: {0}".format(annotation_id))
        self._added.append(annotation_id)

    def _log_refreshed(self, annotation_id):
        current_app.logger.info(
            "Refreshed annotation: {0}".format(annotation_id))
        self._refreshed.append(annotation_id)

    def _log_failed(self, exception, annotation_id):
        current_app.logger.warning(
            "Import failed: {1}\n{0}".format(annotation_id, repr(exception)))
        self._failed.append({
                "exception": exception,
                "annotation_id": annotation_id,
            }
        )

    def send_response(self):

        data = {
            "success": True,
            "data": {
                "metadata": {
                    "mode": self._mode,
                    "chunk_size": self._chunk_size,
                },
                "import_succeeded": {
                    "added": self._added,
                    "refreshed": self._refreshed,
                    "skipped_existing": self._skipped_existing,
                    "skipped_protected": self._skipped_protected,
                },
                "import_failed": self._failed,
            }
        }

        response = jsonify(data)
        response.status_code = 201

        return response


def api_key_required(func):
    """ Wrapper function to handle API Key authorization.
    """
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

        raise ApiError(status_code=401, message="Invalid API Key.")

    return check_api_key
