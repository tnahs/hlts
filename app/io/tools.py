#!/usr/bin/env python

import json
import sys
from datetime import datetime

from app import db
from app.models import Annotation

from flask import current_app, flash, abort


class ExportJSON(object):
    """ docstring for ExportJSON
    """
    def __init__(self):

        date = datetime.now().strftime('%Y%m%d')
        query = Annotation.get_all()
        count = query.count()
        data = Annotation.query_to_multiple_dict(query)

        self.annotations = json.dumps(data, indent=4, separators=(',', ': '))
        self.filename = "hlts-export-{}-#{:05d}.json".format(date, count)


class ImportJSON(object):
    """ docstring for ImportJSON
    """

    def __init__(self, file):

        self.annotations = json.load(file)

    def remove_all_annotations(self):

        for result in Annotation.get_all():
            db.session.delete(result)

        db.session.commit()

    def restore_annotations(self):
        """

        WARNING: ERASES WHOLE DATABASE!

        Imports only a previously dumped annotation.

        """

        self.remove_all_annotations()

        for annotation in self.annotations:

            importing = Annotation()

            importing.deserialize(annotation)

            db.session.add(importing)

        try:
            db.session.commit()

            added = len(self.annotations)

            flash('restored {} annotations'.format(added), 'success')

        except:
            db.session.rollback()

            current_app.logger.error(sys.exc_info())

            flash('restore failed: check logs!', 'warning')

            return abort(500)