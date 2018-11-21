#!/usr/bin/env python

import json
import sys
from datetime import datetime
import copy
from StringIO import StringIO

from app import db, mail
from app.models import User, Annotation
from app.tools import async_threaded

from flask import current_app, Response, render_template
from flask_mail import Message
from werkzeug.datastructures import FileStorage


class ExportUserData(object):

    def __init__(self, user, context):

        self.user = user
        self.app = context
        self.date = datetime.now()

    @property
    def user_data(self):
        return json.dumps(self.user.data, indent=4, separators=(",", ": "))

    @property
    def user_data_filename(self):

        date = self.date.strftime("%Y.%m.%d")

        return "{0}_{1}.hlts".format(self.user.username, date)

    @property
    def user_data_attachment(self):

        data = StringIO()
        data.write(self.user_data)
        data.seek(0)

        return data.read()

    def download(self):

        response = Response(
            self.user_data,
            mimetype="text/json",
            headers={
                "Content-disposition":
                "attachment; filename={0}".format(self.user_data_filename)}
        )

        return response

    def email(self):

        date = self.date.strftime("%B %d, %Y")
        user = self.user.display_name

        subject = "{0}'s HLTS data from {1}".format(user, date)
        body = render_template("data/email.txt", user=user, date=date)

        sender = ("The HLTS Team", current_app.config["MAIL_USERNAME"])
        recipients = [self.user.email]

        message = Message(
            subject,
            body=body,
            sender=sender,
            recipients=recipients)

        message.attach(self.user_data_filename, "text/json", self.user_data_attachment)

        self.send_user_data(message)

    @async_threaded
    def send_user_data(self, message):

        with self.app.app_context():

            mail.send(message)


class RestoreUserData(object):

    data = None
    serialized_annotations = None
    serialized_user = None
    annotation_count = 0

    def __init__(self, user, context):

        self.user = user
        self.app = context

    def validate(self, data):
        """

        Validator written to work with Werkzug FileStorage class. In the
        future we need to add a method to verify other input streams as well as
        being able to handle whether the input json is a string or an objet and
        load it accordingly.

        """

        # Genuine .hlts file?

        if isinstance(data, FileStorage):

            if not data.filename.endswith(".hlts"):

                raise Exception("not an .hlts file!")

        # Valid json file?

        try:

            if isinstance(data, FileStorage):
                self.data = json.load(data)
            elif isinstance(data, str):
                self.data = json.loads(data)
            elif isinstance(data, dict):
                self.data = data
            else:
                raise Exception("unrecognized data type!")

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

                annotation = copy.copy(self.serialized_annotations[0])
                annotation["id"] = None

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

        # Remove all annotations
        for annotation in Annotation.query.all():
            annotation.delete()

        try:
            db.session.commit()

        except:
            db.session.rollback()
            current_app.logger.error(sys.exc_info())
            raise Exception("unexpected error clearing annotations!")

    def restore_user_settings(self):

        self.user.deserialize(self.serialized_user)

        try:
            db.session.commit()

        except:
            db.session.rollback()
            current_app.logger.error(sys.exc_info())
            raise Exception("unexpected error restoring user!")

    @async_threaded
    def restore_user_annotations(self):

        # WIPASYNC

        with self.app.app_context():

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