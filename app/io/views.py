#!/usr/bin/env python

from app.io import io

from app.io.tools import ExportJSON, ImportJSON

from flask import Response, redirect, url_for, request, flash
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

        confirm = request.values.get('confirm')

        if 'json' not in request.files:

            flash('No json file selected!', 'warning')

        elif confirm:

            file_ = request.files['json']

            import_json = ImportJSON(file_)

            import_json.restore_annotations()

        else:
            flash('must confirm!', 'warning')

        return redirect(url_for('user.settings'))

    return '''
            <h1>restore annotations from json</h1>
            <br>
            <h1>** THIS WILL DELETE ALL THE CURRENT ANNOTATIONS **</h1>
            <form method="POST" action="/io/restore_from_json" enctype=multipart/form-data>
                <input type="file" name="json">
                <br> confirm? <input type="checkbox" name="confirm"/>
                <br> <button type="submit">restore</button>
            </form>
            '''