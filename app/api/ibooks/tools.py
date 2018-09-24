#!/usr/bin/env python

import re
from datetime import datetime

from app.api.ibooks import defaults as IBooksDefaults

from app import db
from app.models import Annotation


class IBooksSyncAPI(object):

    def __init__(self, ignoring=None):

        # TODO Add a way for user to input their ignore preferences

        self.ignoring = ignoring if ignoring else IBooksDefaults.IGNORING

        self._new = 0
        self._refreshed = 0
        self._protected = 0
        self._exists = 0
        self._ignored = 0
        self._errors = 0

    @property
    def response(self):

        ignoring_response = []

        for color, ignore in self.ignoring.items():

            if ignore:

                ignoring_response.append(color)

        response = {
            "a. new":                self._new,
            "b. refreshed":          self._refreshed,
            "c. skipped: protected": self._protected,
            "d. skipped: exists":    self._exists,
            "e. skipped: ignored":   self._ignored,
            "f. errors":             self._errors,
            "g. ignoring":           ignoring_response
        }

        return response

    @staticmethod
    def notes_to_tags_and_collections(notes):
        """ splits tags from 'notes' and append them as 'tags'
        """
        TAG_PREFIX_re = re.compile(IBooksDefaults.TAG_PREFIX)
        TAG_PATTERN_re = re.compile(IBooksDefaults.TAG_PATTERN)

        COLLECTION_PREFIX_re = re.compile(IBooksDefaults.COLLECTION_PREFIX)
        COLLECTION_PATTERN_re = re.compile(IBooksDefaults.COLLECTION_PATTERN)

        if notes:

            # extract tags from notes
            tags = re.findall(TAG_PATTERN_re, notes)
            tags = [tag.strip() for tag in tags]
            tags = [re.sub(TAG_PREFIX_re, '', tag) for tag in tags]

            # extract collections from notes
            collections = re.findall(COLLECTION_PATTERN_re, notes)
            collections = [collection.strip() for collection in collections]
            collections = [re.sub(COLLECTION_PREFIX_re, '', collection) for collection in collections]

            # remove tags from notes
            notes = re.sub(TAG_PATTERN_re, '', notes)
            notes = re.sub(COLLECTION_PATTERN_re, '', notes)
            notes = notes.strip()

        else:

            notes = ""
            tags = []
            collections = []

        data = {
            "notes": notes,
            "tags": tags,
            "collections": collections
        }

        return data

    @staticmethod
    def markdown_linebreaks(passage):
        """ Add linebreaks for Markdown compatibility.
        """
        return passage.replace("\n", "\n\n")

    @staticmethod
    def epoch_to_iso8601(date_epoch):
        """ docstring
        """
        seconds_since_epoch = float(date_epoch) + IBooksDefaults.NS_TIME_INTERVAL_SINCE_1970

        date = datetime.utcfromtimestamp(seconds_since_epoch)

        return date.isoformat()

    def ignore_annotation(self, color):
        """ Ignore annotations based on user preferences
        """
        if color == 0 and self.ignoring['underline']:
            return True

        if color == 1 and self.ignoring['green']:
            return True

        if color == 2 and self.ignoring['blue']:
            return True

        if color == 3 and self.ignoring['yellow']:
            return True

        if color == 4 and self.ignoring['pink']:
            return True

        if color == 5 and self.ignoring['purple']:
            return True

        return False

    def sync_annotations(self, annotations):
        """ docstring
        """

        for annotation in annotations['add']:

            if self.ignore_annotation(annotation['color']):

                self._ignored += 1

                continue

            """ Check for annotation
            """

            exists = Annotation.query_by_id(annotation['id'])

            if exists:

                self._exists += 1

            else:

                self.import_annotation(annotation)

                self._new += 1

        for annotation in annotations['refresh']:

            if self.ignore_annotation(annotation['color']):

                self._ignored += 1

                continue

            """ Check for annotation
            """

            exists = Annotation.query_by_id(annotation['id'])

            # TODO clean up the logic here?

            if exists:

                if exists.protected:

                    self._protected += 1

                    continue

                else:

                    db.session.delete(exists)
                    db.session.commit()

            self.import_annotation(annotation)

            self._refreshed += 1

    def import_annotation(self, annotation):

        # id = annotation['id']
        # collection = annotation['collection']
        # color = annotation['color']
        passage = annotation['passage']
        notes = annotation['notes']
        source = annotation['source']
        author = annotation['author']
        created = annotation['created']
        modified = annotation['modified']

        """ Process data...
        """

        # Passage
        annotation['passage'] = self.markdown_linebreaks(passage)

        # Notes / Tags / Collections
        processed = self.notes_to_tags_and_collections(notes)

        annotation['notes'] = processed['notes']
        annotation['tags'] = processed['tags']
        annotation['collections'] = processed['collections']

        # Dates
        annotation['created'] = self.epoch_to_iso8601(created)
        annotation['modified'] = self.epoch_to_iso8601(modified)

        """ Re-align source...
        """

        annotation['source'] = {}
        annotation['source']['name'] = source
        annotation['source']['author'] = author

        """ Set defaults...
        """

        annotation['origin'] = IBooksDefaults.ORIGIN
        annotation['protected'] = False
        annotation['deleted'] = False

        """ Instansiate Annotation()
        """

        importing = Annotation()
        importing.deserialize(annotation)

        db.session.add(importing)

        try:
            db.session.commit()

        except:
            db.session.rollback()

            self._errors += 1
