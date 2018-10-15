#!/usr/bin/env python

import sys
from functools import wraps

from flask import g, request, jsonify
from werkzeug.http import HTTP_STATUS_CODES

from app import db
from app.models import User, Annotation
from app.tools import async_threaded


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


@async_threaded
def run_async_import_annotations_refresh(app, annotations):

    # WIPASYNC

    with app.app_context():

        count_added = 0
        count_protected = 0
        count_errors = 0

        for annotation in annotations:

            if not annotation['id']:
                annotation['id'] = None

            existing = Annotation.query_by_id(annotation['id'])

            if existing:

                if existing.protected:

                    count_protected += 1

                    continue

                elif not existing.protected:

                    db.session.delete(existing)
                    db.session.commit()

            importing = Annotation()
            importing.deserialize(annotation)

            try:
                db.session.add(importing)
                db.session.commit()

                count_added += 1

            except:
                db.session.rollback()
                app.logger.error(sys.exc_info())

                count_errors += 1

        reponse = {
            "added": count_added,
            "protected (skipped)": count_protected,
            "errors": count_errors
        }

        app.logger.info(reponse)


@async_threaded
def run_async_import_annotations_add(app, annotations):

    # WIPASYNC

    with app.app_context():

        count_added = 0
        count_existing = 0
        count_errors = 0

        for annotation in annotations:

            if not annotation['id']:
                annotation['id'] = None

            existing = Annotation.query_by_id(annotation['id'])

            if existing:

                count_existing += 1

                continue

            elif not existing:

                importing = Annotation()
                importing.deserialize(annotation)

                try:
                    db.session.add(importing)
                    db.session.commit()

                    count_added += 1

                except:
                    db.session.rollback()
                    app.logger.error(sys.exc_info())

                    count_errors += 1

        reponse = {
            "added": count_added,
            "existing (skipped)": count_existing,
            "errors": count_errors
        }

        app.logger.info(reponse)
