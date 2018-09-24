#!/usr/bin/env python

import sys
import os

from app import db
from app.models import User, Annotation

from app.admin import admin
from app.admin.tools import admin_only

from flask import redirect, url_for, flash, jsonify
from flask_login import login_required, login_user


@admin.route("/reset")
def reset():
    """

    NOTE this is apparently a hack db.reflect() is broken is Flask-SQLAlchemy.

    """
    try:
        db.reflect()
        db.drop_all()

    except:
        print sys.exc_info()

        return "dropping error"

    #

    try:
        db.create_all()

    except:
        print sys.exc_info()

        return "creation error!"

    #

    try:
        shant = User(
            username=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            admin=False
        )

        db.session.add(shant)
        db.session.commit()

    except:
        print sys.exc_info()

        return "shant creation error!"

    try:
        admin = User(
            username="admin",
            password=os.getenv("PASSWORD"),
            admin=True
        )

        db.session.add(admin)
        db.session.commit()

        login_user(admin, remember=False)

        return redirect(url_for("user.settings"))

    except:
        print sys.exc_info()

        return "admin creation error!"


@admin.route("/remove_unprotected")
@login_required
@admin_only
def remove_unprotected():

    unprotected = Annotation.query.filter_by(protected=False)

    for annotation in Annotation.query.filter_by(protected=False):

        db.session.delete(annotation)

    db.session.commit()

    return "deleted!"


@admin.route("/flash_me/<which>")
@login_required
@admin_only
def flash_me(which=None):

    if which == "success":

        flash("success: this is a great flash!", "success")

    else:

        flash("error: this is a sad flash!", "warning")

    return redirect(url_for("user.settings", mode="tools"))