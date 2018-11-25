#!flask/bin/python

import sys
import click
from os import getenv, path

from app import db
from app.models import User, Annotation, Collection

from flask import json, current_app
from sqlalchemy.exc import IntegrityError


def register_cli(app):

    """ Base Methods """

    def run_init_db():

        try:
            db.create_all()
            click.echo("Database initiated!")

        except:
            click.echo("Unexpected error: {0}".format(sys.exc_info()[0]))

    def run_drop_db():

        if click.confirm("WARNING! Drop all databases?", abort=True):

            try:
                db.drop_all()
                click.echo("Database erased!")

            except:
                click.echo("Unexpected error: {0}".format(sys.exc_info()[0]))

    def run_create_default_user():

        user = User(username=getenv("DEFAULT_APPUSER_USERNAME"),
                    email=getenv("DEFAULT_APPUSER_EMAIL"),
                    is_admin=False)
        user.validate_password(getenv("DEFAULT_APPUSER_PASSWORD"))

        try:
            db.session.add(user)
            db.session.commit()

        except AssertionError as error:
            db.session.rollback()
            click.echo(error)

        except IntegrityError as error:
            db.session.rollback()
            click.echo(error)

        except:
            db.session.rollback()
            click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

        else:
            click.echo("Created Default User!")
            click.echo("<Username: {0.username}> <is admin: {0.is_admin}>".format(user))

    def run_create_admin():

        user = User(username=getenv("ADMIN_APPUSER_USERNAME"),
                    email=getenv("ADMIN_APPUSER_EMAIL"),
                    is_admin=True)
        user.validate_password(getenv("ADMIN_APPUSER_PASSWORD"))

        try:
            db.session.add(user)
            db.session.commit()

        except AssertionError as error:
            db.session.rollback()
            click.echo(error)

        except IntegrityError as error:
            db.session.rollback()
            click.echo(error)

        except:
            db.session.rollback()
            click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

        else:
            click.echo("Created Admin User!")
            click.echo("<Username: {0.username}> <is admin: {0.is_admin}>".format(user))

    def run_create_welcome_annotations():

        welcome_json = path.join(current_app.root_path, "init", "welcome.json")

        with open(welcome_json) as f:
            welcome = json.load(f)

        Collection.restore(welcome["collections"])

        for annotation in welcome["annotations"]:

            importing = Annotation()
            importing.deserialize(annotation)

            db.session.add(importing)

        try:
            db.session.commit()

        except AssertionError as error:
            db.session.rollback()
            click.echo(error)

        except IntegrityError as error:
            db.session.rollback()
            click.echo(error)

        else:
            click.echo("Added welcome annotations!")

    def show_current_users():

        users = User.query.all()
        click.echo("Current users:")
        click.echo("------------------------------")
        click.echo(users)
        click.echo("------------------------------")

    """ CLI Methods """

    @app.cli.command(
        name="init_db",
        help="Create all tables.")
    def init_db():
        run_init_db()

    @app.cli.command(
        name="drop_db",
        help="Drop all tables.")
    def drop_db():
        run_drop_db()

    @app.cli.command(
        name="init_beta",
        help="Create default user and welcome annotations.")
    def init_beta():
        run_create_default_user()
        run_create_welcome_annotations()

    @app.cli.command(
        name="create_default_user",
        help="Create default user.")
    def create_default_user():
        run_create_default_user()

    @app.cli.command(
        name="create_admin",
        help="Create app admin.")
    def create_admin():
        run_create_admin()

    @app.cli.command(
        name="create_welcome_annotations",
        help="Create welcome annotations.")
    def create_welcome_annotations():
        run_create_welcome_annotations()

    @app.cli.command(
        name="create_user",
        help="Create single user.")
    def create_user():

        click.echo("Create user...")

        username = click.prompt("Username")
        password = click.prompt("Password (6-32 characters)", hide_input=True, confirmation_prompt=True)
        email = click.prompt("Email")
        is_admin = click.prompt("Admin?", type=bool, default=False)

        user = User(username=username, email=email, is_admin=is_admin)
        user.validate_password(password)

        db.session.add(user)

        try:
            db.session.commit()

        except AssertionError as error:
            db.session.rollback()
            click.echo(error)

        except IntegrityError as error:
            db.session.rollback()
            click.echo(error)

        except:
            db.session.rollback()
            click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

        else:
            click.echo("Created User!")
            click.echo("<Username: {0.username}> <is admin: {0.is_admin}>".format(user))

    @app.cli.command(
        name="delete_user",
        help="Delete single user.")
    def delete_user():

        show_current_users()

        click.echo("Delete user...")

        username = click.prompt("Username")

        user = User.query.filter_by(username=username).first()

        if user and click.confirm("User exists! Delete user?", abort=True):

            db.session.delete(user)

            try:
                db.session.commit()

            except AssertionError as error:
                db.session.rollback()
                click.echo(error)

            except IntegrityError as error:
                db.session.rollback()
                click.echo(error)

            except:
                db.session.rollback()
                click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

            else:
                click.echo("Deleted user!")

        else:

            click.echo("User does not exist!")

    @app.cli.command(
        name="edit_user",
        help="Edit single user.")
    def edit_user():

        show_current_users()

        click.echo("Edit User...")

        username = click.prompt("Username")

        user = User.query.filter_by(username=username).first()

        if user and click.confirm("User exists! Edit user?", abort=True):

            if click.confirm("Change Username?"):
                new_username = click.prompt("New Username")
                user.username = new_username

            if click.confirm("Change Password?"):
                new_password = click.prompt("New Password (6-32 characters)", hide_input=True, confirmation_prompt=True)
                user.validate_password(new_password)

            if click.confirm("Change Email?"):
                new_email = click.prompt("New Email")
                user.email = new_email

            if click.confirm("Change Admin Status?"):
                new_admin_status = click.prompt("New Admin Status?", type=bool)
                user.is_admin = new_admin_status

            try:
                db.session.commit()

            except AssertionError as error:
                db.session.rollback()
                click.echo(error)

            except IntegrityError as error:
                db.session.rollback()
                click.echo(error)

            except:
                db.session.rollback()
                click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

            else:
                click.echo("Updated User!")
                click.echo("<Username: {0.username}> <is admin: {0.is_admin}>".format(user))

        else:

            click.echo("User does not exist!")

    @app.cli.command(
        name="generate_new_api_key",
        help="Generate new token.")
    def generate_new_api_key():

        show_current_users()

        click.echo("Generate new API key...")

        username = click.prompt("Username")

        user = User.query.filter_by(username=username).first()

        if user and click.confirm("User exists! Generate new API Key?", abort=True):

            user.new_api_key()
            click.echo("New API Key: {0}".format(user.api_key))

        else:

            click.echo("User does not exist!")

    @app.cli.command(
        name="reset_user",
        help="Erase and re-create user.")
    def reset_user():

        if click.confirm("WARNING! Reset user to default?", abort=True):

            # Remove all users
            User.query.delete()

            try:
                db.session.commit()

            except:
                db.session.rollback()
                click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

            else:
                click.echo("Removed all users!")

            # Create users
            run_create_default_user()

    @app.cli.command(
        name="erase_all_annotations",
        help="Erase annotations.")
    def erase_all_annotations():

        if click.confirm("WARNING! Reset annotations?", abort=True):

            # Remove all annotations
            for annotation in Annotation.query.all():
                annotation.delete()

            try:
                db.session.commit()

            except:
                db.session.rollback()
                click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

            else:
                click.echo("Removed all annotations!")

    @app.cli.command(
        name="reset_app",
        help="Drop databases & re-create users.")
    def reset_app():

        if click.confirm("WARNING! Perform full reset?", abort=True):

            run_drop_db()
            run_init_db()

    @app.cli.command(
        name="show_dashboard_notification",
        help="Show Dashboard Notification.")
    def show_dashboard_notification():

        show_current_users()

        username = click.prompt("Username")

        user = User.query.filter_by(username=username).first()

        if user and click.confirm("User exists! Show dashboard notification?", abort=True):

            user.show_dashboard_notification = True
            click.echo("Now showing dashboard notification for {0}".format(user.username))

        else:

            click.echo("User does not exist!")
