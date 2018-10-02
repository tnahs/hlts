#!/usr/bin/env python

import json
import sys
from datetime import datetime

from app import db
from app.models import User, Annotation

from flask import current_app
from flask_login import current_user


class ExportUserData(object):

    @property
    def filename(self):

        date = datetime.now().strftime("%Y.%m.%d")

        return "{0}_{1}.hlts".format(current_user.username, date)

    @property
    def data(self):
        return json.dumps(current_user.data, indent=4, separators=(",", ": "))


class RestoreUserData(object):

    data = None
    serialized_annotations = None
    serialized_user = None
    annotation_count = 0

    def validate(self, data):
        """

        Validator written to work with Werkzug FileStorage class. In the
        future we need to add a method to verify other input streams as well as
        being able to handle whether the input json is a string or an objet and
        load it accordingly.

        """

        # Genuine .hlts file?

        if not data.filename.endswith(".hlts"):

            raise Exception("not an .hlts file!")

        # Valid json file?

        try:
            self.data = json.load(data)

        except ValueError as error:
            current_app.logger.error(error)
            raise Exception("invalid .hlts file!")

        except:
            current_app.logger.error(sys.exc_info())
            raise Exception("unexpected error loading data!")

        # Are annotations in right place?

        try:
            self.serialized_annotations = self.data["annotations"]

        except KeyError as error:
            current_app.logger.error(error)
            raise Exception("no annotation data found!")

        except:
            current_app.logger.error(sys.exc_info())
            raise Exception("unexpected error loading annotation data!")

        else:

            # If annotations exist check formatting.

            if self.serialized_annotations:

                self.annotation_count = len(self.serialized_annotations)

                annotation = self.serialized_annotations[0]
                annotation['id'] = None

                try:
                    check_annotation = Annotation()
                    check_annotation.deserialize(annotation)

                except KeyError as error:
                    current_app.logger.error(error)
                    raise Exception("invalid annotation formatting!")

                except:
                    current_app.logger.error(sys.exc_info())
                    raise Exception("unexpected error checking annotation data!")

                finally:
                    db.session.rollback()

        # Is user data in right place?

        try:
            self.serialized_user = self.data["user"]

        except KeyError as error:
            current_app.logger.error(error)
            raise Exception("no user data found!")

        except:
            current_app.logger.error(sys.exc_info())
            raise Exception("unexpected error loading user data!")

        else:

            # Check user settings formatting.

            try:
                check_user = User()
                check_user.deserialize(self.serialized_user)

            except KeyError as error:
                current_app.logger.error(error)
                raise Exception("invalid user data formatting!")

            except:
                current_app.logger.error(sys.exc_info())
                raise Exception("unexpected error checking user data!")

            finally:
                db.session.rollback()

        return True

    def execute(self):

        self.delete_user_annotations()
        self.restore_user_settings()
        self.restore_user_annotations()

    def delete_user_annotations(self):

        Annotation.query.delete()

        try:
            db.session.commit()

        except:
            db.session.rollback()
            current_app.logger.error(sys.exc_info())
            raise Exception("unexpected error clearing annotations!")

    def restore_user_settings(self):

        current_user.deserialize(self.serialized_user)

        try:
            db.session.commit()

        except:
            db.session.rollback()
            current_app.logger.error(sys.exc_info())
            raise Exception("unexpected error restoring user!")

    def restore_user_annotations(self):

        for annotation in self.serialized_annotations:

            importing = Annotation()
            importing.deserialize(annotation)
            db.session.add(importing)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            current_app.logger.error(sys.exc_info())
            raise Exception("unexpected error restoring annotations!")
