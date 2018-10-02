#!/usr/bin/env python

from app.io import io

from app.tools import home_url
from app.io.tools import ExportUserData, RestoreUserData
from app.io.forms import RestoreDataForm

from flask import Response, redirect, url_for, request, flash, render_template
from flask_login import login_required


@io.route("/export_user_data")
@login_required
def export_user_data():

    export = ExportUserData()

    data = Response(
        export.data,
        mimetype="text/json",
        headers={
            "Content-disposition":
            "attachment; filename={0}".format(export.filename)}
    )

    return data


@io.route("/restore_user_data", methods=["GET", "POST"])
@login_required
def restore_user_data():

    form_restore = RestoreDataForm()

    if request.method == "POST":

        data = request.files["hlts_file"]

        restore = RestoreUserData()

        try:
            restore.validate(data)
        except Exception as error:
            flash(error.message, "warning")
            return redirect(url_for("io.restore_user_data"))

        else:

            try:
                restore.execute()
            except Exception as error:
                flash(error.message, "warning")
                return redirect(url_for("io.restore_user_data"))

            else:
                flash("restored user settings and {0} annotations".format(restore.annotation_count), "success")
                return redirect(home_url())

    return render_template("io/restore.html", form_restore=form_restore)
