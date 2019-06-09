#!/usr/local/bin/python3

from . import data

from app.tools import home_url
from app.data.tools import ExportUserData, RestoreUserData
from app.data.forms import RestoreDataForm

from flask import redirect, url_for, request, flash, render_template, current_app, jsonify
from flask_login import login_required, current_user


@data.route("/download_user_data")
def download_user_data():

    app = current_app._get_current_object()

    export = ExportUserData(user=current_user, context=app)

    return export.download()


# @data.route("/email_user_data")
# @login_required
# def email_user_data():
#
#     app = current_app._get_current_object()
#
#     export = ExportUserData(user=current_user, context=app)
#
#     export.email()
#
#     flash("e-mailed HLTS data to {0}".format(current_user.email), "flashSuccess")
#
#     return redirect(url_for("main.tools"))


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
            # TODO: Exception message not bubbling up.
            flash(repr(error), "flashWarning")
            return redirect(url_for("data.restore_user_data"))

        else:

            try:
                restore.execute()
            except Exception as error:
                # TODO: Exception message not bubbling up.
                flash(repr(error), "flashWarning")
                return redirect(url_for("data.restore_user_data"))

            else:
                flash("restored user settings", "flashSuccess")
                flash("{0} annotations currently restoring in the background"
                      .format(restore.annotation_count), "flashSuccess")
                return redirect(home_url())

    return render_template("data/restore.html", form_restore=form_restore)
