#!/usr/bin/env python

from app.errors import errors

from app import db

# from flask import render_template


""" TODO http://flask.pocoo.org/docs/1.0/blueprints/#error-handlers """


@errors.errorhandler(404)
def not_found_error(error):

    # return render_template('404.html'), 404

    return "404", 404


@errors.errorhandler(500)
def internal_error(error):

    db.session.rollback()

    # return render_template('500.html'), 500

    return "500", 500
