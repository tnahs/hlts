#!/usr/bin/env python

from app.errors import errors

from app import db

from flask import render_template, current_app


@errors.app_errorhandler(401)
def error401(exception):

    current_app.logger.error(exception)

    error = {
        "number": 401,
        "message": "unauthorized!",
        "exception": exception
    }

    return render_template("errors/errors.html", error=error), 401


@errors.app_errorhandler(403)
def error400(exception):

    current_app.logger.error(exception)

    error = {
        "number": 403,
        "message": "forbidden!",
        "exception": exception
    }

    return render_template("errors/errors.html", error=error), 403


@errors.app_errorhandler(404)
def error404(exception):

    current_app.logger.error(exception)

    error = {
        "number": 404,
        "message": "file not found!",
        "exception": exception
    }

    return render_template("errors/errors.html", error=error), 404


@errors.app_errorhandler(500)
def error500(exception):

    db.session.rollback()

    current_app.logger.error(exception)

    error = {
        "number": 500,
        "message": "unexpected error! sorry for the convenience!",
        "exception": exception
    }

    return render_template("errors/errors.html", error=error), 500
