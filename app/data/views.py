#!/usr/bin/env python

from app.data import data

from app.tools import home_url
from app.data.tools import ExportUserData, RestoreUserData
from app.data.forms import RestoreDataForm

from flask import redirect, url_for, request, flash, render_template, \
    current_app
from flask_login import login_required, current_user


@data.route("/download_user_data")
@login_required
def download_user_data():

    app = current_app._get_current_object()

    export = ExportUserData(user=current_user, context=app)

    return export.download()


@data.route("/email_user_data")
@login_required
def email_user_data():

    app = current_app._get_current_object()

    export = ExportUserData(user=current_user, context=app)
    export.email()

    flash("e-mailed HLTS data to {0}!".format(current_user.email), "success")

    return redirect(url_for("main.tools"))


@data.route("/restore_user_data", methods=["GET", "POST"])
@login_required
def restore_user_data():

    # WIPASYNC

    app = current_app._get_current_object()

    form_restore = RestoreDataForm()

    if request.method == "POST":

        data = request.files["hlts_file"]

        restore = RestoreUserData(user=current_user, context=app)

        try:
            restore.validate(data)
        except Exception as error:
            flash(error.message, "warning")
            return redirect(url_for("data.restore_user_data"))

        else:

            try:
                restore.execute()
            except Exception as error:
                flash(error.message, "warning")
                return redirect(url_for("data.restore_user_data"))

            else:
                flash("restored user settings and {0} annotations".format(restore.annotation_count), "success")
                return redirect(home_url())

    return render_template("data/restore.html", form_restore=form_restore)
