#!/usr/bin/env python

from app.errors import errors

from app import db

from flask import render_template


@errors.app_errorhandler(404)
def error404(error):

    return render_template("errors/404.html"), 404


@errors.app_errorhandler(500)
def error500(error):

    db.session.rollback()

    return render_template("errors/500.html"), 500


