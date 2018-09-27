#!/usr/bin/env python

from app.io import io

from app.tools import home_url
from app.io.tools import ExportJSON, ImportJSON

from flask import Response, redirect, url_for, request, flash, render_template
from flask_login import login_required


@io.route('/export_to_json')
@login_required
def export_to_json():

    export = ExportJSON()

    export_to_json = Response(
        export.annotations,
        mimetype='text/json',
        headers={'Content-disposition': 'attachment; filename={0}'.format(export.filename)}
    )

    return export_to_json


@io.route('/restore_from_json', methods=['GET', 'POST'])
@login_required
def restore_from_json():

    if request.method == 'POST':

        confirmed = request.values.get('confirm')

        if 'json' not in request.files:

            flash('No json file selected!', 'warning')

        elif confirmed:

            file_ = request.files['json']

            import_json = ImportJSON(file_)

            import_json.restore_annotations()

        else:
            flash('you must confirm before continuing!', 'warning')

            return redirect(url_for('io.restore_from_json'))

        return redirect(home_url())

    return render_template("io/restore.html")