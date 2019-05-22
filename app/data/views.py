#!/usr/local/bin/python3

from . import data

from app import celery
from app.tools import home_url
from app.data.tools import ExportUserData, RestoreUserData
from app.data.forms import RestoreDataForm
from app.data.tasks import take_nap

from flask import redirect, url_for, request, flash, render_template, current_app, jsonify
from flask_login import login_required, current_user
from celery.result import AsyncResult


# Testing Celery --------------------------------------------------------------

@data.route("/worker/")
def worker():

    worker = {
        "id": "NONE",
        "state": "NONE"
    }

    return render_template("data/worker.html", worker=worker)


@data.route("/run_worker", methods=["POST"])
def run_worker():

    new_worker = request.get_json(force=True)
    nap_length = new_worker.get("napLength", 1)

    task = take_nap.delay(nap_length)

    new_worker = {
        "id": task.id,
        "state": task.state
    }

    return jsonify(new_worker)


@data.route("/get_state", methods=["POST"])
def get_state():

    which_worker = request.get_json(force=True)
    id_ = which_worker.get("id", None)

    result = celery.AsyncResult(id_)

    response = {
        "id": id_,
        "state": result.state,
    }

    try:
        result.info
        response["info"] = result.info
    except:
        pass

    return jsonify(response)

# Testing Celery --------------------------------------------------------------


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
